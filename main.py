import webapp2 # NOTE: pull in a library for using appengine
import jinja2
import os
from Models import ReminderData

from google.appengine.api import urlfetch
import json



the_jinja_env=jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True)

class UsernameHandler(webapp2.RequestHandler):
    def get(self):
        Username_template=the_jinja_env.get_template('templates/Username.html')
        self.response.write(Username_template.render())

class RemindHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('This is the home page')
    def post(self):
        Home_template=the_jinja_env.get_template('templates/Home.html')
        self.response.write(Home_template.render())
        optionwater = self.request.get('WaterCheckBox')

class DataStore(webapp2.RequestHandler):
    def get(self):
        Event_template=the_jinja_env.get_template('templates/Event.html')
        self.response.write(Event_template.render())


    def post(self):
        optionwater = self.request.get('WaterCheckBox')

        if optionwater:
            optionwater=True
            watertime=self.request.get('WaterTime')
        if not optionwater:
            optionwater=False
        optionshave = self.request.get('ShaveCheckBox')
        if optionshave:
            optionshave=True
            shavetime=self.request.get('ShaveTime')
        if not optionshave:
            optionshave=False
        optionsleep = self.request.get('SleepCheckBox')
        if optionsleep:
            optionsleep=True
            sleeptime=self.request.get('SleepTime')
        if not optionsleep:
            optionsleep=False
        username=self.request.get("user-name")

        variable_dict =  {
            "optionwater": optionwater,
            "optionshave": optionshave,
<<<<<<< HEAD
            "optionsleep": optionsleep
                        }
        username = ReminderData(
        optionwater= optionwater,
        optionshave=optionshave,
        optionsleep=optionsleep
        )
=======
            "optionsleep": optionsleep,
            "watertime": watertime,
            "shavetime": shavetime,
            "sleeptime": sleeptime
            }

        username = ReminderData(optionwater= optionwater,optionshave=optionshave,optionsleep=optionsleep,watertime= watertime,shavetime=shavetime,sleeptime=sleeptime)
>>>>>>> f4078b8ca83ef7266f4e5240a77f2354fd0b1459
        username.put()





app=webapp2.WSGIApplication([
('/',UsernameHandler),
('/Main',RemindHandler),
('/Data',DataStore)


],debug=True)
