import streamlit as st
from src.ats_engine import fit_ats_model, run_single_inference, run_batch_inference

st.set_page_config(page_title="Mini ATS", layout="wide")
st.title("Mini ATS - Resume Screening and Ranking System")

@st.cache_resource
def load_model():
    return fit_ats_model("data/baseline_cvs", "data/job_description.txt")

model = load_model()

tab1, tab2, tab3 = st.tabs(["Baseline Ranking", "Single CV Inference", "Batch CV Inference"])

with tab1:
    st.subheader("Original 40 Candidates Ranking")
    st.dataframe(model.baseline_df, use_container_width=True)
    st.download_button(
        "Download Baseline Ranking CSV",
        model.baseline_df.to_csv(index=False).encode("utf-8"),
        file_name="baseline_ranking.csv",
        mime="text/csv",
    )

with tab2:
    st.subheader("Upload One New CV")
    single_file = st.file_uploader("Upload a single .txt CV", type=["txt"], key="single")
    if single_file is not None:
        single_result = run_single_inference(single_file, model)
        st.dataframe(single_result, use_container_width=True)
        st.download_button(
            "Download Single Inference CSV",
            single_result.to_csv(index=False).encode("utf-8"),
            file_name="single_inference_result.csv",
            mime="text/csv",
        )

with tab3:
    st.subheader("Upload Multiple New CVs")
    batch_files = st.file_uploader("Upload multiple .txt CVs", type=["txt"], accept_multiple_files=True, key="batch")
    if batch_files:
        batch_result = run_batch_inference(batch_files, model)
        st.dataframe(batch_result, use_container_width=True)
        st.download_button(
            "Download Batch Inference CSV",
            batch_result.to_csv(index=False).encode("utf-8"),
            file_name="batch_inference_result.csv",
            mime="text/csv",
        )
