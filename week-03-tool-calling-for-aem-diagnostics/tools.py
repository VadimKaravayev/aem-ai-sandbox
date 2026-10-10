from contracts import BundleStatus, BundleState, ComponentStatus, ComponentState

_BUNDLES: dict[str, BundleStatus] = {
    "com.acme.core": BundleStatus(
        symbolic_name="com.acme.core",
        state=BundleState.ACTIVE,
        version="1.4.2",
        import_problems=[],
    ),
    "com.acme.translation.core": BundleStatus(
        symbolic_name="com.acme.translation.core",
        state=BundleState.INSTALLED,
        version="2.1.0",
        import_problems=["com.acme.translation.api;version=[2.0,3) -- Cannot be resolved"]
    ),
}

_COMPONENTS: dict[str, ComponentStatus] = {
    "com.acme.core.services.impl.SiteConfigServiceImpl": ComponentStatus(
        name="com.acme.core.services.impl.SiteConfigServiceImpl",
        state=ComponentState.ACTIVE,
        unsatisfied_references=[]
    ),
    "com.acme.translation.core.scheduler.TranslationSchedulerJob": ComponentStatus(
        name="com.acme.translation.core.scheduler.TranslationSchedulerJob",
        state=ComponentState.UNSATISFIED_REFENCE,
        unsatisfied_references=["TranslationService (com.acme.translation.api.TranslationService)"]
    )
}

def get_bundle_status(symbolic_name: str) -> BundleStatus:
    bundle = _BUNDLES.get(symbolic_name)
    if bundle is None:
        raise LookupError(f"Bundle not found {symbolic_name}")
    return bundle

def get_component_status(component_name: str) -> ComponentStatus:
    component = _COMPONENTS.get(component_name)
    if component is None:
        raise LookupError(f"Component not found {component_name}")
    return component
