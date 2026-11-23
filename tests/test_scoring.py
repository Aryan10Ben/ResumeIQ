from resumeiq.scoring import calculate_score, cosine_text_similarity
from resumeiq.service import DEMO_JOB_DESCRIPTION, sample_documents, screen_documents


def test_score_is_bounded_and_transparent():
    details = calculate_score("Python Flask React", "Python Flask React", ["Python", "Flask"], ["Python", "Flask"])
    assert 0 <= details["score"] <= 100
    assert details["skill_coverage"] == 100
    assert details["text_similarity"] > 0
    assert "65%" in details["score_method"]


def test_no_recognized_skills_falls_back_to_text_similarity():
    detail = calculate_score("accounting finance", "accounting reporting", [], [])
    assert detail["skill_coverage"] is None
    assert detail["score"] == detail["text_similarity"]


def test_empty_or_stopword_only_document():
    assert cosine_text_similarity("", "Python") == 0
    assert cosine_text_similarity("the and or", "the or") == 0


def test_sample_full_stack_ranking_is_sensible():
    results, errors = screen_documents(sample_documents(), DEMO_JOB_DESCRIPTION)
    assert not errors
    assert len(results) == 3
    assert results[0]["filename"] == "alice_dev.txt"
    assert results[0]["score"] >= results[1]["score"] >= results[2]["score"]
    assert "Python" in results[0]["matched_skills"]


def test_sample_data_science_ranking_is_sensible():
    jd = "Data Scientist: Python, Pandas, NumPy, Machine Learning, NLP, Scikit-learn, TensorFlow, AWS."
    results, errors = screen_documents(sample_documents(), jd)
    assert not errors
    assert results[0]["filename"] == "bob_ds.txt"


def test_result_is_repeatable():
    first, _ = screen_documents(sample_documents(), DEMO_JOB_DESCRIPTION)
    second, _ = screen_documents(sample_documents(), DEMO_JOB_DESCRIPTION)
    assert [row["score"] for row in first] == [row["score"] for row in second]
