from pydantic import ValidationError

from service import diagnose
from contracts import Severity, AemDiagnostic

# Define the escalation policy as a module-level
# constant - a set, not list

ESCALATE = {Severity.HIGH, Severity.CRITICAL}

CONTEXT = """                                                                                                                                                               
  Environment: AEM as a Cloud Service SDK, local author instance, version 2026.6.                                                                                               
                                                                                                                                                                                
  /system/console/bundles                                                                                                                                                       
    com.devhandler.aem.translation.core (1.4.0-SNAPSHOT) — state: Installed                                                                                                     
                                                                                                                                                                                
  Bundle detail, unsatisfied requirement:                                                                                                                                       
    org.apache.commons.lang3,version=[3.20,4) -- Cannot be resolved                                                                                                             
                                                                                                                                                                                
  error.log                                                                                                                                                                     
    *ERROR* [FelixStartLevel] com.devhandler.aem.translation.core Bundle                                                                                                        
    com.devhandler.aem.translation.core [612] cannot be resolved                                                                                                                
                                                                                                                                                                                
  The service that should be running:                                                                                                                                           
    @Component(service = TranslationRulesService.class)                                                                                                                         
    public class TranslationRulesServiceImpl implements TranslationRulesService { ... }                                                                                         
                                                                                                                                                                                
  /system/console/components does not list TranslationRulesServiceImpl at all.                                                                                                  
  """


diagnostic = diagnose(CONTEXT)
escalate = diagnostic.severity in ESCALATE

print(f"Summary: {diagnostic.summary}")
print(f"Likely cause: {diagnostic.likely_cause}")
print(f"Severity: {diagnostic.severity.value}")
print(f"Confidence {diagnostic.confidence:.2f}")

if escalate:
    print(f"\n[ESCALATE] severity '{diagnostic.severity.value}' requires a human owner")
else:
    print(f"\n[OK] severity '{diagnostic.severity.value}' can be handled by the reporter")

print("\nSuggested actions:")
if diagnostic.suggested_actions:
    for i, action in enumerate(diagnostic.suggested_actions, start=1):
        print(f" {i}. {action}")
else:
    print(" none - the context does not support a remediation step")


BAD_PAYLOAD = {
    "summary": "Bundle cannot be resolved",
    "likely_cause": "Missing package export",
    "severity": "high",
    "evidence": [],
    "confidence": 1.4,
    "suggested_actions": [],
}

print("\nValidating a hand-built bad payload:")

try:
    AemDiagnostic.model_validate(BAD_PAYLOAD)
    print(" accepted - the contract did not catch it")
except ValidationError as e:
    print(f"   [REJECTED] {e}")
