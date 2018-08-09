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
        optionwater = self.request.get('WaterCheckBox')

        if optionwater:
            optionwater=True
            optionshave = request.form.get('Shave')
        if optionshave:
            optionshave=True
            optionsleep = request.form.get('Sleep')
        if optionsleep:
            optionsleep=True

        self.response.write(Home_template.render())


# class DataStore(webapp2.RequestHandler):

        # if optionwater:
        #     optionwater=True
        # optionshave = request.form.get('Shave')
        # if optionshave:
        #     optionshave=True
        # optionsleep = request.form.get('Sleep')
        # if optionsleep:
        #     optionsleep=True
        # self.response.write(optionshave,optionsleep,optionwater)
        # store_variables = ReminderData(optionwater= optionwater, optionshave= optionshave , optionsleep= optionsleep)
        # store_variables.put()
        # variable_dict =  {
        #     "optionwater": optionwater,
        #     "optionshave": optionshave,
        #     "optionsleep": optionsleep
        #                 }
        # self.response.write(Home_template.render(variable_dict))

app=webapp2.WSGIApplication([
('/',UsernameHandler),
('/main', RemindHandler)


],debug=True)
