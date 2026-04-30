import streamlit as st

from src.ats_engine import run_batch_inference, run_single_inference
from src.ui import (
    inject_custom_css,
    load_model,
    render_batch_summary,
    render_brand_header,
    render_empty_state,
    render_metrics,
    render_single_candidate_view,
    render_status_pills,
    render_table_and_download,
    render_top_candidates,
)

st.set_page_config(
    page_title="TalentMatch | Screening Workspace",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded",
)


def render_home_button():
    st.markdown(
        """
        <div class="top-nav-wrap">
            <a class="top-nav-link" href="/" target="_self">Home</a>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main():
    inject_custom_css()
    model = load_model()

    render_home_button()

    render_brand_header(
        title="TalentMatch",
        subtitle="Screening Workspace",
        description="Choose a screening mode to evaluate a single candidate against the baseline pool or rank a new batch of applicants.",
        centered=True,
        accent_color="#0F766E",
    )

    render_status_pills(
        [
            "ATS engine active",
            "Baseline comparison ready",
            "TXT CV upload supported",
        ]
    )

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    mode = st.radio(
        "Choose screening mode",
        ["Single Candidate Review", "Batch Screening"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if mode == "Single Candidate Review":
        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">Single Candidate Review</div>
                <div class="section-caption">
                    Upload one CV in .txt format to compare it against the original baseline ranking.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        single_file = st.file_uploader(
            "Upload a single CV (.txt)",
            type=["txt"],
            key="single_candidate_uploader_page",
        )

        if single_file is None:
            render_empty_state(
                "Upload one candidate CV to generate a score, match level, baseline rank position, and explanation summary."
            )
        else:
            with st.spinner("Reviewing candidate..."):
                single_result = run_single_inference(single_file, model)

            render_single_candidate_view(
                single_result,
                baseline_count=len(model.baseline_df),
            )

    else:
        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">Batch Screening</div>
                <div class="section-caption">
                    Upload multiple CVs in .txt format to rank candidates within the new batch.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        batch_files = st.file_uploader(
            "Upload multiple CVs (.txt)",
            type=["txt"],
            accept_multiple_files=True,
            key="batch_candidate_uploader_page",
        )

        if not batch_files:
            render_empty_state(
                "Upload multiple candidate CVs to generate ranked batch screening results, explanations, and a downloadable CSV."
            )
        else:
            with st.spinner("Screening batch candidates..."):
                batch_result = run_batch_inference(batch_files, model)

            render_batch_summary(batch_result)
            render_metrics(batch_result, total_label="Uploaded Candidates")
            render_top_candidates(
                batch_result,
                title="Top Candidates in Current Batch",
                limit=min(5, len(batch_result)),
            )
            render_table_and_download(
                batch_result,
                file_name="batch_inference_result.csv",
                button_label="Download Batch Screening CSV",
                section_title="Batch Screening Results",
                section_caption="Ranked results for the uploaded batch only, including scores, match levels, and explanations.",
            )

    st.markdown(
        """
        <div class="small-note" style="margin-top: 1rem;">
            The presentation layer has been upgraded for a more professional HR dashboard experience. The ATS scoring and ranking logic remain unchanged.
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
