import re

TECH_KEYWORDS = [

    # PAM
    "CyberArk",
    "Wallix",
    "BeyondTrust",
    "ARCON",
    "Delinea",
    "Hashicorp Vault",
    "PAM",
    "Privileged Access Management",

    # Identity
    "Active Directory",
    "Entra ID",
    "LDAP",
    "RBAC",
    "MFA",
    "SSO",

    # Operating Systems
    "Windows",
    "Linux",
    "Unix",

    # Security
    "Vaulting",
    "Password Rotation",
    "Session Management",
    "Audit",
    "Authentication",
    "Authorization",

    # Infrastructure
    "Server",
    "Network",
    "Firewall",

    # ITSM
    "ServiceNow",

    # Data
    "Python",
    "SQL",
    "Excel",
    "Power BI",
    "Tableau",

    # Cloud
    "AWS",
    "Azure",
    "Docker",
    "Kubernetes"
]


def job_match(resume, job_description):

    resume_text = " ".join([
        str(resume.summary or ""),
        str(resume.education or ""),
        str(resume.experience or ""),
        str(resume.skills or ""),
        str(resume.projects or ""),
        str(resume.certifications or ""),
        str(resume.custom_sections or "")
    ]).lower()

    jd = job_description.lower()

    found = []
    missing = []

    jd_keywords = []

    for keyword in TECH_KEYWORDS:

        if keyword.lower() in jd:
            jd_keywords.append(keyword)

    if not jd_keywords:
        return {
            "score": 0,
            "found": [],
            "missing": []
        }

    for keyword in jd_keywords:

        if keyword.lower() in resume_text:
            found.append(keyword)
        else:
            missing.append(keyword)

    score = round((len(found) / len(jd_keywords)) * 100)

    return {
        "score": score,
        "found": found,
        "missing": missing
    }