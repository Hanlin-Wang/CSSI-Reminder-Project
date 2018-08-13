from google.appengine.ext import ndb

class ReminderData(ndb.Model):
    optionwater = ndb.BooleanProperty(required=False)
    optionshave = ndb.BooleanProperty(required=False)
    optionsleep = ndb.BooleanProperty(required=False)
    watertime = ndb.StringProperty(required=False)
    shavetime = ndb.StringProperty(required=False)
    sleeptime = ndb.StringProperty(required=False)
