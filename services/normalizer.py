from typing import Any
from datetime import datetime


def normalize_experience(
    exp: dict[str, Any]
) -> dict[str, Any]:

    role = (
        exp.get("role")
        or exp.get("title")
        or exp.get("position")
        or exp.get("job_title")
        or ""
    )

    company = exp.get(
        "company",
        ""
    )

    start_date = None
    end_date = None

    dates = (
        exp.get("dates")
        or exp.get("duration")
    )

    if dates and isinstance(dates, str):

        separators = [
            "–",
            "—",
            "-",
            " to "
        ]

        for sep in separators:

            if sep in dates:

                parts = dates.split(
                    sep,
                    maxsplit=1
                )

                if len(parts) == 2:

                    start_date = (
                        parts[0].strip()
                    )

                    end_date = (
                        parts[1].strip()
                    )

                break

    return {
        "company": company,
        "role": role,
        "start_date": (
            start_date
            or exp.get("start_date")
        ),
        "end_date": (
            end_date
            or exp.get("end_date")
        ),
        "location": exp.get(
            "location"
        ),
        "description": exp.get(
            "description",
            ""
        ),
        "technologies": (
            exp.get(
                "technologies"
            )
            or []
        )
    }


def normalize_project(
    project: dict[str, Any]
) -> dict[str, Any]:

    technologies = (
        project.get("technologies")
        or project.get("tech_stack")
        or project.get("skills")
        or []
    )

    return {
        "name": (
            project.get("name")
            or project.get("title")
            or project.get("project_name")
            or ""
        ),
        "description": project.get(
            "description",
            ""
        ),
        "technologies": technologies,
        "tags": technologies,
        "github_url": project.get(
            "github_url"
        ),
        "live_url": project.get(
            "live_url"
        ),
        "image_url": project.get(
            "image_url"
        )
    }


def normalize_education(
    edu: dict[str, Any]
) -> dict[str, Any]:

    return {
        "institution": edu.get(
            "institution",
            ""
        ),
        "degree": (
            edu.get("degree")
            or edu.get("title")
            or edu.get("program")
            or ""
        ),
        "field_of_study": (
            edu.get(
                "field_of_study"
            )
        ),
        "start_date": (
            edu.get(
                "start_date"
            )
        ),
        "end_date": (
            edu.get("end_date")
            or edu.get(
                "year"
            )
            or edu.get(
                "graduation_year"
            )
            or edu.get(
                "expectedGraduationDate"
            )
        ),
        "grade": edu.get(
            "grade"
        )
    }


def normalize_skill(
    skill: Any
) -> dict[str, Any] | None:

    if isinstance(
        skill,
        str
    ):

        skill = skill.strip()

        if skill:

            return {
                "name": skill,
                "category": None
            }

    elif isinstance(
        skill,
        dict
    ):

        return {
            "name": (
                skill.get("name")
                or ""
            ),
            "category": skill.get(
                "category"
            )
        }

    return None


def normalize_skills(
    skills: list[Any]
) -> list[dict[str, Any]]:

    normalized = []
    seen = set()

    for skill in skills:

        item = normalize_skill(
            skill
        )

        if not item:
            continue

        key = item["name"]

        if key in seen:
            continue

        seen.add(key)

        normalized.append(
            item
        )

    return normalized


def normalize_certifications(
    certifications: list[Any]
) -> list[dict[str, Any]]:

    normalized = []

    for cert in certifications:

        if isinstance(
            cert,
            str
        ):

            normalized.append(
                {
                    "title": cert,
                    "issuer": None
                }
            )

        elif isinstance(
            cert,
            dict
        ):

            normalized.append(
                {
                    "title": (
                        cert.get(
                            "title"
                        )
                        or cert.get(
                            "name"
                        )
                        or ""
                    ),
                    "issuer": cert.get(
                        "issuer"
                    ),
                    "issued_date": cert.get(
                        "issued_date"
                    ),
                    "credential_id": cert.get(
                        "credential_id"
                    )
                }
            )

    return normalized


def normalize_achievements(
    achievements: list[Any]
) -> list[dict[str, Any]]:

    normalized = []

    for item in achievements:

        if isinstance(
            item,
            str
        ):

            normalized.append(
                {
                    "title": item,
                    "description": None
                }
            )

        elif isinstance(
            item,
            dict
        ):

            normalized.append(
                {
                    "title": (
                        item.get(
                            "title"
                        )
                        or ""
                    ),
                    "description": item.get(
                        "description"
                    )
                }
            )

    return normalized


def normalize_profile(
    data: dict[str, Any]
) -> dict[str, Any]:

    return {

        "name": data.get(
            "name",
            ""
        ),

        "headline": (
            data.get(
                "headline"
            )
            or "Professional"
        ),

        "summary": data.get(
            "summary"
        ),

        "location": data.get(
            "location"
        ),

        "profile_image": data.get(
            "profile_image"
        ),

        "contact": {
            "email": data.get(
                "email"
            ),
            "phone": data.get(
                "phone"
            )
        },

        "github": data.get(
            "github"
        ),

        "linkedin": data.get(
            "linkedin"
        ),

        "website": data.get(
            "website"
        ),

        "links": data.get(
            "links",
            []
        ),

        "skills": normalize_skills(
            data.get(
                "skills",
                []
            )
        ),

        "experience": [
            normalize_experience(
                exp
            )
            for exp in data.get(
                "experience",
                []
            )
        ],

        "projects": [
            normalize_project(
                project
            )
            for project in data.get(
                "projects",
                []
            )
        ],

        "education": [
            normalize_education(
                edu
            )
            for edu in data.get(
                "education",
                []
            )
        ],

        "certifications":
            normalize_certifications(
                data.get(
                    "certifications",
                    []
                )
            ),

        "achievements":
            normalize_achievements(
                data.get(
                    "achievements",
                    []
                )
            ),

        "publications":
            data.get(
                "publications",
                []
            ),

        "metadata": {
            "source_file":
                data.get(
                    "source_file"
                ),
            "generated_at":
                datetime.utcnow().isoformat(),
            "version": "1.0"
        }
    }
