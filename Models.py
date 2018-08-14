from google.appengine.ext import ndb

class Options(ndb.Model):
    optionwater = ndb.BooleanProperty(required=False)
    optionshave = ndb.BooleanProperty(required=False)
    optionsleep = ndb.BooleanProperty(required=False)
    optionshower = ndb.BooleanProperty(required=False)
    optiongym = ndb.BooleanProperty(required=False)
    optioneat = ndb.BooleanProperty(required=False)


class Time(ndb.Model):
    watertime = ndb.StringProperty(required=False)
    shavetime = ndb.StringProperty(required=False)
    sleeptime = ndb.StringProperty(required=False)
    showertime = ndb.StringProperty(required=False)
    gymtime = ndb.StringProperty(required=False)
    eattime = ndb.StringProperty(required=False)

class ReminderData(ndb.Model):
    options = ndb.KeyProperty(Options)
    time =  ndb.KeyProperty(Time)
