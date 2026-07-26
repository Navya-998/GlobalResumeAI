from datetime import datetime
from extensions import db


class Resume(db.Model):
    __tablename__ = "resumes"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # -------------------------
    # Personal Details
    # -------------------------

    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)

    phone = db.Column(db.String(30))
    address = db.Column(db.String(300))

    linkedin = db.Column(db.String(300))
    github = db.Column(db.String(300))

    # NEW

    # -------------------------
    # Resume Content
    # -------------------------

    summary = db.Column(db.Text)

    education = db.Column(db.Text)
    experience = db.Column(db.Text)
    skills = db.Column(db.Text)

    projects = db.Column(db.Text)
    certifications = db.Column(db.Text)

    custom_sections = db.Column(db.Text)

    pam_skills = db.Column(db.Text)

    # -------------------------
    # Settings
    # -------------------------

    country = db.Column(
        db.String(50),
        default="India"
    )

    template = db.Column(
        db.String(50),
        default="classic"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<Resume {self.full_name}>"