from flask import Flask, render_template, request
import os
from resume_parser import parse_resume
from jd_matcher import extract_jd_keywords, match_score
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        resume_file = request.files["resume"]
        jd_text = request.form["jd"]

        if resume_file:
            filename = secure_filename(resume_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            resume_file.save(filepath)

            resume_data = parse_resume(filepath)
            jd_keywords = extract_jd_keywords(jd_text)
            score = match_score(resume_data["skills"], jd_keywords)
            return render_template("result.html", data=resume_data, score=score, jd=jd_keywords)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
