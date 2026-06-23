from models.profile import Profile
from models.warning import ValidationWarning


BAD_HEADLINES = {
    "Professional",
    "Engineer",
    "Student",
    "Developer"
}


def validate_profile(
    profile: Profile
) -> list[ValidationWarning]:

    warnings = []

    # Headline

    if (
        profile.headline
        and profile.headline.strip()
        in BAD_HEADLINES
    ):

        warnings.append(
            ValidationWarning(
                field="headline",
                severity="warning",
                message="Generic headline detected",
                suggestion=(
                    "AI Engineer & Backend Developer"
                )
            )
        )

    # Email

    if not profile.contact.email:

        warnings.append(
            ValidationWarning(
                field="contact.email",
                severity="error",
                message="Email missing"
            )
        )

    # Phone

    if not profile.contact.phone:

        warnings.append(
            ValidationWarning(
                field="contact.phone",
                severity="warning",
                message="Phone number missing"
            )
        )

    # GitHub

    if not profile.github:

        warnings.append(
            ValidationWarning(
                field="github",
                severity="info",
                message="GitHub profile not found"
            )
        )

    # LinkedIn

    if not profile.linkedin:

        warnings.append(
            ValidationWarning(
                field="linkedin",
                severity="info",
                message="LinkedIn profile not found"
            )
        )

    # Projects

    for i, project in enumerate(
    profile.projects
):

        if (len(project.description)< 25):
            warnings.append(
                ValidationWarning(
                    field=f"projects[{i}]",
                    severity="warning",
                    message=(
                        "Project description may be too short"
                    ),
                    suggestion=(
                        "Describe project functionality and impact"
                    )
                )
            )

    # Experience

    if len(profile.experience) == 0:

        warnings.append(
            ValidationWarning(
                field="experience",
                severity="warning",
                message="No experience found"
            )
        )

    # Profile image

    if not profile.profile_image:

        warnings.append(
            ValidationWarning(
                field="profile_image",
                severity="info",
                message="Profile image missing",
                suggestion=(
                    "Upload a professional profile image"
                )
            )
        )

    if not profile.achievements:
        warnings.append(
            ValidationWarning(
                field="achievements",
                severity="info",
                message="No achievements found",
                suggestion=(
                    "Add notable achievements, awards, or recognitions"
                )
            )
        )
    return warnings

def calculate_completeness_score(
    profile
) -> int:

    score = 0

    if profile.name:
        score += 10

    if profile.contact.email:
        score += 10

    if profile.contact.phone:
        score += 10

    if profile.summary:
        score += 10

    if profile.github:
        score += 10

    if profile.linkedin:
        score += 10

    if profile.skills:
        score += 10

    if profile.projects:
        score += 15

    if profile.experience:
        score += 15

    return min(
        score,
        100
    )

BAD_HEADLINES = {
    "Professional",
    "Engineer",
    "Student",
    "Developer"
}


def calculate_quality_score(
    profile
) -> int:

    score = 100

    if (
        profile.headline
        and profile.headline.strip()
        in BAD_HEADLINES
    ):
        score -= 10

    if not profile.profile_image:
        score -= 5

    if not profile.achievements:
        score -= 5

    for project in profile.projects:

        if (
            len(
                project.description
            )
            < 25
        ):
            score -= 3

    return max(
        score,
        0
    )

def calculate_overall_score(
    profile
):

    completeness = (
        calculate_completeness_score(
            profile
        )
    )

    quality = (
        calculate_quality_score(
            profile
        )
    )

    overall = int(
        (
            completeness
            + quality
        ) / 2
    )

    return {
        "completeness_score":
            completeness,

        "quality_score":
            quality,

        "overall_score":
            overall
    }