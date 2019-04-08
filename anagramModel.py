
from google.appengine.ext import ndb;

class anagramModel(ndb.Model):
    aKey = ndb.StringProperty()
    User = ndb.StringProperty()
    wordList = ndb.StringProperty(repeated=True)
    wordCount = ndb.IntegerProperty()
    letterCount = ndb.IntegerProperty()


