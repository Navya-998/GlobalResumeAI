from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models.resume import Resume

main = Blueprint("main", __name__)


# ==========================================================
# Home
# ==========================================================
@main.route("/")
def home():
    return render_template("home.html")


# ==========================================================
# Dashboard
# ==========================================================
@main.route("/dashboard")
@login_required
def dashboard():

    resumes = Resume.query.filter_by(
        user_id=current_user.id
    ).all()

    total_resumes = len(resumes)

    ats_score = 0
    pam_score = 0
    latest_resume = None

    if resumes:

        latest_resume = resumes[-1]

        keywords = [
            "CyberArk",
            "BeyondTrust",
            "ARCON",
            "Wallix",
            "Delinea",
            "Hashicorp Vault",
            "Linux",
            "Windows",
            "Active Directory",
            "PowerShell",
            "ServiceNow"
        ]

        text = (
            str(latest_resume.skills or "") +
            str(latest_resume.pam_skills or "") +
            str(latest_resume.summary or "")
        ).lower()

        score = 0

        for keyword in keywords:

            if keyword.lower() in text:
                score += 10

        pam_score = min(score, 100)

        ats_score = min(
            100,
            40
            + len((latest_resume.skills or "").split(",")) * 5
            + len((latest_resume.projects or "").split("\n")) * 5
        )

    return render_template(
        "dashboard.html",
        user=current_user,
        resumes=resumes,
        latest_resume=latest_resume,
        total_resumes=total_resumes,
        ats_score=ats_score,
        pam_score=pam_score
    )