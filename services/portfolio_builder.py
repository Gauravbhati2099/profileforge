from pathlib import Path

from jinja2 import (
    Environment,
    FileSystemLoader
)

from models.profile import Profile


def build_portfolio(
    profile: Profile
):

    env = Environment(
        loader=FileSystemLoader(
            "templates"
        )
    )

    template = env.get_template(
        "portfolio.html"
    )

    html = template.render(
        profile=profile
    )

    output_path = (
        Path("output")
        / "index.html"
    )

    output_path.write_text(
        html,
        encoding="utf-8"
    )

    return output_path