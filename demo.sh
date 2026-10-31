#!/bin/bash
set -e
source venv/bin/activate
echo "== 1. Simulate attacks =="
python simulator/run_all.py
echo
echo "== 2. Detect =="
python detector/run_all.py
echo
echo "== 3. Remediate =="
python remediator/run_all.py
echo
echo "== 4. Launch dashboard =="
streamlit run dashboard/app.py --server.port 8501
