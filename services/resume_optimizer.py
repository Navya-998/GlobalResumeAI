import re


SUGGESTIONS = {

    "wallix":
        "Mention your experience with Wallix PAM.",

    "cyberark":
        "Add CyberArk if you have worked on it.",

    "active directory":
        "Mention Active Directory administration.",

    "windows":
        "Include Windows Server knowledge.",

    "linux":
        "Mention Linux administration.",

    "rbac":
        "Include Role Based Access Control (RBAC).",

    "servicenow":
        "Mention ServiceNow ticket handling.",

    "powershell":
        "Mention PowerShell scripting.",

    "sql":
        "Mention SQL skills.",

    "python":
        "Mention Python programming."

}


def optimize_resume(found, missing):

    tips = []

    for keyword in missing:

        keyword = keyword.lower()

        if keyword in SUGGESTIONS:

            tips.append(SUGGESTIONS[keyword])

        else:

            tips.append(

                f"Try adding experience related to '{keyword}'."

            )

    estimated_score = min(

        100,

        len(found) * 10 + len(tips) * 5

    )

    return {

        "tips": tips,

        "estimated_score": estimated_score

    }