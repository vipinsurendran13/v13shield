"""
Minimal, dependency-free VCF parser.
Handles standard VCF v4.x text files (plain or gzipped).
We don't need a full library here -- we only need to pull out
CHROM, POS, REF, ALT, and per-sample genotype (GT) for a small,
known list of positions. Keeping this dependency-free keeps the
final Docker image small and avoids compilation headaches.
"""
import gzip
import sys


def _open_vcf(path):
    if path.endswith(".gz"):
        return gzip.open(path, "rt")
    return open(path, "rt")


def parse_vcf(path):
    """
    Yields dicts: {chrom, pos, id, ref, alt, genotypes: {sample_name: gt_string}}
    ALT with multiple values (comma-separated) is split into separate records,
    one per alt allele, keeping the same genotype field for reference.
    """
    samples = []
    with _open_vcf(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            if line.startswith("##"):
                continue
            if line.startswith("#CHROM"):
                fields = line.split("\t")
                samples = fields[9:] if len(fields) > 9 else []
                continue

            fields = line.split("\t")
            if len(fields) < 8:
                continue

            chrom, pos, vid, ref, alt_field = fields[0:5]
            # normalize chrom naming (some VCFs omit 'chr' prefix)
            if not chrom.startswith("chr"):
                chrom = "chr" + chrom

            genotypes = {}
            if len(fields) > 9:
                format_keys = fields[8].split(":")
                gt_index = format_keys.index("GT") if "GT" in format_keys else 0
                for sample_name, sample_data in zip(samples, fields[9:]):
                    sample_vals = sample_data.split(":")
                    gt = sample_vals[gt_index] if gt_index < len(sample_vals) else "./."
                    genotypes[sample_name] = gt

            for alt in alt_field.split(","):
                yield {
                    "chrom": chrom,
                    "pos": int(pos),
                    "id": vid,
                    "ref": ref,
                    "alt": alt,
                    "genotypes": genotypes,
                }


def genotype_is_variant(gt_string):
    """
    Returns 'het', 'hom_alt', or 'ref' based on a GT string like '0/1', '1|1', '0/0'.
    Treats any non-zero, non-missing allele as the alt allele of interest
    (fine for our single-alt-per-record use case after splitting multi-allelics).
    """
    if not gt_string or gt_string in (".", "./.", ".|."):
        return "missing"
    sep = "/" if "/" in gt_string else "|"
    alleles = gt_string.split(sep)
    try:
        alleles = [a for a in alleles if a != "."]
        vals = [int(a) for a in alleles]
    except ValueError:
        return "missing"
    if not vals:
        return "missing"
    if all(v == 0 for v in vals):
        return "ref"
    if len(vals) >= 2 and all(v > 0 for v in vals):
        return "hom_alt"
    return "het"


if __name__ == "__main__":
    # quick self-test when run directly
    for rec in parse_vcf(sys.argv[1]):
        print(rec)
