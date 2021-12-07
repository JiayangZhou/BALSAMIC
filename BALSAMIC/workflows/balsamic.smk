# vim: syntax=python tabstop=4 expandtab
# coding: utf-8
import os
import logging
import tempfile

from pathlib import Path
from yapf.yapflib.yapf_api import FormatFile

from snakemake.exceptions import RuleException, WorkflowError

from PyPDF2 import PdfFileMerger

from BALSAMIC.utils.exc import BalsamicError

from BALSAMIC.utils.cli import (write_json, check_executable, generate_h5)

from BALSAMIC.utils.models import VarCallerFilter, BalsamicWorkflowConfig

from BALSAMIC.utils.workflowscripts import plot_analysis

from BALSAMIC.utils.rule import (get_variant_callers, get_rule_output, get_result_dir,
                                 get_vcf, get_picard_mrkdup, get_sample_type,
                                 get_threads, get_script_path, get_sequencing_type, get_capture_kit)

from BALSAMIC.constants.common import (SENTIEON_DNASCOPE, SENTIEON_TNSCOPE,
                                    RULE_DIRECTORY, VCFANNO_TOML, MUTATION_TYPE);
from BALSAMIC.constants.variant_filters import COMMON_SETTINGS,VARDICT_SETTINGS,SENTIEON_VARCALL_SETTINGS;
from BALSAMIC.constants.workflow_params import WORKFLOW_PARAMS, VARCALL_PARAMS
from BALSAMIC.constants.workflow_rules import SNAKEMAKE_RULES 


shell.executable("/bin/bash")
shell.prefix("set -eo pipefail; ")

LOG = logging.getLogger(__name__)
logging.getLogger("filelock").setLevel("WARN")

# Create a temporary directory with trailing /
tmp_dir = os.path.join(get_result_dir(config), "tmp", "" )
Path.mkdir(Path(tmp_dir), exist_ok=True)

benchmark_dir = config["analysis"]["benchmark"]
fastq_dir = get_result_dir(config) + "/fastq/"
bam_dir = get_result_dir(config) + "/bam/"
cnv_dir = get_result_dir(config) + "/cnv/"
fastqc_dir = get_result_dir(config) + "/fastqc/"
result_dir = get_result_dir(config) + "/"
vcf_dir = get_result_dir(config) + "/vcf/"
vep_dir = get_result_dir(config) + "/vep/"
qc_dir = get_result_dir(config) + "/qc/"
delivery_dir = get_result_dir(config) + "/delivery/"

umi_dir = get_result_dir(config) + "/umi/" 
umi_qc_dir = qc_dir + "umi_qc/"

singularity_image = config['singularity']['image']

# picarddup flag
picarddup = get_picard_mrkdup(config)

# Varcaller filter settings
COMMON_FILTERS = VarCallerFilter.parse_obj(COMMON_SETTINGS)
VARDICT = VarCallerFilter.parse_obj(VARDICT_SETTINGS)
SENTIEON_CALLER = VarCallerFilter.parse_obj(SENTIEON_VARCALL_SETTINGS)

# parse parameters as constants to workflows
params = BalsamicWorkflowConfig.parse_obj(WORKFLOW_PARAMS)

# Capture kit name
if config["analysis"]["sequencing_type"] != "wgs":
    capture_kit = os.path.split(config["panel"]["capture_kit"])[1]

# Sample names for tumor or normal
tumor_sample = get_sample_type(config["samples"], "tumor")[0]
if config['analysis']['analysis_type'] == "paired":
    normal_sample = get_sample_type(config["samples"], "normal")[0]

# Set case id/name
case_id = config["analysis"]["case_id"]

# explicitly check if cluster_config dict has zero keys.
if len(cluster_config.keys()) == 0:
    cluster_config = config

# Find and set Sentieon binary and license server from env variables
try:
    config["SENTIEON_LICENSE"] = os.environ["SENTIEON_LICENSE"]
    config["SENTIEON_INSTALL_DIR"] = os.environ["SENTIEON_INSTALL_DIR"]

    if os.getenv("SENTIEON_EXEC") is not None:
        config["SENTIEON_EXEC"] = os.environ["SENTIEON_EXEC"]
    else:
        config["SENTIEON_EXEC"] = Path(os.environ["SENTIEON_INSTALL_DIR"], "bin", "sentieon").as_posix()

    config["SENTIEON_TNSCOPE"] = SENTIEON_TNSCOPE
    config["SENTIEON_DNASCOPE"] = SENTIEON_DNASCOPE
    
except KeyError as error:
    LOG.error("Set environment variables SENTIEON_LICENSE, SENTIEON_INSTALL_DIR, SENTIEON_EXEC "
              "to run SENTIEON variant callers")
    raise BalsamicError

if not Path(config["SENTIEON_EXEC"]).exists():
    LOG.error("Sentieon executable not found {}".format(Path(config["SENTIEON_EXEC"]).as_posix()))
    raise BalsamicError

# Add reference assembly if not defined for backward compatibility
if 'genome_version' not in config["reference"]:
    GENOME_VERSION = 'hg19' ## if hg19 convention works, replace accordingly
    LOG.info('Genome version was not found in config. Setting it to %s', GENOME_VERSION)

# Add normal sample if analysis is paired
germline_call_samples = ["tumor"]
if config['analysis']['analysis_type'] == "paired":
    germline_call_samples.append("normal")

# Create list of chromosomes in panel for panel only variant calling to be used in rules
if config["analysis"]["sequencing_type"] != "wgs":
    chromlist = config["panel"]["chrom"]

background_variant_file = ""
if "background_variants" in config:
    background_variant_file = config["background_variants"]

# Set temporary dir environment variable
os.environ["SENTIEON_TMPDIR"] = result_dir
os.environ['TMPDIR'] = get_result_dir(config)

# Extract variant callers for the workflow
germline_caller = []
somatic_caller = []
for m in MUTATION_TYPE:
    germline_caller_balsamic = get_variant_callers(config=config,
                                            analysis_type=config['analysis']['analysis_type'],
                                            workflow_solution="BALSAMIC",
                                            mutation_type=m,
                                            sequencing_type=config["analysis"]["sequencing_type"],
                                            mutation_class="germline")

    germline_caller_sentieon = get_variant_callers(config=config,
                                           analysis_type=config['analysis']['analysis_type'],
                                           workflow_solution="Sentieon",
                                           mutation_type=m,
                                           sequencing_type=config["analysis"]["sequencing_type"],
                                           mutation_class="germline")

    germline_caller = germline_caller + germline_caller_balsamic + germline_caller_sentieon 


    somatic_caller_balsamic = get_variant_callers(config=config,
                                           analysis_type=config['analysis']['analysis_type'],
                                           workflow_solution="BALSAMIC",
                                           mutation_type=m,
                                           sequencing_type=config["analysis"]["sequencing_type"],
                                           mutation_class="somatic")

    somatic_caller_sentieon = get_variant_callers(config=config,
                                             analysis_type=config['analysis']['analysis_type'],
                                             workflow_solution="Sentieon",
                                             mutation_type=m,
                                             sequencing_type=config["analysis"]["sequencing_type"],
                                             mutation_class="somatic")

    somatic_caller_sentieon_umi = get_variant_callers(config=config,
                                             analysis_type=config['analysis']['analysis_type'],
                                             workflow_solution="Sentieon_umi",
                                             mutation_type=m,
                                             sequencing_type=config["analysis"]["sequencing_type"],
                                             mutation_class="somatic")
    somatic_caller = somatic_caller + somatic_caller_sentieon_umi + somatic_caller_balsamic + somatic_caller_sentieon

# Collect only snv callers for calculating tmb
somatic_caller_tmb = []
for ws in ["BALSAMIC","Sentieon","Sentieon_umi"]:
    somatic_caller_snv = get_variant_callers(config=config,
                                           analysis_type=config['analysis']['analysis_type'],
                                           workflow_solution=ws,
                                           mutation_type="SNV",
                                           sequencing_type=config["analysis"]["sequencing_type"],
                                           mutation_class="somatic")
    somatic_caller_tmb +=  somatic_caller_snv

# Remove variant callers from list of callers
if "disable_variant_caller" in config:
    variant_callers_to_remove = config["disable_variant_caller"].split(",")
    for var_caller in variant_callers_to_remove:
        if var_caller in somatic_caller:
            somatic_caller.remove(var_caller)
        if var_caller in germline_caller:
            germline_caller.remove(var_caller)

LOG.info(f"The following Germline variant callers will be included in the workflow: {germline_caller}")
LOG.info(f"The following somatic variant callers will be included in the workflow: {somatic_caller}")

rules_to_include = []
analysis_type = config['analysis']["analysis_type"]
sequence_type = config['analysis']["sequencing_type"]

for sub,value in SNAKEMAKE_RULES.items():
  if sub in ["common", analysis_type + "_" + sequence_type]:
    for module_name,module_rules in value.items():
      rules_to_include.extend(module_rules)

LOG.info(f"The following rules will be included in the workflow: {rules_to_include}")

for r in rules_to_include:
    include: Path(RULE_DIRECTORY, r).as_posix()

# Define common and analysis specific outputs
quality_control_results = [result_dir + "qc/" + "multiqc_report.html"]

analysis_specific_results = [expand(vep_dir + "{vcf}.vcf.gz",
                                    vcf=get_vcf(config, germline_caller, germline_call_samples)),
                             expand(vep_dir + "{vcf}.all.vcf.gz",
                                    vcf=get_vcf(config, somatic_caller, [config["analysis"]["case_id"]]))]

if config["analysis"]["sequencing_type"] != "wgs":
    analysis_specific_results.append(expand(vep_dir + "{vcf}.all.filtered.pass.ranked.vcf.gz",
                                           vcf=get_vcf(config, ["vardict"], [config["analysis"]["case_id"]])))

    analysis_specific_results.append(expand(umi_qc_dir + "{sample}.umi.mean_family_depth", sample=config["samples"]))

    if background_variant_file:
        analysis_specific_results.extend([expand(umi_qc_dir + "{case_name}.{var_caller}.AFtable.txt",
                                      case_name=config["analysis"]["case_id"],
                                      var_caller=["TNscope_umi"])]),

#Calculate TMB per somatic variant caller
analysis_specific_results.extend(expand(vep_dir + "{vcf}.balsamic_stat",
                                        vcf=get_vcf(config, somatic_caller_tmb, [config["analysis"]["case_id"]])))

#Gather all the filtered and PASSed variants post annotation
analysis_specific_results.extend([expand(vep_dir + "{vcf}.all.filtered.pass.vcf.gz",
                                        vcf=get_vcf(config, somatic_caller, [config["analysis"]["case_id"]]))])

LOG.info(f"Following outputs will be delivered {analysis_specific_results}")

if config["analysis"]["sequencing_type"] == "wgs" and config['analysis']['analysis_type'] == "single":
    if "dragen" in config:
        analysis_specific_results.extend([Path(result_dir, "dragen", "SNV.somatic." + config["analysis"]["case_id"] + ".dragen_tumor.bam").as_posix(),
                                          Path(result_dir, "dragen", "SNV.somatic." + config["analysis"]["case_id"] + ".dragen.vcf.gz").as_posix()])

if config["analysis"]["sequencing_type"] == "wgs" and config['analysis']['analysis_type'] == "paired":
    analysis_specific_results.append(expand(vcf_dir + "{vcf}.output.pdf", vcf=get_vcf(config, ["ascat"], [config["analysis"]["case_id"]])))

if 'benchmark_plots' in config:
    log_dir = config["analysis"]["log"]
    if not check_executable("sh5util"):
        LOG.warning("sh5util executable does not exist. Won't be able to plot analysis")
    else:
        # Make individual plot per job
        for log_file in Path(log_dir).glob("*.err"):
            log_file_list = log_file.name.split(".")
            job_name = ".".join(log_file_list[0:4]) 
            job_id = log_file_list[4].split("_")[1]
            h5_file = generate_h5(job_name, job_id, log_file.parent)
            benchmark_plot = Path(benchmark_dir, job_name + ".pdf")

            log_file_plot = plot_analysis(log_file, h5_file, benchmark_plot)
            logging.debug("Plot file for {} available at: {}".format(log_file.as_posix(), log_file_plot))

        # Merge plots into one based on rule name
        for my_rule in vars(rules).keys():
            my_rule_pdf = PdfFileMerger()
            my_rule_plots = list()
            for plots in Path(benchmark_dir).glob(f"BALSAMIC*.{my_rule}.*.pdf"):
                my_rule_pdf.append(plots.as_posix())
                my_rule_plots.append(plots)
            my_rule_pdf.write(Path(benchmark_dir, my_rule+".pdf").as_posix())
            my_rule_pdf.close()

            # Delete previous plots after merging
            for plots in my_rule_plots:
                plots.unlink()



if 'delivery' in config:
    wildcard_dict = {"sample": list(config["samples"].keys())+["tumor", "normal"],
                     "case_name": config["analysis"]["case_id"],
                     "allow_missing": True
                     }

    if config['analysis']["analysis_type"] in ["paired", "single"]:
        wildcard_dict.update({"var_type": ["CNV", "SNV", "SV"],
                              "var_class": ["somatic", "germline"],
                              "var_caller": somatic_caller + germline_caller,
                              "bedchrom": config["panel"]["chrom"] if "panel" in config else [],
                              })

    if 'rules_to_deliver' in config:
        rules_to_deliver = config['rules_to_deliver'].split(",")
    else:
        rules_to_deliver = ['multiqc']

    output_files_ready = [('path', 'path_index', 'step', 'tag', 'id', 'format')]

    for my_rule in set(rules_to_deliver):
        try:
            housekeeper_id = getattr(rules, my_rule).params.housekeeper_id
        except (ValueError, AttributeError, RuleException, WorkflowError) as e:
            LOG.warning("Cannot deliver step (rule) {}: {}".format(my_rule, e))
            continue

        LOG.info("Delivering step (rule) {} {}.".format(my_rule, housekeeper_id))
        files_to_deliver = get_rule_output(rules=rules, rule_name=my_rule, output_file_wildcards=wildcard_dict)
        LOG.debug("The following files added to delivery: {}".format(files_to_deliver))
        output_files_ready.extend(files_to_deliver)

    output_files_ready = [dict(zip(output_files_ready[0], value)) for value in output_files_ready[1:]]
    delivery_ready = os.path.join(get_result_dir(config),
                                  "delivery_report",
                                  config["analysis"]["case_id"] + "_delivery_ready.hk")
    write_json(output_files_ready, delivery_ready)
    FormatFile(delivery_ready)

rule all:
    input:
        quality_control_results + analysis_specific_results
    output:
        qc_json_file = os.path.join(get_result_dir(config), "qc", "qc_metrics_summary.json"),
        finish_file = os.path.join(get_result_dir(config), "analysis_finish")
    params:
        tmp_dir = tmp_dir,
        result_dir = result_dir,
        sequencing_type = get_sequencing_type(config),
        panel_bed = get_capture_kit(config)
    run:
        import datetime
        import shutil

        from BALSAMIC.utils.qc_metrics import get_qc_metrics_json

        # Save QC metrics to a JSON file
        try:
            qc_metrics_summary = get_qc_metrics_json(params.result_dir, params.sequencing_type, params.panel_bed)
            write_json(qc_metrics_summary, str(output.qc_json_file))
        except ValueError as val_exc:
            LOG.error(val_exc)
            raise BalsamicError

        # Delete a temporal directory tree
        try:
            shutil.rmtree(params.tmp_dir)
        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))

        # Finish timestamp file
        with open(str(output.finish_file), mode="w") as finish_file:
            finish_file.write("%s\n" % datetime.datetime.now())
