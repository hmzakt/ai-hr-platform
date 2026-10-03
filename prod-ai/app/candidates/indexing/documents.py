from __future__ import annotations

from app.embeddings.models import (
    EmbeddingDocument,
    EmbeddingSourceType,
)
from app.schemas.candidate.profile import CandidateProfile


class CandidateEmbeddingBuilder:

    def build(
        self,
        candidate: CandidateProfile,
        candidate_id: str,
    ) -> list[EmbeddingDocument]:

        documents: list[EmbeddingDocument] = []

        documents.extend(
            self._build_experience_documents(
                candidate,
                candidate_id,
            )
        )

        documents.extend(
            self._build_project_documents(
                candidate,
                candidate_id,
            )
        )

        documents.extend(
            self._build_skill_document(
                candidate,
                candidate_id,
            )
        )

        documents.extend(
            self._build_education_documents(
                candidate,
                candidate_id,
            )
        )

        return documents

    def _build_experience_documents(
        self,
        candidate: CandidateProfile,
        candidate_id: str,
    ) -> list[EmbeddingDocument]:

        documents = []

        for index, experience in enumerate(
            candidate.experience
        ):

            text = self._experience_to_text(
                 experience
            )

            documents.append(
                EmbeddingDocument(
                    id=f"{candidate_id}:experience:{index}",
                    text=text,
                    source_type=EmbeddingSourceType.EXPERIENCE,
                    candidate_id=candidate_id,
                    source_id=str(index),
                    metadata={
                    "candidate_id": candidate_id,
                    "source_type": "experience",                        },
                    )
                )
        return documents

    @staticmethod
    def _experience_to_text(
        experience,
    ) -> str:

        parts = [
            f"Job title: {experience.title}",
            f"Company: {experience.company}",
        ]

        if experience.responsibilities:
            parts.append(
                "Responsibilities: "
                + " ".join(
                    experience.responsibilities
                )
            )

        if experience.achievements:
            parts.append(
                "Achievements: "
                + " ".join(
                    experience.achievements
                )
            )

        return "\n".join(parts)

    def _build_project_documents(
        self,
        candidate: CandidateProfile,
        candidate_id: str,
    ) -> list[EmbeddingDocument]:

        documents = []

        for index, project in enumerate(
            candidate.projects
        ):

            parts = [
                f"Project: {project.title}",
                f"Description: {project.description}",
            ]

            if project.role:
                parts.append(
                    f"Role: {project.role}"
                )

            if project.highlights:
                parts.append(
                    "Highlights: "
                    + " ".join(project.highlights)
                )

            if project.outcomes:
                parts.append(
                    "Outcomes: "
                    + " ".join(project.outcomes)
                )

            text = "\n".join(parts)

            documents.append(
                EmbeddingDocument(
                    id=f"{candidate_id}:project:{index}",
                    text=text,
                    source_type=EmbeddingSourceType.PROJECT,
                    candidate_id=candidate_id,
                    source_id=str(index),
                    metadata={
                        "candidate_id": candidate_id,
                        "source_type": "project",
                    },
                )
            )

        return documents

    def _build_skill_document(
        self,
        candidate: CandidateProfile,
        candidate_id: str,
    ) -> list[EmbeddingDocument]:

        if not candidate.skills:
            return []

        skill_text = (
            "Candidate skills: "
            + ", ".join(
                str(skill)
                for skill in candidate.skills
            )
        )

        return [
            EmbeddingDocument(
                id=f"{candidate_id}:skills",
                text=skill_text,
                source_type=EmbeddingSourceType.SKILL,
                candidate_id=candidate_id,
                source_id="skills",
                metadata={
                    "candidate_id": candidate_id,
                    "source_type": "skill",
                },
            )
        ]