from fastapi import FastAPI, HTTPException

from contracts import AemDiagnostic, DiagnosticRequest
from service import diagnose, DiagnosticUnavailable

app = FastAPI()

@app.post("/diagnose")
def create_diagnostic(request: DiagnosticRequest) -> AemDiagnostic:
    try:
        return diagnose(request.context)
    except DiagnosticUnavailable as e:
        raise HTTPException(status_code=502, detail=str(e)) from e
