"""Description of the Balsamic package."""
import os
from typing import List

from setuptools import setup, find_packages

NAME: str = "BALSAMIC"
AUTHOR: str = "Clinical Genomics"
URL: str = "https://github.com/Clinical-Genomics/BALSAMIC"
EMAIL: str = "support@clinicalgenomics.se"
REQUIRES_PYTHON: str = ">=3.11.0"

# Requirements
requirements: List[str] = [
    "aiohttp==3.8.5",
    "aiosignal==1.3.1",
    "appdirs==1.4.4",
    "argcomplete==3.1.1",
    "async-timeout==4.0.2",
    "attrs==23.1.0",
    "boto==2.49.0",
    "cachetools==5.3.1",
    "certifi==2023.7.22",
    "cffi==1.15.1",
    "charset-normalizer==3.2.0",
    "click==8.1.6",
    "colorclass==2.2.2",
    "coloredlogs==15.0.1",
    "ConfigArgParse==1.7",
    "connection-pool==0.0.3",
    "contourpy==1.1.0",
    "crcmod==1.7",
    "cryptography==41.0.3",
    "cycler==0.11.0",
    "cyvcf2==0.30.22",
    "datrie==0.8.2",
    "defusedxml==0.7.1",
    "dpath==2.1.6",
    "fasteners==0.18",
    "fastjsonschema==2.18.0",
    "fonttools==4.42.0",
    "fpdf2==2.7.4",
    "frozenlist==1.4.0",
    "gcs-oauth2-boto-plugin==3.0",
    "gitdb==4.0.10",
    "GitPython==3.1.32",
    "google-apitools==0.5.32",
    "google-auth==2.22.0",
    "google-reauth==0.1.1",
    "graphviz==0.20.1",
    "gsutil==5.25",
    "h5py==3.9.0",
    "httplib2==0.20.4",
    "humanfriendly==10.0",
    "idna==3.4",
    "importlib-metadata==6.8.0",
    "iniconfig==2.0.0",
    "Jinja2==3.1.2",
    "jsonschema==4.18.6",
    "jsonschema-specifications==2023.7.1",
    "jupyter_core==5.3.1",
    "kiwisolver==1.4.4",
    "MarkupSafe==2.1.3",
    "matplotlib==3.7.2",
    "monotonic==1.6",
    "multidict==6.0.4",
    "nbformat==5.9.2",
    "numpy==1.25.2",
    "oauth2client==4.1.3",
    "packaging==23.1",
    "pandas==2.0.3",
    "Pillow==10.0.0",
    "plac==1.3.5",
    "platformdirs==3.10.0",
    "pluggy==1.2.0",
    "psutil==5.9.5",
    "PuLP==2.7.0",
    "pyasn1==0.5.0",
    "pyasn1-modules==0.3.0",
    "pycparser==2.21",
    "pydantic==1.10.12",
    "Pygments==2.15.1",
    "pyOpenSSL==23.2.0",
    "pyparsing==3.0.9",
    "PyPDF2==3.0.1",
    "pytest==7.4.0",
    "python-dateutil==2.8.2",
    "pytz==2023.3",
    "pyu2f==0.1.5",
    "PyYAML==6.0.1",
    "referencing==0.30.0",
    "requests==2.31.0",
    "reretry==0.11.8",
    "retry-decorator==1.1.1",
    "rpds-py==0.9.2",
    "rsa==4.7.2",
    "six==1.16.0",
    "smart-open==6.3.0",
    "smmap==5.0.0",
    "snakemake==7.32.0",
    "stopit==1.1.2",
    "tabulate==0.9.0",
    "throttler==1.2.2",
    "toml==0.10.2",
    "tomli==2.0.1",
    "toposort==1.10",
    "traitlets==5.9.0",
    "typing_extensions==4.7.1",
    "tzdata==2023.3",
    "urllib3==1.26.16",
    "wrapt==1.15.0",
    "yapf==0.40.1",
    "yarl==1.9.2",
    "yte==1.5.1",
    "zipp==3.16.2",
]

# The C libraries required to build numpy are not available on RTD
if not os.getenv("READTHEDOCS"):
    requirements.extend(["cyvcf2==0.30.22"])

setup(
    name=NAME,
    version="12.0.2",
    url=URL,
    author=AUTHOR,
    author_email=EMAIL,
    install_requires=requirements,
    python_requires=REQUIRES_PYTHON,
    packages=find_packages(),
    package_data={
        "": [
            "*.toml",
            "*.json",
            "*.R",
            "*.model",
            "*.yaml",
            "*.sh",
            "*.rule",
            "*.smk",
            "*.awk",
            "*.html",
            "*.md",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": ["balsamic=BALSAMIC.commands.base:cli"],
    },
)
