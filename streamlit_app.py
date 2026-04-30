import streamlit as st

from src.ui import (
    inject_custom_css,
    load_model,
    render_brand_header,
    render_metrics,
    render_score_analytics,
    render_status_pills,
    render_table_and_download,
    render_top_candidates,
    render_workflow_steps,
)

st.set_page_config(
    page_title="TalentMatch",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded",
)


def render_home_cta_button():
    st.markdown(
        """
        <div class="cta-panel">
            <div class="cta-title">Ready to screen new applicants?</div>
            <div class="cta-text">
                Move into the dedicated screening workspace to evaluate one candidate at a time
                or rank a new batch of CVs using the existing ATS engine.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, center, right = st.columns([1, 1.5, 1])

    with center:
        if st.button(
            "Open Screening Workspace",
            type="primary",
            use_container_width=True,
            key="open_screening_workspace_home",
        ):
            st.switch_page("pages/1_Screening_Workspace.py")

    st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)


def main():
    inject_custom_css()
    model = load_model()

    baseline_df = model.baseline_df.copy()

    render_brand_header(
        title="TalentMatch",
        subtitle="A Mini ATS for Resume Screening and Candidate Ranking",
        description=(
            "Review baseline candidates, monitor match distribution, and move into a dedicated "
            "screening workspace for single or batch applicant review."
        ),
        centered=True,
        accent_color="#0F766E",
    )

    render_status_pills(
        [
            f"{len(baseline_df)} baseline CVs loaded",
            "Job description active",
            "Single and batch screening available",
        ]
    )

    render_home_cta_button()

    render_metrics(baseline_df, total_label="Total Candidates")
    render_top_candidates(baseline_df, title="Top 5 Baseline Candidates", limit=5)
    render_score_analytics(baseline_df)
    render_workflow_steps()

    render_table_and_download(
        baseline_df,
        file_name="baseline_ranking.csv",
        button_label="Download Baseline Ranking CSV",
        section_title="Baseline Candidate Ranking",
        section_caption="Full ranked baseline candidate view with scores, match levels, and explanation summaries.",
    )


if __name__ == "__main__":
    main()
