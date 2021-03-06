import webapp2 # NOTE: pull in a library for using appengine
import jinja2
import os
from Models import ReminderData , Options ,Time
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
import json



the_jinja_env=jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True)

# decorator = appengine.OAuth2DecoratorFromClientSecrets(
#    'client_secrets.json',
#    scope='https://www.googleapis.com/auth/calendar')

class CssiUser(ndb.Model):
  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()

class UsernameHandler(webapp2.RequestHandler):
    # @decorator.oauth_required
    def get(self):
        user = users.get_current_user()
        # If the user is logged in...
        if user:
          email_address = user.nickname()
          cssi_user = CssiUser.get_by_id(user.user_id())
          signout_link_html = '<a href="%s">sign out</a>' % (
              users.create_logout_url('/'))
          # If the user has previously been to our site, we greet them!
          if cssi_user:
            self.response.write('''
                Welcome %s %s (%s)! <br> %s <br>''' % (
                  cssi_user.first_name,
                  cssi_user.last_name,
                  email_address,
                  signout_link_html))
          # If the user hasn't been to our site, we ask them to sign up
          else:
            self.response.write('''
                Welcome to our site, %s!  Please sign up! <br>
                <form method="post" action="/Main">
                <input type="text" name="first_name" value="firstname">
                <input type="text" name="last_name" value="lastname">
                <input type="submit">
                </form><br> %s <br>
                ''' % (email_address, signout_link_html))
        # Otherwise, the user isn't logged in!
        else:
          self.response.write('''
            Please log in to use our site! <br>
            <a href="%s">Sign in</a>''' % (
              users.create_login_url('/')))

    def post(self):
        user = users.get_current_user()
        if not user:
          # You shouldn't be able to get here without being logged in
          self.error(500)
          return
          cssi_user = CssiUser(
            first_name=self.request.get('first_name'),
            last_name=self.request.get('last_name'),
            id=user.user_id())
          cssi_user.put()
          self.response.write('Thanks for signing up, %s!' %
            cssi_user.first_name)


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
        all_data = ReminderData.query().fetch()



    def post(self):
        optionwater = self.request.get('WaterCheckBox')
        Event_template=the_jinja_env.get_template('templates/Event.html')
        self.response.write(Event_template.render())

        if optionwater:
            optionwater=True
            watertime=self.request.get('WaterTime')
        if not optionwater:
            optionwater=False
            watertime=None
        optionshave = self.request.get('ShaveCheckBox')
        if optionshave:
            optionshave=True
            shavetime=self.request.get('ShaveTime')
        if not optionshave:
            optionshave=False
            shavetime=None
        optionsleep = self.request.get('SleepCheckBox')
        if optionsleep:
            optionsleep=True
            sleeptime=self.request.get('SleepTime')
        if not optionsleep:
            optionsleep=False
            sleeptime=None
        optionshower = self.request.get('ShowerCheckBox')
        if optionshower:
            optionshower=True
            showertime=self.request.get('ShowerTime')
        if not optionshower:
            optionshower=False
            showertime=None
        optiongym = self.request.get('GymCheckBox')
        if optiongym:
            optiongym=True
            gymtime=self.request.get('GymTime')
        if not optiongym:
            optiongym=False
            gymtime=None
        optioneat = self.request.get('EatCheckBox')
        if optioneat:
            optioneat=True
            eattime=self.request.get('EatTime')
        if not optioneat:
            optioneat=False
            eattime=None




        useroptions_key = Options(optionwater= optionwater,optionshave= optionshave,optionsleep= optionsleep,optionshower= optionshower,optiongym= optiongym, optioneat=optioneat).put()
        usertime_key = Time(watertime = watertime,shavetime = shavetime,sleeptime = sleeptime,showertime= showertime, gymtime= gymtime, eattime= eattime).put()

        ReminderData(options=useroptions_key ,time=usertime_key).put()


        all_data = ReminderData.query().fetch()
        alldata_dict=[]
        for reminder in all_data:
            rdict={}

            options = reminder.options.get()
            optionDict = {}
            optionDict["optionwater"]=options.optionwater
            optionDict["optionshave"]=options.optionshave
            optionDict["optionsleep"]=options.optionsleep
            optionDict["optionshower"]=options.optionshower
            optionDict["optiongym"]=options.optiongym
            optionDict["optioneat"]=options.optioneat
            rdict["options"] = optionDict

            # add the times dictionary
            times = reminder.time.get()
            timeDict = {}
            timeDict["watertime"]=times.watertime
            timeDict["shavetime"]=times.shavetime
            timeDict["sleeptime"]=times.sleeptime
            timeDict["showertime"]=times.showertime
            timeDict["gymtime"]=times.gymtime
            timeDict["eattime"]=times.eattime
            rdict["times"] = timeDict
            alldata_dict.append(rdict)

            # self.response.write(alldata_dict)
            # self.response.write(type(alldata_dict))
            Data_as_Json=json.dumps(alldata_dict)
            # self.response.write(Data_as_Json)
            # self.response.write(Event_template.render({"test": "testing"}))

            variable_dict =  {
                "optionwater": optionwater,
                "optionshave": optionshave,
                "optionsleep": optionsleep,
                "optionshower": optionshower,
                "optiongym": optiongym,
                "optioneat": optioneat,
                "watertime": watertime,
                "shavetime": shavetime,
                "sleeptime": sleeptime,
                "showertime": showertime,
                "gymtime": gymtime,
                "eattime": eattime,
                "sleeptime": sleeptime
                }

            # jQuery.ajax({
            #
            #   url:"Data"
            # }).done(function(response){
            #   alert(response);
            # });



        # Data_as_json=json.loads(all_data)
        # def set_default(obj):
        #     if isinstance(obj, set):
        #         return list(obj)
        #     raise TypeError
        #
        #
        #


        # self.response.write(Data_as_json)
        # for results in trivia_as_json:
        #     for result in trivia_as_json["results"]:
        #        self.response.write(result["question"])
        #        self.response.write("<br>")
        #        self.response.write(result["correct_answer"])
        #        self.response.write("<br><br>")
        #     break





app=webapp2.WSGIApplication([
('/',UsernameHandler),
('/Main',RemindHandler),
('/Data',DataStore)


],debug=True)
