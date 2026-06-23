import json

from extractors.loader import load_file
from services.extractor import extract_profile
from services.normalizer import normalize_profile
from models.profile import Profile


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