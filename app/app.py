import os
from typing import Any
from uuid import uuid4
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from tempfile import NamedTemporaryFile
from .business import get_question, evaluate_answer, extract_job_details
from .helpers.file import allowed_job_file


app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)
user_score: list[dict[str, int]] = []

job_details_state: dict[str, Any] = {}
interview_questions_state: dict[str, Any] = {}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/questions", methods=["GET"])
def get_questions():
    file_id = request.args.get("file_id")
    if not file_id:
        return jsonify({"status": "error", "message": "No file_id provided"}), 400

    job_details = job_details_state.get(file_id)
    if not job_details:
        return jsonify({"status": "error", "message": "Invalid file_id"}), 400

    temp_file_path = job_details.get("file_path")
    if not temp_file_path:
        return jsonify({"status": "error", "message": "Invalid file_id"}), 400

    if file_id in job_details_state and job_details_state[file_id].get(
        "extracted_job_details"
    ):
        extracted_job_details = job_details_state[file_id]["extracted_job_details"]
    else:
        extracted_job_details = extract_job_details(job_document=temp_file_path)

    job_details_state[file_id] = {
        **job_details,
        "extracted_job_details": extracted_job_details,
    }
    question = get_question(extracted_job_details, previous_scores=user_score)

    question_id = str(uuid4())
    existing_interview_questions = (
        interview_questions_state.get(file_id, {}).get("interview_questions") or []
    )
    existing_interview_questions.append(
        {"question_id": question_id, "question": question}
    )
    interview_questions_state[file_id] = {
        **interview_questions_state.get(file_id, {}),
        "interview_questions": existing_interview_questions,
    }

    response = {
        "job_details": extracted_job_details,
        "question": question,
        "question_id": question_id,
    }
    return jsonify(response)


@app.route("/api/evaluate", methods=["POST"])
def answer():
    data = request.json
    file_id = data.get("file_id")
    if not file_id:
        return jsonify({"status": "error", "message": "No file_id provided"}), 400

    question_id = data.get("question_id")
    if not question_id:
        return jsonify({"status": "error", "message": "No question_id provided"}), 400

    job_details = job_details_state.get(file_id)
    if not job_details:
        return jsonify({"status": "error", "message": "Invalid file_id"}), 400

    temp_file_path = job_details.get("file_path")
    if not temp_file_path:
        return jsonify({"status": "error", "message": "Invalid file_id"}), 400

    extracted_job_details = job_details.get("extracted_job_details")
    if not extracted_job_details:
        extracted_job_details = extract_job_details(job_document=temp_file_path)

    answer = data.get("answer")

    questions = interview_questions_state.get(file_id, {}).get("interview_questions")
    if not questions:
        return jsonify({"status": "error", "message": "Invalid question_id"}), 400

    question_details = next(
        (q for q in questions if q["question_id"] == question_id), None
    )
    if not question_details:
        return jsonify({"status": "error", "message": "Invalid question_id"}), 400

    question = question_details.get("question")
    test_cases = question_details.get("test_cases")
    question_type = question_details.get("question_type")

    result = evaluate_answer(
        answer=answer,
        question=question,
        question_type=question_type,
        test_cases=test_cases,
        job=extracted_job_details,
    )

    difficulty = question_details.get("difficulty")

    user_score.append({"score": result["score"], "difficulty": difficulty})

    return jsonify(result)


@app.route("/api/job", methods=["POST"])
def submit_job():
    file = request.files.get("document")
    if not file:
        return jsonify({"status": "error", "message": "No file uploaded"}), 400

    if file.filename == "":
        return jsonify({"status": "error", "message": "No selected file"}), 400

    if not allowed_job_file(file.filename):
        return jsonify(
            {
                "status": "error",
                "message": "Invalid file type. Only .pdf, .doc, and .docx files are allowed.",
            }
        ), 400

    try:
        file_id = str(uuid4())
        temp_file = NamedTemporaryFile(
            delete=False, suffix=os.path.splitext(file.filename)[1]
        )
        file.save(temp_file.name)

        job_details_state[file_id] = {
            "file_path": temp_file.name,
        }

        return jsonify(
            {
                "status": "success",
                "message": "Job details submitted successfully",
                "file_id": file_id,
                "temp_file": temp_file.name,
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8123)
