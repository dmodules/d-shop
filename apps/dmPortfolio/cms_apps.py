
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

class PortfolioApp(CMSApp):
    app_name = "dmportfolio"  # must match the application namespace
    name = "Portfolio Apphook"

    def get_urls(self, page=None, language=None, **kwargs):
        return ['apps.dmPortfolio.cms_urls']


apphook_pool.register(PortfolioApp)
