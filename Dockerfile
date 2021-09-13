FROM continuumio/miniconda3:4.9.2-alpine

LABEL base_image="continuumio/miniconda3:4.9.2-alpine"
LABEL about.home="https://github.com/Clinical-Genomics/BALSAMIC"
LABEL about.documentation="https://balsamic.readthedocs.io/"
LABEL about.license="MIT License (MIT)"
LABEL about.maintainer="Hassan Foroughi hassan dot foroughi at scilifelab dot se" 
LABEL about.description="Bioinformatic analysis pipeline for somatic mutations in cancer"
LABEL about.version="8.1.0"

ENV PATH="/opt/conda/bin/:${PATH}"
ENV MUSL_LOCPATH="/usr/share/i18n/locales/musl"
ENV LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8

RUN apk add --no-cache bash gcc git zlib-dev musl-dev libintl

# Locale installation
RUN apk add --no-cache --virtual .locale_tmp cmake make gettext-dev && \
    git clone https://gitlab.com/rilian-la-te/musl-locales && \
    cd musl-locales && cmake -DLOCALE_PROFILE=OFF -DCMAKE_INSTALL_PREFIX:PATH=/usr . && make && make install && \
    cd .. && rm -r musl-locales && \
    apk del .locale_tmp

ARG WORK_DIR=project
ARG CONTAINER_NAME

# Copy all project files
COPY . /${WORK_DIR}

RUN cd /${WORK_DIR}/BALSAMIC/containers/${CONTAINER_NAME}/ && /bin/sh ${CONTAINER_NAME}.sh ${CONTAINER_NAME}
RUN if [ "$CONTAINER_NAME" = "balsamic" ]; then cd /project && pip install --no-cache-dir . ; fi

# Clean work environment
RUN rm -rf /project && conda clean --all --yes
