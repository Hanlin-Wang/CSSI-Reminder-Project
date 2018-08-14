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

class CssiUser(ndb.Model):
  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()

class UsernameHandler(webapp2.RequestHandler):
    def get(self):
        Username_template=the_jinja_env.get_template('templates/Username.html')
        self.response.write(Username_template.render())
    def post(self):
        global username
        username=self.request.get('user-name')

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
        if optionshower:
            optionshower=True
            showertime=self.request.get('ShowerTime')
        if not optionshower:
            optionshower=False
            showertime=None
        if optiongym:
            optiongym=True
            gymtime=self.request.get('GymTime')
        if not optiongym:
            optiongym=False
            gymtime=None
        if optioneat:
            optioneat=True
            optiontime=self.request.get('EatTime')
        if not optioneat:
            optioneat=False
            gymtime=None



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
            "username": username
            }
        useroptions_key = Options(optionwater= optionwater,optionshave= optionshave,optionsleep= optionsleep,optionshower= optionshower,optiongym= optiongym, optioneat=optioneat).put()
        usertime_key = Time(watertime = watertime,shavetime = shavetime,sleeptime = sleeptime,showertime= showertime, gymtime= gymtime, eattime= eattime).put()

        ReminderData(options=useroptions_key ,time=usertime_key,username=username).put()


        all_data = ReminderData.query().fetch()
        alldata_dict=[]
        for reminder in all_data:
            rdict={}
            rdict["username"]=reminder.username

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
            timeDict["showertime"]=time.showertime
            timeDict["gymtime"]=time.gymtime
            timeDict["eattime"]=time.eattime
            rdict["times"] = timeDict
            alldata_dict.append(rdict)

            # for option in reminder.options:
            #     optionObj = option.get()
            #     optionDict = {}
            #     optionDict["optionwater"]=optionObj.optionwater
            #     optionDict["optionshave"]=optionObj.optionshave
            #     optionDict["optionsleep"]=optionObj.optionsleep
            #     rdict["options"].append(optionDict)
            # for time in times.options:
            #     timeObj = time.get()
            #     timeDict = {}
            #     timeDict["watertime"]=timeObj.watertime
            #     timeDict["shavetime"]=timeObj.shavetime
            #     timeDict["sleeptime"]=timeObj.sleeptime
            #     rdict["times"].append(timeDict)

        # Data_as_json=json.loads(all_data)
        # def set_default(obj):
        #     if isinstance(obj, set):
        #         return list(obj)
        #     raise TypeError

        # Data_as_Json=json.dumps(all_data, default=set_default)
        # var_dict = {'data': Data_as_Json}
        self.response.write(alldata_dict)
        self.response.write(type(all_data))
        # # all_data = json.dumps(all_data)
        # # loaded_data = json.loads(all_data)
        # # var_dict = {'data': loaded_data}
        #  #Output 3.5
        #
        #
        #
        # Event_template=the_jinja_env.get_template('templates/Event.html')
        # self.response.write(Event_template.render(var_dict))


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
