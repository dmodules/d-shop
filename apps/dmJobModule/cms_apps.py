
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

class JobApp(CMSApp):
    app_name = "dmjobmodule"  # must match the application namespace
    name = "Job Module Apphook"

    def get_urls(self, page=None, language=None, **kwargs):
        return ['apps.dmJobModule.cms_urls']


apphook_pool.register(JobApp)
