conda env update -n base --file ${1}.yaml --prune
pip install --no-cache-dir genmod==3.7.4
