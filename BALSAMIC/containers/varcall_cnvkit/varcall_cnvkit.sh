conda env update -n base --file ${1}.yaml --prune
pip install --upgrade --no-cache-dir cnvkit==0.9.4 biopython==1.76
