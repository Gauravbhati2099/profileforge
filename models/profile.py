from typing import Optional

from pydantic import BaseModel, Field


class Link(BaseModel):
    label: str
    url: str


class Contact(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None


class Certification(BaseModel):
    title: str
    issuer: Optional[str] = None
    issued_date: Optional[str] = None
    credential_id: Optional[str] = None


class Skill(BaseModel):
    name: str
    category: Optional[str] = None


class Experience(BaseModel):
    company: str
    role: str

    start_date: Optional[str] = None
    end_date: Optional[str] = None

    location: Optional[str] = None

    description: Optional[str] = None

    technologies: list[str] = Field(
        default_factory=list
    )


class Project(BaseModel):
    name: str

    description: str

    technologies: list[str] = Field(
        default_factory=list
    )

    tags: list[str] = Field(
        default_factory=list
    )

    github_url: Optional[str] = None

    live_url: Optional[str] = None

    image_url: Optional[str] = None


class Education(BaseModel):
    institution: str

    degree: str

    field_of_study: Optional[str] = None

    start_date: Optional[str] = None

    end_date: Optional[str] = None

    grade: Optional[str] = None


class Achievement(BaseModel):
    title: str
    description: Optional[str] = None


class Metadata(BaseModel):
    source_file: Optional[str] = None
    generated_at: Optional[str] = None
    version: str = "1.0"


class Profile(BaseModel):

    # Identity

    name: str

    headline: Optional[str] = None

    summary: Optional[str] = None

    location: Optional[str] = None

    profile_image: Optional[str] = None

    contact: Contact = Field(
        default_factory=Contact
    )

    # Links

    github: Optional[str] = None

    linkedin: Optional[str] = None

    website: Optional[str] = None

    links: list[Link] = Field(
        default_factory=list
    )

    # Content

    skills: list[Skill] = Field(
        default_factory=list
    )

    experience: list[Experience] = Field(
        default_factory=list
    )

    projects: list[Project] = Field(
        default_factory=list
    )

    education: list[Education] = Field(
        default_factory=list
    )

    certifications: list[Certification] = Field(
        default_factory=list
    )

    achievements: list[Achievement] = Field(
        default_factory=list
    )

    publications: list[str] = Field(
        default_factory=list
    )

    # Metadata

    metadata: Metadata = Field(
        default_factory=Metadata
    )
