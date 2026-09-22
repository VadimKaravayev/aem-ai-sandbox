from enum import Enum

from pydantic import BaseModel, Field


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AemDiagnostic(BaseModel):
    summary: str
    likely_cause: str
    severity: Severity
    evidence: list[str] = Field(
        min_length=1,
        description=(
            "Verbatim lines from the supplied diagnostic context that support the cause. "
            "Do not paraphrase and do not add facts absent from the context."
        ),
    )
    suggested_actions: list[str]
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description=(
            "Your own certainty in this diagnosis, 0.0-1.0. "
            "Lower it when the supplied context is insufficient."
        ),
    )

class DiagnosticRequest(BaseModel):
    context: str = Field(
        min_length=1,
        description="Raw AEM diagnostic context: log lines, bundle state, console output",
    )
