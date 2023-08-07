import json
import logging
import os
import subprocess
import sys
from pathlib import Path

import click

from BALSAMIC.constants.cluster import ClusterConfigType
from BALSAMIC.constants.paths import SCHEDULER_PATH
from BALSAMIC.constants.workflow_params import VCF_DICT
from BALSAMIC.models.snakemake import SnakemakeExecutable
from BALSAMIC.utils.analysis import get_singularity_bind_paths
from BALSAMIC.utils.cli import (
    createDir,
    get_snakefile,
    job_id_dump_to_yaml,
    get_config_path,
)

LOG = logging.getLogger(__name__)


@click.command(
    "analysis", short_help="Run the analysis on a provided sample config-file"
)
@click.option(
    "-S",
    "--snake-file",
    type=click.Path(),
    show_default=True,
    help=(
        "Input for a custom snakefile. WARNING: "
        "This is for internal testing, and should "
        "not be used. Providing a snakefile supersedes"
        "analysis_type option."
    ),
)
@click.option(
    "-s",
    "--sample-config",
    required=True,
    type=click.Path(),
    help="Sample json config file.",
)
@click.option(
    "--run-mode",
    show_default=True,
    default="cluster",
    type=click.Choice(["local", "cluster"]),
    help=(
        "Run mode to use. By default SLURM will be used to "
        "run the analysis. But local runner also available "
        "for local computing"
    ),
)
@click.option(
    "-c",
    "--cluster-config",
    show_default=True,
    default=get_config_path(ClusterConfigType.ANALYSIS),
    type=click.Path(),
    help="cluster config json file. (eg- SLURM, QSUB)",
)
@click.option(
    "--dragen", is_flag=True, default=False, help="Enable dragen variant caller"
)
@click.option(
    "-p",
    "--profile",
    default="slurm",
    type=click.Choice(["slurm", "qsub"]),
    help="cluster profile to submit jobs",
)
@click.option(
    "--benchmark",
    default=False,
    is_flag=True,
    help="Profile slurm jobs using the value of this option. Make sure you have slurm profiler enabled in your HPC.",
)
@click.option(
    "-r",
    "--run-analysis",
    show_default=True,
    default=False,
    is_flag=True,
    help=(
        "By default balsamic run_analysis will run in "
        "dry run mode. Raise thise flag to make the "
        "actual analysis"
    ),
)
@click.option(
    "--qos",
    type=click.Choice(["low", "normal", "high", "express"]),
    show_default=True,
    default="low",
    help=f"QOS for sbatch jobs. Passed to {SCHEDULER_PATH.as_posix()}",
)
@click.option(
    "-f",
    "--force-all",
    show_default=True,
    default=False,
    is_flag=True,
    help="Force run all analysis. This is same as snakemake --forceall",
)
@click.option(
    "--snakemake-opt", multiple=True, help="Pass these options directly to snakemake"
)
@click.option(
    "--account",
    "--slurm-account",
    "--qsub-account",
    help="cluster account to run jobs, ie: slurm_account",
)
@click.option(
    "--mail-user", help="cluster mail user to send out email. e.g.: slurm_mail_user"
)
@click.option(
    "-q",
    "--quiet",
    default=False,
    is_flag=True,
    help="Instruct snakemake to be quiet! No output will be printed",
)
@click.option(
    "--mail-type",
    type=click.Choice(
        [
            "NONE",
            "BEGIN",
            "END",
            "FAIL",
            "REQUEUE",
            "ALL",
            "TIME_LIMIT",
        ]
    ),
    help=(
        "cluster mail type to send out email. This will "
        "be applied to all jobs and override snakemake settings."
    ),
)
@click.option(
    "--disable-variant-caller",
    help=(
        f"Run workflow with selected variant caller(s) disable."
        f"Use comma to remove multiple variant callers. Valid "
        f"values are: {list(VCF_DICT.keys())}"
    ),
)
@click.pass_context
def analysis(
    context,
    snake_file,
    sample_config,
    run_mode,
    cluster_config,
    run_analysis,
    force_all,
    snakemake_opt,
    mail_type,
    mail_user,
    account,
    qos,
    profile,
    disable_variant_caller,
    quiet,
    dragen,
    benchmark,
):
    """
    Runs BALSAMIC workflow on the provided sample's config file
    """
    LOG.info(f"BALSAMIC started with log level {context.obj['loglevel']}.")

    if run_mode == "cluster" and not run_analysis:
        LOG.info("Changing run-mode to local on dry-run")
        run_mode = "local"

    if run_mode == "cluster" and not account:
        LOG.info(
            "slurm-account, qsub-account, or account is required for slurm run mode"
        )
        raise click.Abort()

    sample_config_path: Path = Path(sample_config).absolute()
    with open(sample_config_path, "r") as sample_fh:
        sample_config = json.load(sample_fh)

    logpath = sample_config["analysis"]["log"]
    scriptpath = sample_config["analysis"]["script"]
    resultpath = sample_config["analysis"]["result"]
    benchmarkpath = sample_config["analysis"]["benchmark"]
    case_name = sample_config["analysis"]["case_id"]

    if run_analysis:
        # if not dry run, then create (new) log/script directory
        for dirpath, dirnames, files in os.walk(logpath):
            if files:
                logpath = createDir(logpath, [])
                scriptpath = createDir(scriptpath, [])
                sample_config["analysis"]["benchmark"] = createDir(benchmarkpath, [])

    # Create result directory
    os.makedirs(resultpath, exist_ok=True)

    if not os.path.exists(logpath):
        os.makedirs(logpath, exist_ok=True)
        os.makedirs(scriptpath, exist_ok=True)
        os.makedirs(benchmarkpath, exist_ok=True)

    analysis_type = sample_config["analysis"]["analysis_type"]
    analysis_workflow = sample_config["analysis"]["analysis_workflow"]
    analysis_dir: Path = Path(sample_config["analysis"]["analysis_dir"])
    snakefile: Path = (
        snake_file if snake_file else get_snakefile(analysis_type, analysis_workflow)
    )

    LOG.info(f"Starting {analysis_workflow} workflow...")
    snakemake_executable: SnakemakeExecutable = SnakemakeExecutable(
        account=account,
        benchmark=benchmark,
        case_id=case_name,
        cluster_config_path=cluster_config,
        config_path=sample_config_path,
        disable_variant_caller=disable_variant_caller,
        dragen=dragen,
        force=force_all,
        log_dir=logpath,
        mail_type=mail_type,
        mail_user=mail_user,
        profile=profile,
        qos=qos,
        quiet=quiet,
        result_dir=resultpath,
        run_analysis=run_analysis,
        run_mode=run_mode,
        script_dir=scriptpath,
        singularity_bind_paths=get_singularity_bind_paths(sample_config),
        snakefile=snakefile,
        snakemake_options=snakemake_opt,
        working_dir=Path(analysis_dir, case_name, "BALSAMIC_run"),
    )
    subprocess.run(
        f"{sys.executable} -m {snakemake_executable.get_command()}",
        shell=True,
    )

    if run_analysis and run_mode == "cluster":
        jobid_dump = Path(logpath, f"{case_name}.sacct")
        jobid_yaml = Path(resultpath, f"{profile}_jobids.yaml")
        job_id_dump_to_yaml(
            job_id_dump=jobid_dump, job_id_yaml=jobid_yaml, case_name=case_name
        )
