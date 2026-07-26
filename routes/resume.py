from io import BytesIO

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    make_response,
    jsonify
)
from services.cover_letter_service import generate_cover_letter

from services.docx_service import (
    generate_docx,
    generate_cover_letter as generate_cover_letter_docx
)   
from services.job_match_service import job_match
from flask_login import login_required, current_user
from xhtml2pdf import pisa
from services.resume_optimizer import optimize_resume

from extensions import db
from models.resume import Resume

from services.ats_service import calculate_ats_score
from services.ai_service import generate_summary


resume = Blueprint("resume", __name__)


# ==========================================================
# Resume Builder
# ==========================================================
@resume.route("/resume", methods=["GET","POST"])
@login_required
def resume_builder():

    if request.method == "POST":

        # -------- Experience --------
        companies = request.form.getlist("company[]")
        job_titles = request.form.getlist("job_title[]")
        durations = request.form.getlist("duration[]")
        descriptions = request.form.getlist("job_description[]")

        experience = ""

        for company, title, duration, description in zip(
                companies,
                job_titles,
                durations,
                descriptions):

            if company or title or duration or description:

                experience += (
                    f"Company : {company}\n"
                    f"Job Title : {title}\n"
                    f"Duration : {duration}\n"
                    f"Description : {description}\n\n"
                )

        # -------- Custom Sections --------
        custom_titles = request.form.getlist("custom_title[]")
        custom_contents = request.form.getlist("custom_content[]")

        custom_sections = ""

        for title, content in zip(custom_titles, custom_contents):

            if title or content:

                custom_sections += (
                    f"## {title}\n"
                    f"{content}\n\n"
                )


        # -------- Save Resume --------
        
        new_resume = Resume(

            user_id=current_user.id,

            full_name=request.form.get("full_name"),
            email=request.form.get("email"),
            phone=request.form.get("phone"),
            address=request.form.get("address"),

            linkedin=request.form.get("linkedin"),
            github=request.form.get("github"),

            summary=request.form.get("summary"),

            education=request.form.get("education"),
            experience=experience,
            skills=request.form.get("skills"),
            projects=request.form.get("projects"),
            certifications=request.form.get("certifications"),

            custom_sections=custom_sections,

            country=request.form.get("country"),
            template=request.form.get("template")

        )

        db.session.add(new_resume)
        db.session.commit()

        flash("Resume saved successfully!", "success")

        return redirect(url_for("resume.my_resumes"))

    return render_template("resume.html")
# ==========================================================
# My Resumes
# ==========================================================
@resume.route("/my-resumes")
@login_required
def my_resumes():

    resumes = (
        Resume.query
        .filter_by(user_id=current_user.id)
        .order_by(Resume.created_at.desc())
        .all()
    )

    return render_template(
        "my_resumes.html",
        resumes=resumes
    )

# ==========================================================
# Edit Resume
# ==========================================================
@resume.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_resume(id):

    resume_data = Resume.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    if request.method == "POST":

        resume_data.full_name = request.form.get("full_name")
        resume_data.email = request.form.get("email")
        resume_data.phone = request.form.get("phone")
        resume_data.address = request.form.get("address")

        resume_data.linkedin = request.form.get("linkedin")
        resume_data.github = request.form.get("github")

        resume_data.summary = request.form.get("summary")
        resume_data.education = request.form.get("education")
        resume_data.skills = request.form.get("skills")
        resume_data.projects = request.form.get("projects")
        resume_data.certifications = request.form.get("certifications")

        resume_data.country = request.form.get("country")
        resume_data.template = request.form.get("template")

        db.session.commit()

        flash("Resume updated successfully!", "success")

        return redirect(url_for("resume.my_resumes"))

    return render_template(
        "edit_resume.html",
        resume=resume_data
    )
# ==========================================================
# Resume Preview
# ==========================================================
@resume.route("/preview/<int:id>")
@login_required
def preview(id):

    resume_data = (
        Resume.query
        .filter_by(
            id=id,
            user_id=current_user.id
        )
        .first_or_404()
    )

    template_map = {
        "classic": "resume_templates/classic.html",
        "modern": "resume_templates/modern.html",
        "executive": "resume_templates/executive.html",
        "pam": "resume_templates/pam.html",
        "data_analyst": "resume_templates/data_analyst.html",
    }

    template_name = template_map.get(
        resume_data.template,
        "resume_templates/classic.html"
    )

    return render_template(
        template_name,
        resume=resume_data
    )

# ============================================
# Download Gateway
# ============================================
@resume.route("/download-gateway/<type>/<int:id>")
@login_required
def download_gateway(type, id):

    if type == "pdf":

        download_url = url_for(
            "resume.download_resume",
            id=id
        )

    elif type == "docx":

        download_url = url_for(
            "resume.download_docx",
            id=id
        )

    elif type == "coverpdf":

        download_url = url_for(
            "resume.download_cover_letter_pdf",
            id=id
        )

    elif type == "coverdocx":

        download_url = url_for(
            "resume.download_cover_letter",
            id=id
        )

    else:

        flash("Invalid download type.", "danger")
        return redirect(url_for("resume.my_resumes"))

    return render_template(
        "download_gateway.html",
        download_url=download_url
    )
# ==========================================================
# Download Resume PDF
# ==========================================================
@resume.route("/download/<int:id>")
@login_required
def download_resume(id):

    resume_data = (
        Resume.query
        .filter_by(
            id=id,
            user_id=current_user.id
        )
        .first_or_404()
    )

    template_map = {
        "classic": "resume_templates/classic.html",
        "modern": "resume_templates/modern.html",
        "executive": "resume_templates/executive.html",
        "pam": "resume_templates/pam.html",
        "data_analyst": "resume_templates/data_analyst.html",
    }

    template_name = template_map.get(
        resume_data.template,
        "resume_templates/classic.html"
    )

    html = render_template(
        template_name,
        resume=resume_data
    )

    pdf = BytesIO()

    pisa.CreatePDF(
        html,
        dest=pdf
    )

    response = make_response(pdf.getvalue())

    response.headers["Content-Type"] = "application/pdf"

    response.headers["Content-Disposition"] = (
        f'{resume_data.full_name}_Resume.pdf'
    )

    return response

# ==========================================================
# Download Resume DOCX
# ==========================================================
@resume.route("/download-docx/<int:id>")
@login_required
def download_docx(id):

    resume_data = (
        Resume.query
        .filter_by(
            id=id,
            user_id=current_user.id
        )
        .first_or_404()
    )

    document = generate_docx(resume_data)

    file_stream = BytesIO()

    document.save(file_stream)

    file_stream.seek(0)

    response = make_response(file_stream.read())

    response.headers[
        "Content-Type"
    ] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    response.headers[
        "Content-Disposition"
    ] = f'attachment; filename="{resume_data.full_name}_Resume.docx"'

    return response

# ==========================================================
# Download Cover Letter DOCX
# ==========================================================
@resume.route("/download-cover-letter/<int:id>")
@login_required
def download_cover_letter(id):

    resume_data = (
        Resume.query
        .filter_by(
            id=id,
            user_id=current_user.id
        )
        .first_or_404()
    )

    document = generate_cover_letter_docx(
        resume_data
    )

    file_stream = BytesIO()

    document.save(file_stream)

    file_stream.seek(0)

    response = make_response(file_stream.read())

    response.headers[
        "Content-Type"
    ] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    response.headers[
        "Content-Disposition"
    ] = (
        f'attachment; filename="{resume_data.full_name}_CoverLetter.docx"'
    )

    return response

# ==========================================================
# Download Cover Letter PDF
# ==========================================================

@resume.route("/download-cover-letter-pdf/<int:id>")
@login_required
def download_cover_letter_pdf(id):

    resume_data = (
        Resume.query
        .filter_by(
            id=id,
            user_id=current_user.id
        )
        .first_or_404()
    )

    cover_letter = generate_cover_letter(

        resume_data,
        "",
        ""

    )

    html = render_template(

        "cover_letter_pdf.html",

        cover_letter=cover_letter

    )

    pdf = BytesIO()

    pisa.CreatePDF(

        html,

        dest=pdf

    )

    response = make_response(pdf.getvalue())

    response.headers["Content-Type"] = "application/pdf"

    response.headers["Content-Disposition"] = (

        f'{resume_data.full_name}_CoverLetter.pdf'

    )

    return response
# ==========================================================
# ATS Score
# ==========================================================
@resume.route("/ats-score/<int:id>")
@login_required
def ats_score(id):

    resume_data = (
        Resume.query
        .filter_by(
            id=id,
            user_id=current_user.id
        )
        .first_or_404()
    )

    result = calculate_ats_score(resume_data)

    return render_template(
    "ats_score.html",
    resume=resume_data,
    score=result["score"],
    found=result["found"],
    missing=result["missing"],
    suggestions=result["suggestions"]
)
# ==========================================================
# Job Match
# ==========================================================

@resume.route("/job-match/<int:id>", methods=["GET", "POST"])
@login_required
def job_match_route(id):

    resume_data = (
        Resume.query
        .filter_by(
            id=id,
            user_id=current_user.id
        )
        .first_or_404()
    )

    score = None
    found = []
    missing = []
    tips = []
    estimated_score = None
    job_description = ""

    if request.method == "POST":

        job_description = request.form.get(
            "job_description",
            ""
        )

        result = job_match(
            resume_data,
            job_description
        )

        score = result["score"]
        found = result["found"]
        missing = result["missing"]

        optimizer = optimize_resume(
            found,
            missing
        )

        tips = optimizer["tips"]
        estimated_score = optimizer["estimated_score"]

    return render_template(

        "job_match.html",

        resume=resume_data,

        score=score,

        found=found,

        missing=missing,

        tips=tips,

        estimated_score=estimated_score,

        job_description=job_description

    )
# ==========================================================
# AI Summary Generator
# ==========================================================
@resume.route("/generate-summary", methods=["POST"])
@login_required
def generate_ai_summary():

    data = request.get_json()

    name = data.get("name", "")
    role = data.get("role", "")
    experience = data.get("experience", "")

    summary = generate_summary(
        name,
        role,
        experience
    )

    return jsonify({
        "summary": summary
    })


# ==========================================================
# Delete Resume
# ==========================================================
@resume.route("/delete/<int:id>")
@login_required
def delete_resume(id):

    resume_data = (
        Resume.query
        .filter_by(
            id=id,
            user_id=current_user.id
        )
        .first_or_404()
    )

    db.session.delete(resume_data)
    db.session.commit()

    flash("Resume deleted successfully!", "success")

    return redirect(url_for("resume.my_resumes"))