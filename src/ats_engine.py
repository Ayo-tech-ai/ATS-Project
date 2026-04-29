from dataclasses import dataclass
from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .config import HIGH_MATCH_THRESHOLD, MEDIUM_MATCH_THRESHOLD, PRIORITY_KEYWORDS
from .text_utils import preprocess_text, get_priority_matches, build_explanation

@dataclass
class ATSModel:
    vectorizer: TfidfVectorizer
    jd_vector: object
    processed_jd: str
    baseline_scores: list
    baseline_df: pd.DataFrame

def classify_match(score):
    if score >= HIGH_MATCH_THRESHOLD:
        return "High Match"
    if score >= MEDIUM_MATCH_THRESHOLD:
        return "Medium Match"
    return "Low Match"

def _sort_cv_paths(paths):
    return sorted(
        paths,
        key=lambda p: int("".join(filter(str.isdigit, p.stem)) or 0)
    )

def load_baseline_data(cv_folder, jd_path):
    cv_paths = _sort_cv_paths(list(Path(cv_folder).glob("*.txt")))
    cv_names = [path.name for path in cv_paths]
    cv_texts = [path.read_text(encoding="utf-8", errors="ignore") for path in cv_paths]
    jd_text = Path(jd_path).read_text(encoding="utf-8", errors="ignore")
    return cv_names, cv_texts, jd_text

def fit_ats_model(cv_folder, jd_path):
    cv_names, cv_texts, jd_text = load_baseline_data(cv_folder, jd_path)

    processed_cvs = [preprocess_text(text) for text in cv_texts]
    processed_jd = preprocess_text(jd_text)

    corpus = processed_cvs + [processed_jd]
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(corpus)

    cv_vectors = tfidf_matrix[:-1]
    jd_vector = tfidf_matrix[-1]
    scores = cosine_similarity(cv_vectors, jd_vector).flatten()

    explanations = [
        build_explanation(get_priority_matches(text, processed_jd, PRIORITY_KEYWORDS))
        for text in processed_cvs
    ]

    baseline_df = pd.DataFrame({
        "Candidate Name": cv_names,
        "Score": scores,
        "Explanation": explanations,
    })

    baseline_df["Match Level"] = baseline_df["Score"].apply(classify_match)
    baseline_df = baseline_df.sort_values(by="Score", ascending=False).reset_index(drop=True)
    baseline_df["Rank"] = range(1, len(baseline_df) + 1)
    baseline_df = baseline_df[["Candidate Name", "Score", "Match Level", "Rank", "Explanation"]]

    return ATSModel(
        vectorizer=vectorizer,
        jd_vector=jd_vector,
        processed_jd=processed_jd,
        baseline_scores=baseline_df["Score"].tolist(),
        baseline_df=baseline_df,
    )

def run_single_inference(uploaded_file, model):
    raw_text = uploaded_file.getvalue().decode("utf-8", errors="ignore")
    processed_text = preprocess_text(raw_text)
    vector = model.vectorizer.transform([processed_text])
    score = cosine_similarity(vector, model.jd_vector)[0][0]
    matches = get_priority_matches(processed_text, model.processed_jd, PRIORITY_KEYWORDS)

    result = pd.DataFrame([{
        "Candidate Name": uploaded_file.name,
        "Score": score,
        "Match Level": classify_match(score),
        "Rank": sum(existing > score for existing in model.baseline_scores) + 1,
        "Explanation": build_explanation(matches),
    }])

    return result

def run_batch_inference(uploaded_files, model):
    names = [file.name for file in uploaded_files]
    raw_texts = [file.getvalue().decode("utf-8", errors="ignore") for file in uploaded_files]
    processed_texts = [preprocess_text(text) for text in raw_texts]
    vectors = model.vectorizer.transform(processed_texts)
    scores = cosine_similarity(vectors, model.jd_vector).flatten()

    explanations = [
        build_explanation(get_priority_matches(text, model.processed_jd, PRIORITY_KEYWORDS))
        for text in processed_texts
    ]

    results = pd.DataFrame({
        "Candidate Name": names,
        "Score": scores,
        "Explanation": explanations,
    })

    results["Match Level"] = results["Score"].apply(classify_match)
    results = results.sort_values(by="Score", ascending=False).reset_index(drop=True)
    results["Rank"] = range(1, len(results) + 1)

    return results[["Candidate Name", "Score", "Match Level", "Rank", "Explanation"]]
