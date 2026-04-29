import streamlit as st
from src.ats_engine import (
    fit_ats_model,
    rank_baseline_candidates,
    run_single_inference,
    run_batch_inference,
)

st.set_page_config(page_title="Mini ATS", layout="wide")
st.title("Mini ATS - Resume Screening and Ranking System")

model_state = fit_ats_model(
    cv_folder="data/baseline_cvs",
    jd_path="data/job_description.txt"
)

st.subheader("Baseline Candidate Ranking")
baseline_df = rank_baseline_candidates(model_state)
st.dataframe(baseline_df, use_container_width=True)

st.subheader("Single CV Inference")
single_file = st.file_uploader("Upload one CV (.txt)", type=["txt"], key="single")
if single_file:
    single_result = run_single_inference(single_file, model_state)
    st.dataframe(single_result, use_container_width=True)

st.subheader("Batch CV Inference")
batch_files = st.file_uploader("Upload multiple CVs (.txt)", type=["txt"], accept_multiple_files=True, key="batch")
if batch_files:
    batch_result = run_batch_inference(batch_files, model_state)
    st.dataframe(batch_result, use_container_width=True)

