from service import diagnose

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

print(diagnostic)
print(diagnostic.model_dump_json(indent=2))
