import json, streamlit as st
from pathlib import Path

st.set_page_config(page_title="SupplyGuard", layout="wide")
st.title("🛡️ SupplyGuard — CI/CD Supply Chain Security")

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"

def load(name, default):
    p = REPORTS / name
    if p.exists():
        return json.loads(p.read_text())
    return default

col1, col2, col3 = st.columns(3)

sim = load("simulation.json", {})
det = load("findings.json", {"sbom_diff": {"added": []}, "policy_denials": [], "risk_score": 0})
rem = load("remediation.json", {"fixes": []})

col1.metric("Attacks Simulated", len(sim))
col2.metric("Findings", len(det.get("sbom_diff", {}).get("added", [])) + len(det.get("policy_denials", [])))
col3.metric("Risk Score", det.get("risk_score", 0))

st.divider()

st.subheader("1️⃣ Simulated Attacks")
st.json(sim)

st.subheader("2️⃣ Detections")
st.json(det)

st.subheader("3️⃣ Auto-Remediation")
st.json(rem)

st.divider()
st.caption("Flow: simulate → detect → remediate")
