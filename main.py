import json

from extractors.loader import load_file
from services.extractor import extract_profile
from services.normalizer import normalize_profile
from models.profile import Profile
from services.profile_validator import (
    validate_profile,
    calculate_overall_score
)
from services.portfolio_builder import (
    build_portfolio
)

# Extract text from resume
resume_text = load_file(
    "resume/resume.pdf"
)

# LLM extraction
profile_json = extract_profile(
    resume_text
)

# Convert JSON string -> dict
raw_data = json.loads(
    profile_json
)

# Normalize
normalized = normalize_profile(
    raw_data
)

# Validate
profile = Profile.model_validate(
    normalized
)

warnings = validate_profile(
    profile
)

scores = (
    calculate_overall_score(
        profile
    )
)

review_data = {

    **scores,

    "warnings": [

        warning.model_dump()

        for warning in warnings
    ]
}

with open(
    "output/warnings.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        review_data,
        f,
        indent=2
    )

print("\n===== PROFILE REVIEW =====")

print(
    f"Overall Score      : {scores['overall_score']}/100"
)

print(
    f"Completeness Score : {scores['completeness_score']}/100"
)

print(
    f"Quality Score      : {scores['quality_score']}/100"
)

print("\nWarnings:")

for warning in warnings:

    print(
        f"- [{warning.severity.upper()}] "
        f"{warning.message}"
    )

print()


# Save
with open(
    "output/profile.json",
    "w",
    encoding="utf-8"
) as f:

    f.write(
        profile.model_dump_json(
            indent=2
        )
    )

print(
    "✓ Profile saved to output/profile.json"
)

portfolio_path = build_portfolio(
    profile
)

print(
    f"✓ Portfolio generated: {portfolio_path}"
)