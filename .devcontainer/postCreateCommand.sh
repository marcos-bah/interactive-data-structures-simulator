#!/usr/bin/env bash
set -euo pipefail

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release -j"$(nproc)"

echo "Ambiente pronto. Execute: streamlit run app.py --server.address 0.0.0.0 --server.port 8501"
