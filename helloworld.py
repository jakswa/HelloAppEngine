import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class Greeting(db.Model):
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write('<html><head><title>Say Hi to Jake!!!</title></head><body>')
        
        self.response.out.write("""<style>
        body {
            background: #F7F6AF;
            color: #1C2124;
            font-family: Tahoma, Helvetica, sans-serif;
        }
        a {
            color: #D62822;
        }
        /*h1 {
            color: #34A8A1;
        }*/
        div {
            padding: 10px 20px 10px 20px;
        }
        div.one {
            background: #9BD6A3;
            color: #000000;
        }
        div.another {
            background: #4E8264;
            color: #FFFFFF;
        }
        div.one h3 {
            background: #ABE6B3;
            padding: 10px 20px 10px 20px;
        }
        div.another h3 {
            background: #3E7254;
            padding: 10px 20px 10px 20px;
        }
        </style>""")
        # Write the submission form and the header of the page
        self.response.out.write("""
              <form action="/sign" method="post">
              <div><h2>Say Hi to Me</h2></div>
                <div><textarea name="content" rows="3" cols="60"></textarea></div>""")
        if users.get_current_user():
            self.response.out.write("<div>Logged in as "+users.get_current_user().nickname()+"""<br /><a href="logout">Logout</a></div>""")
        else:
            self.response.out.write("""<div>Name (optional): <input type="text" name="author" id="thename"></input> or <a href="login">Login</a><br /><br />""")
            
        self.response.out.write("""<div><input type="submit" value="Sign Guestbook"></div></form><br /><br />""")
            
        self.response.out.write("""<h1>What Everyone Says</h1>""")
        
        greetings = db.GqlQuery("SELECT * FROM Greeting ORDER BY date DESC LIMIT 10")
        bob = 0;
        for greeting in greetings:
            bob = bob + 1
            if (bob % 2 == 0):
                self.response.out.write("""<div class="one">""")
            else:
                self.response.out.write("""<div class="another">""")
                
            if greeting.author:
                self.response.out.write("""<h3>%s wrote:</h3>""" % greeting.author.nickname())
            else:
                self.response.out.write('<h3>Someone wrote:</h3>')
            self.response.out.write('<blockquote>%s</blockquote></div>' %
                                    cgi.escape(greeting.content))

        self.response.out.write("""
            </body>
            <a href="
          </html>""")

class Guestbook(webapp.RequestHandler):
    def post(self):
        greeting = Greeting()

        if users.get_current_user():
            greeting.author = users.get_current_user()
        elif (self.request.get('author')):
            greeting.author = users.User(self.request.get('author'))

        greeting.content = self.request.get('content')
        greeting.put()
        self.redirect('/')

class Login(webapp.RequestHandler):
	def get(self):
		self.redirect(users.create_login_url(self.request.uri+"/.."))

class Logout(webapp.RequestHandler):
    def get(self):
        self.redirect(users.create_logout_url(self.request.uri+"/.."))

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/sign', Guestbook),
                                      ('/login', Login),
                                      ('/logout', Logout)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
