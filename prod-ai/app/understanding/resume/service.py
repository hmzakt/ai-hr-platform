from __future__ import annotations

from app.parsing.models.parsed_document import ParsedDocument
from app.schemas.candidate.profile import CandidateProfile

from .exceptions import EmptyResumeError


class ResumeUnderstandingService:

    def __init__(
        self,
        prompt_registry,
        llm_service,
    ) -> None:
        self.prompt_registry = prompt_registry
        self.llm_service = llm_service

    def understand(
        self,
        document: ParsedDocument,
    ) -> CandidateProfile:

        resume_text = self._prepare_resume(document)
        prompt = self._build_prompt(resume_text)
        return self._extract_candidate(prompt)

    def _prepare_resume(
        self,
        document: ParsedDocument,
    ) -> str:

        text = document.cleaned_text.strip()

        if not text:
            raise EmptyResumeError(
                "Resume contains no usable text."
            )

        return text

    def _build_prompt(
        self,
        resume_text: str,
    ) -> str:
        schema = CandidateProfile.model_json_schema()
        return self.prompt_registry.render(
            "resume_understanding",
            resume=resume_text,
            schema = schema
        )

    def _extract_candidate(
        self,
        prompt: str,
    ) -> CandidateProfile:

        return self.llm_service.invoke(
            prompt=prompt,
            response_model=CandidateProfile,
        )