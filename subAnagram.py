import webapp2;
import os;
import jinja2;
from google.appengine.ext import ndb;
from google.appengine.api import users
from anagramModel import anagramModel
from myuser import MyUser
from itertools import combinations

JINJA_ENVIRONMENT = jinja2.Environment(
loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions = ['jinja2.ext.autoescape'],
autoescape = True
)

def Sort(word):
    listWord = list(word)
    subWordKey = []
    for i in range(3,len(word)+1):
        temp=(["".join(c)for c in combinations(word,i)])
        for c in temp:
            subWordKey.append(c)
    return subWordKey

def lexico(word):
    list1 = list(word.lower())
    sorted_list = sorted(list1)
    return ''.join(sorted_list)
class subAnagram(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        result =[]
        template_values = {

        'subAnagram':result
        }
        template = JINJA_ENVIRONMENT.get_template('subAnagram.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser',user.user_id())
        myuser = myuser_key.get()

        result =[]

        action = self.request.get('button')
        if action == 'search':
            word = self.request.get('word')

            if word=="":
                self.redirect('/subAnagram')
            else:
                lexi = lexico(word)

                subAn = Sort(lexi)
                for anaKey in subAn:
                    anaKey = ndb.Key('anagramModel',user.email()+anaKey)
                    word = anaKey.get()

                    if word == None:
                        continue
                    else:
                        result.extend(word.wordList)
                template_values = {
                'subAnagram':result,

                }
                template = JINJA_ENVIRONMENT.get_template('subAnagram.html')
                self.response.write(template.render(template_values))
        else:
            self.redirect('/subAnagram')
