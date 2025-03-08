from pydantic import BaseModel, EmailStr
from typing import List

class PersonalInformation(BaseModel):
    name: str
    email: EmailStr
    phone: str
    location: str

class Education(BaseModel):
    degree: str
    institution: str
    start_date: str
    end_date: str

class Qualification(BaseModel):
    certification: str
    issuer: str
    date: str

class Skills(BaseModel):
    technical: List[str]
    soft: List[str]

class WorkExperience(BaseModel):
    job_title: str
    company: str
    start_date: str
    end_date: str
    responsibilities: List[str]

class Project(BaseModel):
    title: str
    description: List[str]
    technologies: List[str]

class CV(BaseModel):
    personal_information: PersonalInformation
    education: List[Education]
    qualifications: List[Qualification]
    skills: Skills
    work_experience: List[WorkExperience]
    projects: List[Project]

    def to_google_sheet_format(self):
        return [
            self.personal_information.email,
            self.personal_information.phone,
            self.personal_information.location,
            "\n\n".join([f"{edu.degree} at {edu.institution} ({edu.start_date} - {edu.end_date})" for edu in self.education]),
            "\n\n".join([f"{qual.certification} from {qual.issuer} ({qual.date})" for qual in self.qualifications]),
            f"Technical: {', '.join(self.skills.technical)} | Soft: {', '.join(self.skills.soft)}",
            "\n\n".join([f"{work.job_title} at {work.company} ({work.start_date} - {work.end_date}): {', '.join(work.responsibilities)}" for work in self.work_experience]),
            "\n\n".join([f"{proj.title}: {', '.join(proj.description)} (Tech: {', '.join(proj.technologies)})" for proj in self.projects]),
        ]
