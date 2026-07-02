"""
Core analysis logic for the Chemo Toxicity Risk Checker.

Takes a patient VCF, checks it against known CPIC pharmacogene variants,
and produces a structured result (risk per gene/drug) ready for reporting.
"""
import json
from vcf_parser import parse_vcf, genotype_is_variant


def load_pgx_database(json_path):
    with open(json_path) as f:
        return json.load(f)


def build_lookup_index(pgx_db):
    """
    Build a fast lookup: (chrom, pos, ref, alt) -> variant metadata (with gene context attached)
    """
    index = {}
    for gene_entry in pgx_db["genes"]:
        for variant in gene_entry["variants"]:
            key = (variant["chrom"], variant["pos_hg38"], variant["ref"], variant["alt"])
            index[key] = {
                **variant,
                "gene": gene_entry["gene"],
                "drug_class": gene_entry["drug_class"],
                "drugs": gene_entry["drugs"],
                "risk_summary": gene_entry["risk_summary"],
            }
    return index


def analyze_vcf(vcf_path, pgx_db):
    """
    Returns a list of findings, one per matched risk variant found in the sample,
    plus a summary of which genes/drugs are affected.
    """
    lookup = build_lookup_index(pgx_db)
    findings = []
    total_variants_scanned = 0

    for rec in parse_vcf(vcf_path):
        total_variants_scanned += 1
        key = (rec["chrom"], rec["pos"], rec["ref"], rec["alt"])
        if key not in lookup:
            continue

        variant_info = lookup[key]
        # look at the first sample's genotype (single-sample VCF assumed for v1)
        genotypes = rec["genotypes"]
        if not genotypes:
            continue
        sample_name = list(genotypes.keys())[0]
        gt_string = genotypes[sample_name]
        zygosity = genotype_is_variant(gt_string)

        if zygosity in ("het", "hom_alt"):
            findings.append({
                "sample": sample_name,
                "gene": variant_info["gene"],
                "star_allele": variant_info["star_allele"],
                "rsid": variant_info["rsid"],
                "drug_class": variant_info["drug_class"],
                "drugs": variant_info["drugs"],
                "zygosity": zygosity,
                "activity": variant_info["activity"],
                "effect": variant_info["effect"],
                "risk_summary": variant_info["risk_summary"],
                "genotype_raw": gt_string,
            })

    return {
        "total_variants_scanned": total_variants_scanned,
        "findings": findings,
        "db_version": pgx_db["_meta"]["version"],
        "disclaimer": pgx_db["_meta"]["disclaimer"],
    }


def classify_overall_risk(findings):
    """
    Simple, transparent risk tiering per gene based on zygosity + activity.
    Homozygous 'no function' = High risk. Heterozygous or 'decreased function' = Moderate.
    This mirrors (simplified) CPIC phenotype logic -- NOT a replacement for full
    diplotype/phenotype calling, which requires more complete variant coverage.
    """
    gene_risk = {}
    for f in findings:
        gene = f["gene"]
        if f["zygosity"] == "hom_alt" and f["activity"] == "no function":
            tier = "High risk"
        elif f["zygosity"] == "hom_alt":
            tier = "Moderate-High risk"
        elif f["zygosity"] == "het" and f["activity"] == "no function":
            tier = "Moderate risk"
        else:
            tier = "Low-Moderate risk"

        # keep the highest risk tier seen per gene
        order = {"Low-Moderate risk": 1, "Moderate risk": 2, "Moderate-High risk": 3, "High risk": 4}
        if gene not in gene_risk or order[tier] > order[gene_risk[gene]]:
            gene_risk[gene] = tier

    return gene_risk
