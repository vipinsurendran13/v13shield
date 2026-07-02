# V13Shield

**Version:** 1.0.0<br>
**Updated:** 01 July 2026<br>
**Author:** Vipin Surendra Kumar<br>
**Language:** Python 3<br>
**Containerisation:** Docker • Singularity • Apptainer<br>
**Sif image:** https://hub.docker.com/r/vipinsurendran13/v13shield
---

# Table of Contents

1. Overview
2. Motivation
3. Key Features
4. Workflow
5. Installation
6. Quick Start
7. Input Format
8. Pharmacogenes Supported
9. Risk Classification
10. Output Files
11. Docker Usage
12. Singularity / Apptainer Usage
13. Directory Structure
14. Future Development
15. Disclaimer
16. Citation

---

# Overview

**V13Shield** is an open-source pharmacogenomics screening tool that identifies inherited variants associated with chemotherapy toxicity from VCF files.

The tool screens clinically important pharmacogenes using curated CPIC guideline variants and generates an easy-to-understand HTML report containing toxicity warnings, visualizations, and treatment recommendations.

The primary objective of V13Shield is to help researchers and clinicians identify patients who may be at increased risk of severe chemotherapy toxicity before treatment begins.

---

# Motivation

Many chemotherapy drugs can cause life-threatening adverse reactions in patients carrying specific inherited genetic variants.

Although international pharmacogenomic guidelines exist, screening is not routinely performed in many laboratories due to workflow complexity.

V13Shield provides a simple, reproducible, containerized solution that enables rapid toxicity screening using existing VCF files.

---

# Key Features

✔ Reads standard VCF files

✔ Screens clinically validated pharmacogenes

✔ CPIC guideline based interpretation

✔ Interactive HTML report

✔ Publication-quality plots

✔ JSON output for downstream analysis

✔ Lightweight Python implementation

✔ Docker compatible

✔ Singularity / Apptainer compatible

✔ Completely offline analysis

---

# Workflow

```
               Patient VCF
                    │
                    ▼
          Variant Identification
                    │
                    ▼
        Pharmacogene Screening
     (DPYD • TPMT • NUDT15 • UGT1A1)
                    │
                    ▼
       Clinical Risk Classification
                    │
                    ▼
      Plot Generation & HTML Report
                    │
                    ▼
          Final Toxicity Report
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/<username>/V13Shield.git

cd V13Shield
```

---

## Python Requirements

```
Python >=3.10
matplotlib
pandas
jinja2
```

Install

```bash
pip install pandas matplotlib jinja2
```

---

# Quick Start

Run using built-in test dataset

```bash
python scripts/main.py \
    --test \
    --outdir results \
    --json
```

Run using your own VCF

```bash
python scripts/main.py \
    --input patient.vcf \
    --outdir results \
    --json
```

---

# Input Format

Accepted input

* Standard VCF v4.x

Required information

* Chromosome
* Position
* REF allele
* ALT allele
* Genotype

Example

```
chr1    970448  .  C  T
```

---

# Pharmacogenes Supported

| Gene | Drug | Clinical Effect |
|------|------|-----------------|
| DPYD | 5-FU / Capecitabine | Severe toxicity |
| TPMT | Thiopurines | Myelosuppression |
| NUDT15 | Thiopurines | Leukopenia |
| UGT1A1 | Irinotecan | Neutropenia |

---

# Risk Classification

| Risk Level | Description |
|------------|-------------|
| Low | Normal drug metabolism |
| Moderate | Dose adjustment may be required |
| High | High toxicity risk |

---

# Output Files

```
results/

├── chemo_tox_report.html
├── chemo_tox_findings.json
├── toxicity_plot.png
```

---

# Docker Usage

Build image

```bash
docker build -t vipin13/v13shield:v1.0 .
```

Run

```bash
docker run --rm \
-v $(pwd)/results:/app/scripts/results \
vipin13/v13shield:v1.0 \
--test \
--outdir results
```

---

# Singularity / Apptainer

Pull image

```bash
singularity pull docker://vipin13/v13shield:v1.0
```

or

```bash
apptainer pull docker://vipin13/v13shield:v1.0
```

Run

```bash
singularity run v13shield.sif \
--test \
--outdir results
```

---

# Directory Structure

```
V13Shield/

├── data/
│   └── pgx_variants.json
│
├── scripts/
│   ├── main.py
│   ├── analyze.py
│   ├── report.py
│   └── vcf_parser.py
│
├── test_data/
│   └── sample_patient.vcf
│
├── results/
│
├── Dockerfile
│
└── README.md
```


# Legal, Regulatory & Privacy Notice 

1. Regulatory Status Designation

V13Shield is classified strictly as Research Use Only (RUO) software and a computational Clinical Decision Support (CDS) framework. It is not cleared, approved, or certified as an active diagnostic medical device by the United States Food and Drug Administration (FDA), European CE-IVD, India's Central Drugs Standard Control Organisation (CDSCO), or any national medical authority.
2. Liability and Clinical Limitation Statement

This application performs computational matching against automated database captures of public domain scientific guidelines. It does not constitute medical advice or diagnostic verification. All high-risk alerts generated by this framework must be independently confirmed via targeted certified laboratory assays. Any modifications to active oncology treatments or patient drug dosing ranges must be explicitly reviewed and managed by a licensed oncologist or qualified clinical pharmacist.
3. Patient Privacy and Sovereign Compliance (HIPAA / GDPR / DPDP Act)

To protect patient data privacy, V13Shield functions with a fully isolated local execution protocol. The script stack contains zero internet telemetry, tracking pixels, external API calls, or cloud database syncs. It never transmits, views, or collects Personal Health Information (PHI) or raw genomic files across the open web, ensuring complete compliance with global privacy mandates.

---

# Future Development

- Additional CPIC pharmacogenes
- Multi-sample analysis
- PDF report generation
- Automatic database updates
- CNV support
- STAR allele detection
- Clinical decision support
- Multi-language reports

---

# Disclaimer

V13Shield is intended for **research purposes only**.

This software is **not a medical device** and must **not** be used as the sole basis for clinical decision-making.

All findings should be confirmed by certified clinical pharmacogenomics laboratories and interpreted by qualified healthcare professionals.

---

# Citation

Vipin Surendra Kumar

V13Shield: A Containerized Pharmacogenomics Tool for Chemotherapy Toxicity Screening

Version 1.0.0

2026
