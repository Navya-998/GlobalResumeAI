import re

ATS_KEYWORDS = [
    "python",
    "sql",
    "excel",
    "power bi",
    "tableau",
    "aws",
    "azure",
    "docker",
    "kubernetes",
    "linux",
    "git",
    "github",
    "flask",
    "django",
    "api",
    "rest",
    "machine learning",
    "data analysis",
    "communication",
    "teamwork",
    "problem solving"
]


def calculate_ats_score(resume):

    text = f"""
    {resume.summary}
    {resume.education}
    {resume.experience}
    {resume.skills}
    {resume.projects}
    {resume.certifications}
    {resume.custom_sections}
    """.lower()

    found = []
    missing = []
    suggestions = []

    score = 0

    # ---------- Keyword Score ----------
    for keyword in ATS_KEYWORDS:

        if re.search(rf"\b{re.escape(keyword)}\b", text):

            found.append(keyword)
            score += 3

        else:

            missing.append(keyword)

    # ---------- Section Score ----------
    if resume.summary:
        score += 10
    else:
        suggestions.append("Add a Professional Summary.")

    if resume.education:
        score += 10
    else:
        suggestions.append("Add Education details.")

    if resume.experience:
        score += 15
    else:
        suggestions.append("Add Work Experience.")

    if resume.skills:
        score += 15
    else:
        suggestions.append("Add Skills section.")

    if resume.projects:
        score += 10
    else:
        suggestions.append("Add Projects.")

    if resume.certifications:
        score += 5
    else:
        suggestions.append("Add Certifications.")

    if resume.linkedin:
        score += 5
    else:
        suggestions.append("Add LinkedIn profile.")

    if resume.github:
        score += 5
    else:
        suggestions.append("Add GitHub profile.")

    if len(text.split()) < 200:
        suggestions.append("Increase resume content with measurable achievements.")

    score = min(score, 100)

    return {
        "score": score,
        "found": found,
        "missing": missing,
        "suggestions": suggestions
    }