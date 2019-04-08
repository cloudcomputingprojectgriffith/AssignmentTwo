from google.appengine.ext import ndb


class MyUser(ndb.Model):
    username = ndb.StringProperty()
    wc = ndb.IntegerProperty()
    ac = ndb.IntegerProperty()

