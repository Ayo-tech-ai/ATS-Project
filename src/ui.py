import pandas as pd
import streamlit as st

from src.ats_engine import fit_ats_model


@st.cache_resource
def load_model():
    return fit_ats_model("data/baseline_cvs", "data/job_description.txt")


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
                padding: 1.8rem 1.5rem 1.5rem 1.5rem;
                margin-bottom: 1rem;
            }

            .hero-centered {
                text-align: center;
            }

            .hero-title {
                font-size: 2.35rem;
                font-weight: 800;
                margin-bottom: 0.35rem;
                letter-spacing: 0;
            }

            .hero-subtitle {
                font-size: 1rem;
                color: #4b5563;
                margin-bottom: 0.65rem;
            }

            .hero-description {
                font-size: 0.96rem;
                color: #5b6473;
                max-width: 860px;
                margin: 0 auto 0.75rem auto;
                line-height: 1.55;
            }

            .status-wrap {
                display: flex;
                gap: 0.5rem;
                flex-wrap: wrap;
                justify-content: center;
                margin-top: 0.6rem;
                margin-bottom: 1rem;
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
                margin-bottom: 0.2rem;
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
                margin-top: 0.5rem;
            }

            .small-note {
                font-size: 0.85rem;
                color: #6b7280;
            }

            .step-card {
                background: #ffffff;
                border: 1px solid #e6ebf2;
                border-radius: 10px;
                padding: 1rem;
                height: 100%;
            }

            .step-number {
                font-size: 0.78rem;
                font-weight: 800;
                color: #0F766E;
                margin-bottom: 0.45rem;
            }

            .step-title {
                font-size: 0.96rem;
                font-weight: 700;
                color: #111827;
                margin-bottom: 0.25rem;
            }

            .step-text {
                font-size: 0.88rem;
                color: #5b6473;
                line-height: 1.5;
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
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_brand_header(title, subtitle, description, centered=True, accent_color="#0F766E"):
    alignment_class = "hero-centered" if centered else ""
    st.markdown(
        f"""
        <div class="hero {alignment_class}">
            <div class="hero-title" style="color: {accent_color};">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
            <div class="hero-description">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_status_pills(items):
    pills = "".join([f'<span class="status-pill">{item}</span>' for item in items])
    st.markdown(f'<div class="status-wrap">{pills}</div>', unsafe_allow_html=True)


def get_match_badge(level):
    badge_class = {
        "High Match": "badge badge-high",
        "Medium Match": "badge badge-medium",
        "Low Match": "badge badge-low",
    }.get(level, "badge")
    return f'<span class="{badge_class}">{level}</span>'


def extract_skill_tags(explanation):
    if "such as:" not in explanation.lower():
        return []
    _, _, trailing = explanation.partition("such as:")
    skills = [item.strip().strip(".") for item in trailing.split(",") if item.strip()]
    return skills[:6]


def style_results_table(df):
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


def render_metrics(df, total_label="Total Candidates"):
    total_candidates = len(df)
    top_score = df["Score"].max() if total_candidates else 0
    high_matches = (df["Match Level"] == "High Match").sum() if total_candidates else 0
    avg_score = df["Score"].mean() if total_candidates else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(total_label, f"{total_candidates}")
    col2.metric("Top Match Score", f"{top_score:.3f}")
    col3.metric("High Matches", f"{high_matches}")
    col4.metric("Average Match Score", f"{avg_score:.3f}")


def render_top_candidates(df, title, limit=5):
    st.markdown(
        f"""
        <div class="section-card">
            <div class="section-title">{title}</div>
            <div class="section-caption">Highest-ranked candidates with concise match summaries.</div>
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


def render_score_analytics(df):
    left, right = st.columns(2)

    with left:
        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">Match Level Breakdown</div>
                <div class="section-caption">Distribution of match labels across the current candidate view.</div>
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
                <div class="section-caption">Binned distribution of similarity scores.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        score_bins = pd.cut(df["Score"], bins=6).value_counts().sort_index()
        score_bins.index = score_bins.index.astype(str)
        st.bar_chart(score_bins)


def render_table_and_download(df, file_name, button_label, section_title, section_caption):
    st.markdown(
        f"""
        <div class="section-card">
            <div class="section-title">{section_title}</div>
            <div class="section-caption">{section_caption}</div>
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
    )


def render_home_cta():
    st.markdown(
        """
        <div class="cta-panel">
            <div class="cta-title">Ready to review new applicants?</div>
            <div class="cta-text">
                Move into the dedicated screening workspace to evaluate a single candidate or screen a new batch of CVs.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link(
        "pages/1_Screening_Workspace.py",
        label="Open Screening Workspace",
        icon="📂",
        use_container_width=True,
    )


def render_workflow_steps():
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">How TalentMatch Works</div>
            <div class="section-caption">A simple screening flow designed for structured candidate review.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="step-card">
                <div class="step-number">STEP 1</div>
                <div class="step-title">Review Baseline Candidates</div>
                <div class="step-text">
                    Use the home dashboard to monitor rankings, match levels, and score distribution across the existing candidate pool.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="step-card">
                <div class="step-number">STEP 2</div>
                <div class="step-title">Open Screening Workspace</div>
                <div class="step-text">
                    Move into a dedicated review environment built for new applicant screening without cluttering the overview dashboard.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="step-card">
                <div class="step-number">STEP 3</div>
                <div class="step-title">Screen Single or Batch Uploads</div>
                <div class="step-text">
                    Choose one-candidate review for individual ranking or batch screening for a ranked set of new applicants.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_empty_state(message):
    st.markdown(
        f"""
        <div class="empty-state">
            {message}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_single_candidate_view(single_result, baseline_count):
    row = single_result.iloc[0]
    percentile_band = (row["Rank"] / baseline_count) * 100 if baseline_count else 0
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
                Placement band: <strong>Top {percentile_band:.1f}%</strong>
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
        section_title="Single Candidate Result",
        section_caption="Final ATS output for the uploaded candidate, including score, match level, baseline rank, and explanation.",
    )


def render_batch_summary(batch_result):
    top_candidate = batch_result.iloc[0]
    skills = extract_skill_tags(top_candidate["Explanation"])

    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Top Candidate in Current Batch</div>
            <div class="section-caption">Highest-ranked applicant from the uploaded set.</div>
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
