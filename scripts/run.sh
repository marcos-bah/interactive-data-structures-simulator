#!/usr/bin/env bash
set -euo pipefail

if ! find build -maxdepth 1 -type f \( -name 'ds_core*.so' -o -name 'ds_core*.pyd' \) | grep -q .; then
  bash scripts/build.sh
fi

streamlit run app.py --server.address 0.0.0.0 --server.port 8501
