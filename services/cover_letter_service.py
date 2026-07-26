def generate_cover_letter(resume, company="", position=""):

    return f"""
Dear Hiring Manager,

I am excited to apply for the {position if position else "position"} at {company if company else "your company"}.

My background includes:

{resume.summary}

Key Skills:
{resume.skills}

Professional Experience:
{resume.experience}

I am confident that my technical knowledge, problem-solving skills and passion for learning will allow me to contribute effectively to your team.

Thank you for your time and consideration. I look forward to hearing from you.

Sincerely,

{resume.full_name}
"""