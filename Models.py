from google.appengine.ext import ndb

class ReminderData(ndb.Model):
    optionwater = ndb.BooleanProperty(required=False)
    optionshave = ndb.BooleanProperty(required=False)
    optionsleep = ndb.BooleanProperty(required=False)
