from openai import OpenAI

client = OpenAI()

INSTRUCTIONS = (
    "You are an assistant that helps developers working with "
    "Adobe Experience Manager (AEM). Answer accurately and concisely. "
    "If you are unsure or the answer depends on the specific AEM version "
    "or environment, say so rather than guessing."
)

QUESTION = "Why isn't my AEM service working?"


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

ungrounded = client.responses.create(
    model="gpt-5.6-luna",
    instructions=INSTRUCTIONS,
    input=QUESTION
)

print("=== no context ===")
print(ungrounded.output_text)

grounded = client.responses.create(
    model="gpt-5.6-luna",
    instructions=INSTRUCTIONS,
    input=f"{QUESTION}\n\nDiagnostic context: \n{CONTEXT}",
)

print("=== with context ===")
print(grounded.output_text)
