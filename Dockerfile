# V13Shield
# A lightweight, dependency-minimal tool for screening germline VCFs
# against known CPIC pharmacogene toxicity-risk variants.
# Created by Vipin surendra kumar.

FROM mambaorg/micromamba:1.5-jammy

LABEL org.opencontainers.image.title="V13Shield"
LABEL org.opencontainers.image.description="Screens germline VCF files for CPIC pharmacogene variants linked to severe chemotherapy toxicity risk (DPYD, TPMT, NUDT15, UGT1A1)."
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.authors="Vipin surendra kumar"
LABEL org.opencontainers.image.classification="Research Use Only (RUO) / Clinical Decision Support Framework"
LABEL org.opencontainers.image.source="https://github.com/vipin13/v13shield"

USER root

# Install only what we need: pandas, matplotlib, jinja2 (no compiled VCF libs needed --
# our parser is pure Python, keeping this image small and build-fast)
RUN micromamba install -y -n base -c conda-forge \
        python=3.12 \
        pandas \
        matplotlib \
        jinja2 \
        pillow \
    && micromamba clean --all --yes

# Create non-root user for running the tool
RUN useradd -m -u 1000 tooluser
WORKDIR /app

# Ensure LICENSE is copied into the container root directory for distribution compliance
COPY --chown=tooluser:tooluser LICENSE /app/LICENSE
COPY --chown=tooluser:tooluser scripts/ /app/scripts/
COPY --chown=tooluser:tooluser data/ /app/data/
COPY --chown=tooluser:tooluser test_data/ /app/test_data/

USER tooluser

ENV MAMBA_ROOT_PREFIX=/opt/conda
ENV PATH="/opt/conda/bin:$PATH"

ENTRYPOINT ["python3", "/app/scripts/main.py"]
CMD ["--help"]
