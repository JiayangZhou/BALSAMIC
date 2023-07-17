"""Balsamic analysis workflow constants."""
from typing import Dict

from BALSAMIC.constants.cache import DockerContainers
from BALSAMIC.utils.class_types import StrEnum


class Gender(StrEnum):
    """Sex options."""

    FEMALE: str = "female"
    MALE: str = "male"


class AnalysisType(StrEnum):
    """Supported analysis types."""

    PAIRED: str = "paired"
    PON: str = "pon"
    SINGLE: str = "single"


class AnalysisWorkflow(StrEnum):
    """Available Balsamic workflows."""

    BALSAMIC: str = "balsamic"
    BALSAMIC_QC: str = "balsamic-qc"
    BALSAMIC_UMI: str = "balsamic-umi"


class SequencingType(StrEnum):
    """Sequencing carried out."""

    TARGETED: str = "targeted"
    WGS: str = "wgs"


class SampleType(StrEnum):
    """Balsamic sample type inputs."""

    NORMAL: str = "normal"
    TUMOR: str = "tumor"


class MutationOrigin(StrEnum):
    """Variations present in a sample."""

    GERMLINE: str = "germline"
    SOMATIC: str = "somatic"


class MutationType(StrEnum):
    """Types of variations present in a sample."""

    CNV: str = "CNV"
    SNV: str = "SNV"
    SV: str = "SV"


class WorkflowSolution(StrEnum):
    """Solution applied to a specific part of the analysis."""

    BALSAMIC: str = "BALSAMIC"
    DRAGEN: str = "DRAGEN"
    SENTIEON: str = "Sentieon"
    SENTIEON_UMI: str = "Sentieon_umi"


class BioinfoTools(StrEnum):
    """List of bioinformatics tools in Balsamic."""

    ASCAT: str = "ascatNgs"
    BCFTOOLS: str = "bcftools"
    BEDTOOLS: str = "bedtools"
    BGZIP: str = "bgzip"
    BWA: str = "bwa"
    CNVKIT: str = "cnvkit"
    CNVPYTOR: str = "cnvpytor"
    CSVKIT: str = "csvkit"
    DELLY: str = "delly"
    VEP: str = "ensembl-vep"
    FASTP: str = "fastp"
    FASTQC: str = "fastqc"
    GATK: str = "gatk"
    GENMOD: str = "genmod"
    MANTA: str = "manta"
    MOSDEPTH: str = "mosdepth"
    MULTIQC: str = "multiqc"
    PICARD: str = "picard"
    SAMBAMBA: str = "sambamba"
    SAMTOOLS: str = "samtools"
    SOMALIER: str = "somalier"
    SVDB: str = "svdb"
    TABIX: str = "tabix"
    TIDDIT: str = "tiddit"
    VARDICT: str = "vardict"
    VCF2CYTOSURE: str = "vcf2cytosure"
    VCFANNO: str = "vcfanno"


BIOINFO_TOOL_ENV: Dict[str, str] = {
    BioinfoTools.BEDTOOLS.value: DockerContainers.ALIGN_QC.value,
    BioinfoTools.BWA.value: DockerContainers.ALIGN_QC.value,
    BioinfoTools.FASTQC.value: DockerContainers.ALIGN_QC.value,
    BioinfoTools.SAMTOOLS.value: DockerContainers.ALIGN_QC.value,
    BioinfoTools.PICARD.value: DockerContainers.ALIGN_QC.value,
    BioinfoTools.MULTIQC.value: DockerContainers.ALIGN_QC.value,
    BioinfoTools.FASTP.value: DockerContainers.ALIGN_QC.value,
    BioinfoTools.CSVKIT.value: DockerContainers.ALIGN_QC.value,
    BioinfoTools.VEP.value: DockerContainers.ANNOTATE.value,
    BioinfoTools.GENMOD.value: DockerContainers.ANNOTATE.value,
    BioinfoTools.VCFANNO.value: DockerContainers.ANNOTATE.value,
    BioinfoTools.SAMBAMBA.value: DockerContainers.COVERAGE_QC.value,
    BioinfoTools.MOSDEPTH.value: DockerContainers.COVERAGE_QC.value,
    BioinfoTools.BCFTOOLS.value: DockerContainers.PYTHON_3.value,
    BioinfoTools.TABIX.value: DockerContainers.PYTHON_3.value,
    BioinfoTools.BGZIP.value: DockerContainers.PYTHON_3.value,
    BioinfoTools.GATK.value: DockerContainers.PYTHON_3.value,
    BioinfoTools.VARDICT.value: DockerContainers.PYTHON_3.value,
    BioinfoTools.SVDB.value: DockerContainers.PYTHON_3.value,
    BioinfoTools.TIDDIT.value: DockerContainers.PYTHON_3.value,
    BioinfoTools.CNVPYTOR.value: DockerContainers.CNVPYTOR.value,
    BioinfoTools.MANTA.value: DockerContainers.PYTHON_27.value,
    BioinfoTools.CNVKIT.value: DockerContainers.CNVKIT.value,
    BioinfoTools.DELLY.value: DockerContainers.DELLY.value,
    BioinfoTools.ASCAT.value: DockerContainers.ASCAT.value,
    BioinfoTools.VCF2CYTOSURE.value: DockerContainers.VCF2CYTOSURE.value,
    BioinfoTools.SOMALIER.value: DockerContainers.SOMALIER.value,
}
