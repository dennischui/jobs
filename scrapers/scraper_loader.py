import importlib

def load_scraper_class(company_name):
    module_name = f"scrapers.{company_name.lower()}"
    class_name = f"{company_name}Link"
    try:
        module = importlib.import_module(module_name)
        return getattr(module, class_name)
    except (ModuleNotFoundError, AttributeError):
        raise NotImplementedError(f"No scraper class defined for company '{company_name}'")