#!/usr/bin/env python3
"""
V13Shield
Screens a patient's germline VCF for known CPIC pharmacogene variants
associated with severe chemotherapy toxicity risk.
Created by Vipin.

Usage:
    python3 main.py --input patient.vcf --outdir results/
    python3 main.py --test --outdir results/     (runs on bundled synthetic sample)
"""
import argparse
import os
import sys
import json

from analyze import load_pgx_database, analyze_vcf
from report import generate_report

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "pgx_variants.json")
TEST_VCF_PATH = os.path.join(os.path.dirname(__file__), "..", "test_data", "sample_patient.vcf")


def main():
    parser = argparse.ArgumentParser(
        description="V13Shield -- screens germline VCF for CPIC pharmacogene toxicity risk variants."
    )
    parser.add_argument("--input", help="Path to input VCF file (.vcf or .vcf.gz)")
    parser.add_argument("--outdir", default="results", help="Output directory for the report (default: results/)")
    parser.add_argument("--test", action="store_true", help="Run on the bundled synthetic test sample instead of real data")
    parser.add_argument("--json", action="store_true", help="Also write raw findings as JSON")
    args = parser.parse_args()

    if not args.input and not args.test:
        print("ERROR: You must provide --input <file.vcf> or use --test to run on sample data.", file=sys.stderr)
        sys.exit(1)

    vcf_path = TEST_VCF_PATH if args.test else args.input

    if not os.path.exists(vcf_path):
        print(f"ERROR: Input VCF not found at: {vcf_path}", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(DB_PATH):
        print(f"ERROR: Pharmacogene database not found at: {DB_PATH}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(args.outdir, exist_ok=True)

    print(f"[1/4] Loading pharmacogene knowledge base ({DB_PATH}) ...")
    db = load_pgx_database(DB_PATH)
    print(f"      Database version: {db['_meta']['version']}")

    print(f"[2/4] Scanning VCF: {vcf_path} ...")
    result = analyze_vcf(vcf_path, db)
    print(f"      Scanned {result['total_variants_scanned']} variant records.")
    print(f"      Found {len(result['findings'])} known risk variant(s).")

    print("[3/4] Generating plot and report ...")
    report_path = os.path.join(args.outdir, "chemo_tox_report.html")
    generate_report(result, report_path)

    if args.json:
        json_path = os.path.join(args.outdir, "chemo_tox_findings.json")
        with open(json_path, "w") as f:
            json.dump(result, f, indent=2)
        print(f"      Raw findings JSON: {json_path}")

    print(f"[4/4] Done. Report saved to: {report_path}")
    print()
    print(result["disclaimer"])


if __name__ == "__main__":
    main()
