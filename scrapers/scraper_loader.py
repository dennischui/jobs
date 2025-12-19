import importlib
from scrapers.base_scraper import BaseScraper
def load_scraper_class(company_name) -> BaseScraper:
    module_name = f"scrapers.{company_name.lower()}_scraper"
    class_name = f"{''.join([i[0].upper()+i[1:] for i in company_name.split('_')])}Scraper"
    print(f"{class_name=}")
    try:
        module = importlib.import_module(module_name)
        return getattr(module, class_name)
    except (ModuleNotFoundError, AttributeError):
        raise NotImplementedError(f"No scraper class defined for company '{company_name}'")