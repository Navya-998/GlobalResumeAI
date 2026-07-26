PAM_KEYWORDS = [
    "CyberArk",
    "BeyondTrust",
    "Delinea",
    "ARCON",
    "Wallix",
    "Hashicorp Vault",
    "Active Directory",
    "Azure AD",
    "Windows",
    "Linux",
    "PowerShell",
    "ServiceNow",
    "ITIL",
    "Password Vault",
    "MFA",
    "SSH",
    "RDP",
    "PAM",
    "IAM"
]


def calculate_ats(resume):

    score = 0

    found = []

    text = f"""
    {resume.summary}
    {resume.skills}
    {resume.projects}
    {resume.experience}
    {resume.pam_skills}
    """

    text = text.lower()

    for keyword in PAM_KEYWORDS:

        if keyword.lower() in text:

            found.append(keyword)

            score += 5

    score = min(score, 100)

    missing = [
        keyword
        for keyword in PAM_KEYWORDS
        if keyword not in found
    ]

    return {

        "score": score,

        "found": found,

        "missing": missing

    }