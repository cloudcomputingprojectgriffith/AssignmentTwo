import webapp2;
import os;
import jinja2;
from google.appengine.ext import ndb;
from google.appengine.api import users
from myuser import MyUser
from anagramModel import anagramModel
import re



JINJA_ENVIRONMENT = jinja2.Environment(
loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions = ['jinja2.ext.autoescape'],
autoescape = True
)

class AddWord(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        template_values ={
        'message':''
        }
        template = JINJA_ENVIRONMENT.get_template('addWord.html')
        self.response.write(template.render(template_values))


    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')
        user = users.get_current_user()


        if action=='AddWord':
            anaText = self.request.get('Word')

            if not re.match("^[a-z]*$", anaText.lower()):
                message = "Please enter alphabets only"

            else:

                text = self.request.get('Word')
                lexico = list(text.lower())
                sort = sorted(lexico)
                anagAdd = ''.join(sort)
                anagram_key = ndb.Key('anagramModel',user.email()+anagAdd)
                anagramText = anagram_key.get()
                myuser_key = ndb.Key('MyUser', user.user_id())
                myuser = myuser_key.get()

                if anagramText == None :
                    addingAna = anagramModel(id=user.email()+anagAdd,aKey=anagAdd)
                    addingAna.User=user.email()
                    addingAna.wordList.append(anaText)
                    addingAna.wordCount = 1
                    addingAna.letterCount = len(anaText)
                    addingAna.put()

                    myuser.wc = myuser.wc + 1
                    myuser.ac = myuser.ac + 1
                    # myuser = MyUser(id=user.user_id(),username=user.email(),ac=ac,wc=wc)
                    myuser.put()

                    message = "Word added"

                else:
                    flag = False
                    for word in anagramText.wordList:
                        if word == anaText:
                            flag = True
                            break
                        else:
                            flag = False

                    if flag:
                        message = 'Word already exists'
                    else:

                        anagramText.wordList.append(anaText)
                        anagramText.wordCount = anagramText.wordCount + 1
                        anagramText.put()
                        wc = myuser.wc + 1
                        ac = myuser.ac
                        myuser = MyUser(id=user.user_id(),username=user.email(),ac=ac,wc=wc)
                        myuser.put()

                        message = "Word added"


            template_values ={
            'message':message,
            'wc': myuser.wc,
            'ac' : myuser.ac
            }
            template = JINJA_ENVIRONMENT.get_template('addWord.html')
            self.response.write(template.render(template_values))


