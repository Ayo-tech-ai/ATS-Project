import pandas as pd
import streamlit as st

from src.ats_engine import fit_ats_model, run_batch_inference, run_single_inference


st.set_page_config(
    page_title="Mini ATS",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_custom_css():
    st.markdown(
        """
        <style>
            .stApp {
                background-color: #f6f8fb;
            }

            .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
                max-width: 1400px;
            }

            .hero {
                background: #ffffff;
                border: 1px solid #e6ebf2;
                border-radius: 10px;
                padding: 1.5rem 1.5rem 1.25rem 1.5rem;
                margin-bottom: 1rem;
            }

            .hero-title {
                font-size: 2rem;
                font-weight: 700;
                color: #111827;
                margin-bottom: 0.35rem;
            }

            .hero-subtitle {
                font-size: 1rem;
                color: #4b5563;
                margin-bottom: 1rem;
            }

            .status-wrap {
                display: flex;
                gap: 0.5rem;
                flex-wrap: wrap;
                margin-top: 0.25rem;
            }

            .status-pill {
                display: inline-block;
                padding: 0.4rem 0.75rem;
                border-radius: 999px;
                background: #f3f6fb;
                border: 1px solid #e3e9f2;
                color: #24324a;
                font-size: 0.85rem;
                font-weight: 600;
            }

            .section-card {
                background: #ffffff;
                border: 1px solid #e6ebf2;
                border-radius: 10px;
                padding: 1rem 1rem 0.75rem 1rem;
                margin-bottom: 1rem;
            }

            .section-title {
                font-size: 1.05rem;
                font-weight: 700;
                color: #111827;
                margin-bottom: 0.25rem;
            }

            .section-caption {
                font-size: 0.9rem;
                color: #6b7280;
                margin-bottom: 0.75rem;
            }

            .candidate-card {
                background: #ffffff;
                border: 1px solid #e6ebf2;
                border-radius: 10px;
                padding: 1rem;
                margin-bottom: 0.85rem;
            }

            .candidate-topline {
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 0.75rem;
                margin-bottom: 0.55rem;
            }

            .candidate-name {
                font-size: 1rem;
                font-weight: 700;
                color: #111827;
            }

            .candidate-meta {
                font-size: 0.9rem;
                color: #4b5563;
                margin-bottom: 0.65rem;
            }

            .candidate-explanation {
                font-size: 0.92rem;
                color: #374151;
                line-height: 1.45;
            }

            .badge {
                display: inline-block;
                padding: 0.32rem 0.65rem;
                border-radius: 999px;
                font-size: 0.78rem;
                font-weight: 700;
                border: 1px solid transparent;
                white-space: nowrap;
            }

            .badge-high {
                background: #e9f7ef;
                color: #166534;
                border-color: #ccebd7;
            }

            .badge-medium {
                background: #fff7e6;
                color: #9a6700;
                border-color: #f4dfb1;
            }

            .badge-low {
                background: #fdecec;
                color: #b42318;
                border-color: #f5c7c7;
            }

            .skill-wrap {
                display: flex;
                gap: 0.45rem;
                flex-wrap: wrap;
                margin-top: 0.75rem;
            }

            .skill-pill {
                display: inline-block;
                padding: 0.28rem 0.6rem;
                border-radius: 999px;
                background: #f4f7fb;
                border: 1px solid #dbe5f0;
                color: #334155;
                font-size: 0.78rem;
                font-weight: 600;
            }

            .empty-state {
                background: #ffffff;
                border: 1px dashed #d5deea;
                border-radius: 10px;
                padding: 1.5rem;
                text-align: center;
                color: #64748b;
            }

            .small-note {
                font-size: 0.85rem;
                color: #6b7280;
            }

            div[data-testid="stMetric"] {
                background: #ffffff;
                border: 1px solid #e6ebf2;
                border-radius: 10px;
                padding: 0.85rem 1rem;
            }

            div[data-testid="stMetricLabel"] {
                color: #6b7280;
                font-weight: 600;
            }

            div[data-testid="stMetricValue"] {
                color: #111827;
                font-weight: 700;
            }

            .sidebar-note {
                font-size: 0.88rem;
                line-height: 1.5;
                color: #4b5563;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_resource
def load_model():
    return fit_ats_model("data/baseline_cvs", "data/job_description.txt")


def get_match_badge(level: str) -> str:
    badge_class = {
        "High Match": "badge badge-high",
        "Medium Match": "badge badge-medium",
        "Low Match": "badge badge-low",
    }.get(level, "badge")
    return f'<span class="{badge_class}">{level}</span>'


def extract_skill_tags(explanation: str) -> list[str]:
    if "such as:" not in explanation.lower():
        return []
    _, _, trailing = explanation.partition("such as:")
    skills = [item.strip().strip(".") for item in trailing.split(",") if item.strip()]
    return skills[:6]


def style_results_table(df: pd.DataFrame):
    display_df = df.copy()
    display_df["Score"] = display_df["Score"].map(lambda x: f"{x:.3f}")

    def match_style(value):
        styles = {
            "High Match": "background-color: #e9f7ef; color: #166534; font-weight: 700;",
            "Medium Match": "background-color: #fff7e6; color: #9a6700; font-weight: 700;",
            "Low Match": "background-color: #fdecec; color: #b42318; font-weight: 700;",
        }
        return styles.get(value, "")

    return (
        display_df.style
        .map(match_style, subset=["Match Level"])
        .set_properties(subset=["Explanation"], **{"white-space": "normal"})
    )


def render_header(model):
    total_candidates = len(model.baseline_df)

    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-title">Mini ATS</div>
            <div class="hero-subtitle">
                Resume Screening and Candidate Ranking Dashboard
            </div>
            <div class="hero-subtitle" style="font-size: 0.95rem; margin-bottom: 0.75rem;">
                Evaluate baseline candidates and screen new applicants against the active job description.
            </div>
            <div class="status-wrap">
                <span class="status-pill">{total_candidates} baseline CVs loaded</span>
                <span class="status-pill">Job description active</span>
                <span class="status-pill">Single and batch screening ready</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    st.sidebar.title("Dashboard Notes")
    st.sidebar.markdown(
        """
        <div class="sidebar-note">
            This dashboard presents a fixed ATS scoring engine with a recruiter-friendly interface.
            The underlying preprocessing, TF-IDF modeling, ranking, and inference logic remain unchanged.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Sections**")
    st.sidebar.markdown("- Baseline Screening")
    st.sidebar.markdown("- Single Candidate Review")
    st.sidebar.markdown("- Batch Screening")
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Supported files**")
    st.sidebar.markdown("- `.txt` CV files")
    st.sidebar.markdown("- Single upload or multiple uploads")
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Outputs**")
    st.sidebar.markdown("- Match scores")
    st.sidebar.markdown("- Match levels")
    st.sidebar.markdown("- Ranked candidate views")
    st.sidebar.markdown("- CSV downloads")


def render_metrics(df: pd.DataFrame, total_label: str = "Total Candidates"):
    total_candidates = len(df)
    top_score = df["Score"].max() if total_candidates else 0
    high_matches = (df["Match Level"] == "High Match").sum() if total_candidates else 0
    avg_score = df["Score"].mean() if total_candidates else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(total_label, f"{total_candidates}")
    col2.metric("Top Match Score", f"{top_score:.3f}")
    col3.metric("High Matches", f"{high_matches}")
    col4.metric("Average Match Score", f"{avg_score:.3f}")


def render_top_candidates(df: pd.DataFrame, title: str, limit: int = 5):
    st.markdown(
        f"""
        <div class="section-card">
            <div class="section-title">{title}</div>
            <div class="section-caption">Highest-ranked candidates with match summaries.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    preview_df = df.head(limit)

    for _, row in preview_df.iterrows():
        skills = extract_skill_tags(row["Explanation"])
        skill_html = "".join([f'<span class="skill-pill">{skill}</span>' for skill in skills])

        st.markdown(
            f"""
            <div class="candidate-card">
                <div class="candidate-topline">
                    <div class="candidate-name">{row["Candidate Name"]}</div>
                    <div>{get_match_badge(row["Match Level"])}</div>
                </div>
                <div class="candidate-meta">
                    Score: <strong>{row["Score"]:.3f}</strong> &nbsp;&nbsp;|&nbsp;&nbsp;
                    Rank: <strong>{int(row["Rank"])}</strong>
                </div>
                <div class="candidate-explanation">{row["Explanation"]}</div>
                <div class="skill-wrap">{skill_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_score_analytics(df: pd.DataFrame, chart_title_prefix: str):
    left, right = st.columns(2)

    with left:
        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">Match Level Breakdown</div>
                <div class="section-caption">Distribution of candidate labels across the current view.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        match_counts = (
            df["Match Level"]
            .value_counts()
            .reindex(["High Match", "Medium Match", "Low Match"], fill_value=0)
        )
        st.bar_chart(match_counts)

    with right:
        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">Score Distribution</div>
                <div class="section-caption">Binned view of similarity scores for the current candidate set.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        score_bins = pd.cut(df["Score"], bins=6).value_counts().sort_index()
        score_bins.index = score_bins.index.astype(str)
        st.bar_chart(score_bins)

    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Top Score Comparison</div>
            <div class="section-caption">Top candidates ranked by similarity score.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    top_scores = df.head(10).set_index("Candidate Name")["Score"]
    st.bar_chart(top_scores)


def render_table_and_download(df: pd.DataFrame, file_name: str, button_label: str):
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Detailed Results</div>
            <div class="section-caption">Complete ranked output with match levels and explanation text.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.dataframe(style_results_table(df), use_container_width=True)
    st.download_button(
        button_label,
        df.to_csv(index=False).encode("utf-8"),
        file_name=file_name,
        mime="text/csv",
        use_container_width=False,
    )


def render_single_candidate_view(single_result: pd.DataFrame, baseline_count: int):
    row = single_result.iloc[0]
    top_share = (row["Rank"] / baseline_count) * 100 if baseline_count else 0
    skills = extract_skill_tags(row["Explanation"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Candidate", row["Candidate Name"])
    c2.metric("Match Score", f"{row['Score']:.3f}")
    c3.metric("Match Level", row["Match Level"])
    c4.metric("Rank Against Baseline", f"{int(row['Rank'])} / {baseline_count}")

    st.markdown(
        f"""
        <div class="candidate-card" style="margin-top: 0.75rem;">
            <div class="candidate-topline">
                <div class="candidate-name">Candidate Review Summary</div>
                <div>{get_match_badge(row["Match Level"])}</div>
            </div>
            <div class="candidate-meta">
                This candidate would place at rank <strong>{int(row["Rank"])}</strong> among the original baseline candidates.
                Top placement band: <strong>Top {top_share:.1f}%</strong>
            </div>
            <div class="candidate-explanation">{row["Explanation"]}</div>
            <div class="skill-wrap">
                {"".join([f'<span class="skill-pill">{skill}</span>' for skill in skills])}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_table_and_download(
        single_result,
        file_name="single_inference_result.csv",
        button_label="Download Single Candidate CSV",
    )


def render_batch_summary(batch_result: pd.DataFrame):
    render_metrics(batch_result, total_label="Uploaded Candidates")

    top_candidate = batch_result.iloc[0]
    skills = extract_skill_tags(top_candidate["Explanation"])

    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Top Candidate in Batch</div>
            <div class="section-caption">Highest-ranked applicant from the current upload set.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="candidate-card">
            <div class="candidate-topline">
                <div class="candidate-name">{top_candidate["Candidate Name"]}</div>
                <div>{get_match_badge(top_candidate["Match Level"])}</div>
            </div>
            <div class="candidate-meta">
                Score: <strong>{top_candidate["Score"]:.3f}</strong> &nbsp;&nbsp;|&nbsp;&nbsp;
                Rank in Batch: <strong>{int(top_candidate["Rank"])}</strong>
            </div>
            <div class="candidate-explanation">{top_candidate["Explanation"]}</div>
            <div class="skill-wrap">
                {"".join([f'<span class="skill-pill">{skill}</span>' for skill in skills])}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main():
    inject_custom_css()
    render_sidebar()

    try:
        model = load_model()
    except Exception as exc:
        st.error("The ATS model could not be loaded. Please verify your baseline files and project structure.")
        st.exception(exc)
        st.stop()

    render_header(model)

    tab1, tab2, tab3 = st.tabs(
        ["Baseline Screening", "Single Candidate Review", "Batch Screening"]
    )

    with tab1:
        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">Baseline Candidate Dashboard</div>
                <div class="section-caption">
                    Review the original candidate pool ranked against the active job description.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        baseline_df = model.baseline_df.copy()
        render_metrics(baseline_df)
        render_top_candidates(baseline_df, title="Top 5 Candidates", limit=5)
        render_score_analytics(baseline_df, chart_title_prefix="Baseline")
        render_table_and_download(
            baseline_df,
            file_name="baseline_ranking.csv",
            button_label="Download Baseline Ranking CSV",
        )

    with tab2:
        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">Single Candidate Review</div>
                <div class="section-caption">
                    Upload one CV in .txt format to evaluate it against the baseline ranking.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        single_file = st.file_uploader(
            "Upload a single CV (.txt)",
            type=["txt"],
            key="single_candidate_uploader",
        )

        if single_file is None:
            st.markdown(
                """
                <div class="empty-state">
                    Upload one candidate CV to generate a match score, match level, rank against the original 40 candidates, and explanation summary.
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            with st.spinner("Reviewing candidate..."):
                single_result = run_single_inference(single_file, model)
            render_single_candidate_view(single_result, baseline_count=len(model.baseline_df))

    with tab3:
        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">Batch Screening</div>
                <div class="section-caption">
                    Upload multiple CVs in .txt format to rank them within the new batch.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        batch_files = st.file_uploader(
            "Upload multiple CVs (.txt)",
            type=["txt"],
            accept_multiple_files=True,
            key="batch_candidate_uploader",
        )

        if not batch_files:
            st.markdown(
                """
                <div class="empty-state">
                    Upload multiple candidate CVs to generate ranked batch screening results, match levels, explanations, and a downloadable CSV.
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            with st.spinner("Screening batch candidates..."):
                batch_result = run_batch_inference(batch_files, model)

            render_batch_summary(batch_result)
            render_top_candidates(batch_result, title="Top Candidates in Current Batch", limit=min(5, len(batch_result)))
            render_score_analytics(batch_result, chart_title_prefix="Batch")
            render_table_and_download(
                batch_result,
                file_name="batch_inference_result.csv",
                button_label="Download Batch Screening CSV",
            )

    st.markdown(
        """
        <div class="small-note" style="margin-top: 1rem;">
            This interface upgrades the presentation layer only. The underlying ATS scoring, ranking, and inference logic remain unchanged.
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
