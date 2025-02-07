from unittest import mock
import snakemake

from BALSAMIC.utils.cli import get_snakefile

MOCKED_OS_ENVIRON = "os.environ"


def test_workflow_tumor_normal(
    tumor_normal_config, sentieon_install_dir, sentieon_license
):
    # GIVEN a sample config dict and snakefile
    workflow = "paired"
    reference_genome = "hg19"
    analysis_workflow = "balsamic"
    snakefile = get_snakefile(workflow, analysis_workflow, reference_genome)
    config_json = tumor_normal_config

    # WHEN invoking snakemake module with dryrun option
    # THEN it should return true
    with mock.patch.dict(
        MOCKED_OS_ENVIRON,
        {
            "SENTIEON_LICENSE": sentieon_license,
            "SENTIEON_INSTALL_DIR": sentieon_install_dir,
        },
    ):
        assert snakemake.snakemake(snakefile, configfiles=[config_json], dryrun=True)


def test_workflow_tumor_only(tumor_only_config, sentieon_install_dir, sentieon_license):
    # GIVEN a sample config dict and snakefile
    workflow = "single"
    reference_genome = "hg19"
    analysis_workflow = "balsamic"
    snakefile = get_snakefile(workflow, analysis_workflow, reference_genome)
    config_json = tumor_only_config

    # WHEN invoking snakemake module with dryrun option
    # THEN it should return true
    with mock.patch.dict(
        MOCKED_OS_ENVIRON,
        {
            "SENTIEON_LICENSE": sentieon_license,
            "SENTIEON_INSTALL_DIR": sentieon_install_dir,
        },
    ):
        assert snakemake.snakemake(snakefile, configfiles=[config_json], dryrun=True)


def test_workflow_qc_tumor_only(tumor_only_config):

    # GIVEN a sample config dict and snakefile
    workflow = "single"
    reference_genome = "hg19"
    analysis_workflow = "balsamic-qc"
    snakefile = get_snakefile(workflow, analysis_workflow, reference_genome)
    config_json = tumor_only_config

    # WHEN invoking snakemake module with dryrun option
    # THEN it should return true
    with mock.patch.dict(
        MOCKED_OS_ENVIRON,
    ):
        assert snakemake.snakemake(snakefile, configfiles=[config_json], dryrun=True)


def test_workflow_qc_tumor_only_canfam(tumor_only_config):

    # GIVEN a sample config dict and snakefile
    workflow = "single"
    reference_genome = "canfam3"
    analysis_workflow = "balsamic-qc"
    snakefile = get_snakefile(workflow, analysis_workflow, reference_genome)
    config_json = tumor_only_config

    # WHEN invoking snakemake module with dryrun option
    # THEN it should return true
    with mock.patch.dict(
        MOCKED_OS_ENVIRON,
    ):
        assert snakemake.snakemake(snakefile, configfiles=[config_json], dryrun=True)


def test_workflow_qc_normal(tumor_normal_config):
    # GIVEN a sample config dict and snakefile
    workflow = "paired"
    reference_genome = "hg19"
    analysis_workflow = "balsamic-qc"
    snakefile = get_snakefile(workflow, analysis_workflow, reference_genome)
    config_json = tumor_normal_config

    # WHEN invoking snakemake module with dryrun option
    # THEN it should return true
    with mock.patch.dict(
        MOCKED_OS_ENVIRON,
    ):
        assert snakemake.snakemake(snakefile, configfiles=[config_json], dryrun=True)


def test_workflow_qc_normal_canfam3(tumor_normal_config):
    # GIVEN a sample config dict and snakefile
    workflow = "paired"
    reference_genome = "canfam3"
    analysis_workflow = "balsamic-qc"
    snakefile = get_snakefile(workflow, analysis_workflow, reference_genome)
    config_json = tumor_normal_config

    # WHEN invoking snakemake module with dryrun option
    # THEN it should return true
    with mock.patch.dict(
        MOCKED_OS_ENVIRON,
    ):
        assert snakemake.snakemake(snakefile, configfiles=[config_json], dryrun=True)


def test_workflow_sentieon(
    tumor_normal_wgs_config,
    tumor_only_wgs_config,
    sentieon_install_dir,
    sentieon_license,
):
    # GIVEN a sample config dict and snakefile
    workflows = [("single", tumor_only_wgs_config), ("paired", tumor_normal_wgs_config)]

    # WHEN invoking snakemake module with dryrun option
    # THEN it should return true
    with mock.patch.dict(
        MOCKED_OS_ENVIRON,
        {
            "SENTIEON_LICENSE": sentieon_license,
            "SENTIEON_INSTALL_DIR": sentieon_install_dir,
        },
    ):
        for workflow in workflows:
            analysis_type = workflow[0]
            config = workflow[1]
            reference_genome = "hg19"
            analysis_workflow = "balsamic"
            snakefile = get_snakefile(
                analysis_type, analysis_workflow, reference_genome
            )
            assert snakemake.snakemake(snakefile, configfiles=[config], dryrun=True)
