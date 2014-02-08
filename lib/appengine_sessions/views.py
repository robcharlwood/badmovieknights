# import python deps
from datetime import datetime

# import package deps
from appengine_sessions.mapper import DeleteMapper
from appengine_sessions.models import Session

# import django deps
from django.http import HttpResponse
from django.views.generic.base import View


# cron to clean up sessions that have expired
class SessionCleanUpCron(View):
    """
        View used by cron to clear sessions that have expired
    """
    def get(self, request, *args, **kwargs):
        mapper = DeleteMapper(
            Session,
            filters={
                'lt': ('expire_date', datetime.utcnow())
            })
        mapper.start()
        return HttpResponse('Session cleaner mapper started')

# initialise the view
session_clean_up = SessionCleanUpCron.as_view()
