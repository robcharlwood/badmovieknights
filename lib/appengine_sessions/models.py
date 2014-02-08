# import google deps
from google.appengine.ext import ndb


# session model
class Session(ndb.Model):
    session_key = ndb.StringProperty()
    session_data = ndb.TextProperty()
    expire_date = ndb.DateTimeProperty()
