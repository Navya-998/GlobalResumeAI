def generate_summary(name, role, experience):

    if not role:
        role = "Professional"

    if not experience:
        experience = "0"

    summary = f"""
{name} is a motivated {role} with {experience} years of experience.

Possesses strong analytical thinking, communication skills, teamwork, and problem-solving abilities.

Dedicated to delivering high-quality work while continuously learning new technologies and industry best practices.

Seeking opportunities to contribute effectively and grow professionally within a dynamic organization.
"""

    return summary.strip()