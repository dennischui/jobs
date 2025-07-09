class JobLink:
    def __init__(self, company, url):
        self.company = company
        self.url = url

    def fetch_jobs(self):
        raise NotImplementedError("Subclasses should implement this")