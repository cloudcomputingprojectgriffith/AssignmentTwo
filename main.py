
import os
import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from myuser import MyUser
from anagramModel import anagramModel
from addWord import AddWord
from uploadFile import uploadFile
from subAnagram import subAnagram

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class main(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'


        user = users.get_current_user()

        if user == None:
            template_values = {
                'login_url' : users.create_login_url(self.request.uri)
            }
            template = JINJA_ENVIRONMENT.get_template('mainPage.html')
            self.response.write(template.render(template_values))
            return

        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        if myuser == None:
            myuser = MyUser(id=user.user_id(),username=user.email(),ac=0,wc=0)
            myuser.put()

        anagram = anagramModel.query().fetch()

        template_values = {
            'logout_url' : users.create_logout_url(self.request.uri),
            'user':user,
            'anagram':anagram,
            'ac':myuser.ac,
            'wc':myuser.wc

        }
        template = JINJA_ENVIRONMENT.get_template('home.html')
        self.response.write(template.render(template_values))

    def post(self):

        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')
        if action == 'search':

            user = users.get_current_user()

            searchText = (self.request.get('word')).lower()
            if searchText == "":

                template_values={
                    'user':user,
                    'message': 'Word not found',
                    'anagram': anagramModel.query().fetch()
                    }
                template = JINJA_ENVIRONMENT.get_template('home.html')
                self.response.write(template.render(template_values))
            else:

                lexi = list(searchText.lower())
                sort = sorted(lexi)
                searchW = ''.join(sort)

                anaKey = ndb.Key("anagramModel",user.email()+searchW)
                anagram = anaKey.get()

                myuser_key = ndb.Key('MyUser', user.user_id())
                myuser = myuser_key.get()
                template_values={
                    'anagram':anagram,
                    'user':user,
                    'ac':myuser.ac,
                    'wc':myuser.wc

                    }
                template = JINJA_ENVIRONMENT.get_template('home.html')
                self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', main),
    ('/addWord', AddWord),
    ('/uploadFile', uploadFile),
    ('/subAnagram',subAnagram)
], debug=True)
