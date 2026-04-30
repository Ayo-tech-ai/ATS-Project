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
        <style>
            .home-cta-wrap {
                display: flex;
                justify-content: center;
                margin-top: 0.5rem;
                margin-bottom: 1.25rem;
            }

            .home-cta-link {
                display: inline-block;
                background-color: #0F766E;
                color: #ffffff !important;
                text-decoration: none;
                font-weight: 700;
                font-size: 0.98rem;
                padding: 0.9rem 1.4rem;
                border-radius: 10px;
                border: 1px solid #0b5f59;
                box-shadow: 0 1px 2px rgba(15, 118, 110, 0.15);
                transition: all 0.2s ease;
            }

            .home-cta-link:hover {
                background-color: #0b5f59;
                border-color: #094b46;
                color: #ffffff !important;
            }

            .cta-panel {
                background: #ffffff;
                border: 1px solid #dbe5f0;
                border-radius: 10px;
                padding: 1.15rem;
                margin-bottom: 1rem;
                text-align: center;
            }

            .cta-title {
                font-size: 1.05rem;
                font-weight: 700;
                color: #111827;
                margin-bottom: 0.3rem;
            }

            .cta-text {
                font-size: 0.92rem;
                color: #5b6473;
                margin-bottom: 0.8rem;
            }
        </style>

        <div class="cta-panel">
            <div class="cta-title">Ready to screen new applicants?</div>
            <div class="cta-text">
                Move into the dedicated screening workspace to evaluate a single candidate
                or rank a new batch of CVs using the existing ATS engine.
            </div>
            <div class="home-cta-wrap">
                <a class="home-cta-link" href="./Screening_Workspace" target="_self">
                    Open Screening Workspace
                </a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


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
