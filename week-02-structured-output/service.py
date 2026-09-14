from openai import OpenAI

from contracts import AemDiagnostic

client = OpenAI()

INSTRUCTIONS = (
    "You are an assistant that helps developers working with "
    "Adobe Experience Manager (AEM). You diagnose a single reported problem "
    "from the diagnostic context supplied with the request.\n"
    "\n"
    "Ground every part of the diagnosis in that context. Quote evidence "
    "verbatim from it; never paraphrase it and never introduce facts, log "
    "lines, versions or component names that do not appear in it.\n"
    "\n"
    "Name the single most probable cause rather than listing possibilities. "
    "Judge severity by the impact on the running instance, not by how hard "
    "the fix is. Suggest only actions the context actually supports — if it "
    "supports none, suggest nothing rather than inventing a plausible step.\n"
)

class DiagnosticUnavailable(Exception):
    """The model did not return a usable AemDiagnostic."""

def diagnose(context: str) -> AemDiagnostic:
    response = client.responses.parse(
        model="gpt-5.6-luna",
        instructions=INSTRUCTIONS,
        input=f"Diagnostic context:\n{context}",
        text_format=AemDiagnostic,
    )
    diagnostic = response.output_parsed
    if diagnostic is None:
        raise DiagnosticUnavailable(f"no parsed output (status={response.status})")
    return diagnostic
