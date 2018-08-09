from google.appengine.ext import ndb

class ReminderData(ndb.Model):
    optionwater = ndb.StringProperty(required=False)
    optionshave = ndb.StringProperty(required=False)
    optionsleep = ndb.StringProperty(required=False)
