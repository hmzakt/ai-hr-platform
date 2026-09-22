from __future__ import annotations


class ResumeUnderstandingError(Exception):
    """Base exception for resume understanding."""


class EmptyResumeError(ResumeUnderstandingError):
    """Raised when the parsed resume contains no usable text."""