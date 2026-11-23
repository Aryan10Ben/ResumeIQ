from io import BytesIO


def test_homepage_renders(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Screen & Rank Resumes" in response.data
    assert b"Try an instant demo" in response.data


def test_health_is_lightweight(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"
    assert response.json["skills_loaded"] >= 90


def test_demo_renders_rankings(client):
    response = client.get("/demo")
    assert response.status_code == 200
    assert b"alice_dev.txt" in response.data
    assert b"bob_ds.txt" in response.data
    assert b"Recognized-skill coverage" in response.data
    assert b"Download comparison CSV" in response.data


def test_post_txt_upload_matches(client):
    response = client.post(
        "/match",
        data={
            "job_description": "Python Flask React Docker",
            "resumes": (BytesIO(b"Python Flask Docker React"), "candidate.txt"),
        },
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    assert b"candidate.txt" in response.data


def test_missing_resume_redirects_with_message(client):
    response = client.post("/match", data={"job_description": "Python"})
    assert response.status_code == 302
    page = client.get("/")
    assert b"Please upload at least one" in page.data


def test_missing_job_description_redirects(client):
    response = client.post(
        "/match",
        data={"resumes": (BytesIO(b"Python"), "x.txt")},
        content_type="multipart/form-data",
        follow_redirects=True,
    )
    assert b"Please paste a job description" in response.data


def test_html_filename_is_not_rendered_as_code(client):
    response = client.post(
        "/match",
        data={
            "job_description": "Python",
            "resumes": (BytesIO(b"Python"), "<img src=x onerror=alert(1)>.txt"),
        },
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    assert b"<img src=x onerror=alert(1)>" not in response.data


def test_invalid_content_type_is_rejected(client):
    response = client.post(
        "/match",
        data={
            "job_description": "Python",
            "resumes": (BytesIO(b"not a pdf"), "fake.pdf"),
        },
        content_type="multipart/form-data",
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"PDF file signature is invalid" in response.data


def test_too_many_files_is_rejected(client):
    response = client.post(
        "/match",
        data={
            "job_description": "Python",
            "resumes": [(BytesIO(b"Python"), f"{i}.txt") for i in range(6)],
        },
        content_type="multipart/form-data",
        follow_redirects=True,
    )
    assert b"up to five resumes" in response.data


def test_oversized_request_does_not_crash(client):
    response = client.post(
        "/match",
        data={
            "job_description": "Python",
            "resumes": (BytesIO(b"x" * (4 * 1024 * 1024 + 1)), "too-big.txt"),
        },
        content_type="multipart/form-data",
        follow_redirects=False,
    )
    assert response.status_code in (302, 303)
