# Define set of rules
SNAKEMAKE_RULES = {
    "common": {
        "qc": [
            "snakemake_rules/quality_control/fastp.rule",
            "snakemake_rules/quality_control/fastqc.rule",
            "snakemake_rules/quality_control/multiqc.rule",
            "snakemake_rules/variant_calling/mergetype_tumor.rule",
        ],
        "align": [],
        "varcall": ["snakemake_rules/variant_calling/germline_sv.rule"],
        "annotate": ["snakemake_rules/annotation/vep.rule"],
    },
    "single_targeted": {
        "qc": [
            "snakemake_rules/quality_control/GATK.rule",
            "snakemake_rules/quality_control/picard.rule",
            "snakemake_rules/quality_control/sambamba_depth.rule",
            "snakemake_rules/quality_control/mosdepth.rule",
            "snakemake_rules/umi/qc_umi.rule",
            "snakemake_rules/umi/mergetype_tumor_umi.rule",
            "snakemake_rules/umi/generate_AF_tables.rule",
        ],
        "align": [
            "snakemake_rules/align/bwa_mem.rule",
            "snakemake_rules/umi/sentieon_umiextract.rule",
            "snakemake_rules/umi/sentieon_consensuscall.rule",
        ],
        "varcall": [
            "snakemake_rules/variant_calling/germline.rule",
            "snakemake_rules/variant_calling/split_bed.rule",
            "snakemake_rules/variant_calling/cnvkit_single.rule",
            "snakemake_rules/variant_calling/somatic_tumor_only.rule",
            "snakemake_rules/variant_calling/somatic_sv_tumor_only.rule",
            "snakemake_rules/umi/sentieon_varcall_tnscope.rule",
        ],
        "annotate": [
            "snakemake_rules/annotation/rankscore.rule",
            "snakemake_rules/annotation/varcaller_sv_filter.rule",
            "snakemake_rules/annotation/varcaller_filter_tumor_only.rule",
        ],
    },
    "paired_targeted": {
        "qc": [
            "snakemake_rules/quality_control/GATK.rule",
            "snakemake_rules/quality_control/picard.rule",
            "snakemake_rules/quality_control/sambamba_depth.rule",
            "snakemake_rules/quality_control/mosdepth.rule",
            "snakemake_rules/umi/qc_umi.rule",
            "snakemake_rules/variant_calling/mergetype_normal.rule",
            "snakemake_rules/umi/mergetype_tumor_umi.rule",
            "snakemake_rules/umi/mergetype_normal_umi.rule",
            "snakemake_rules/quality_control/contest.rule",
            "snakemake_rules/umi/generate_AF_tables.rule",
        ],
        "align": [
            "snakemake_rules/align/bwa_mem.rule",
            "snakemake_rules/umi/sentieon_umiextract.rule",
            "snakemake_rules/umi/sentieon_consensuscall.rule",
        ],
        "varcall": [
            "snakemake_rules/variant_calling/germline.rule",
            "snakemake_rules/variant_calling/split_bed.rule",
            "snakemake_rules/variant_calling/somatic_tumor_normal.rule",
            "snakemake_rules/variant_calling/somatic_sv_tumor_normal.rule",
            "snakemake_rules/variant_calling/cnvkit_paired.rule",
            "snakemake_rules/umi/sentieon_varcall_tnscope_tn.rule",
        ],
        "annotate": [
            "snakemake_rules/annotation/rankscore.rule",
            "snakemake_rules/annotation/varcaller_sv_filter.rule",
            "snakemake_rules/annotation/varcaller_filter_tumor_normal.rule",
        ],
    },
    "single_wgs": {
        "qc": [
            "snakemake_rules/quality_control/sentieon_qc_metrics.rule",
            "snakemake_rules/quality_control/picard_wgs.rule",
        ],
        "align": ["snakemake_rules/align/sentieon_alignment.rule"],
        "varcall": [
            "snakemake_rules/variant_calling/sentieon_germline.rule",
            "snakemake_rules/variant_calling/sentieon_split_snv_sv.rule",
            "snakemake_rules/variant_calling/sentieon_t_varcall.rule",
            "snakemake_rules/variant_calling/somatic_sv_tumor_only.rule",
            "snakemake_rules/dragen_suite/dragen_dna.rule",
        ],
        "annotate": [
            "snakemake_rules/annotation/varcaller_wgs_filter_tumor_only.rule",
            "snakemake_rules/annotation/varcaller_sv_wgs_filter_tumor_only.rule",
        ],
    },
    "paired_wgs": {
        "qc": [
            "snakemake_rules/quality_control/sentieon_qc_metrics.rule",
            "snakemake_rules/quality_control/picard_wgs.rule",
            "snakemake_rules/variant_calling/mergetype_normal.rule",
        ],
        "align": ["snakemake_rules/align/sentieon_alignment.rule"],
        "varcall": [
            "snakemake_rules/variant_calling/sentieon_germline.rule",
            "snakemake_rules/variant_calling/sentieon_split_snv_sv.rule",
            "snakemake_rules/variant_calling/sentieon_tn_varcall.rule",
            "snakemake_rules/variant_calling/somatic_sv_tumor_normal.rule",
        ],
        "annotate": [
            "snakemake_rules/annotation/varcaller_wgs_filter_tumor_normal.rule",
            "snakemake_rules/annotation/varcaller_sv_wgs_filter_tumor_normal.rule",
        ],
    },
}


DELIVERY_RULES = [
    "fastp",
    "multiqc",
    "vep_somatic",
    "vep_germline",
    "tmb_calculation",
    "bcftools_filter_TNscope_umi_tumor_only",
    "bcftools_filter_TNscope_umi_tumor_normal",
    "bcftools_filter_vardict_tumor_only",
    "bcftools_filter_vardict_tumor_normal",
    "bcftools_filter_tnscope_tumor_only",
    "bcftools_filter_tnscope_tumor_normal",
    "bcftools_filter_tnhaplotyper_tumor_only",
    "bcftools_filter_tnhaplotyper_tumor_normal",
    "bcftools_filter_manta",
    "bcftools_filter_delly",
    "bcftools_filter_ascat",
    "bcftools_filter_cnvkit",
    "bcftools_intersect_tumor_only",
    "bcftools_filter_TNscope_umi_tumor_only",
    "genmod_score_vardict",
    "mergeBam_tumor",
    "mergeBam_normal",
    "cnvkit_paired",
    "cnvkit_single",
]
