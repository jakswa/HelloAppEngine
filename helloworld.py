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
        self.response.out.write('<html><title>Say Hi to Jake!!!</title><body>')
        # Write the submission form and the footer of the page
        self.response.out.write("""
              <form action="/sign" method="post">
                <div><textarea name="content" rows="3" cols="60"></textarea></div>
                <div><input type="submit" value="Sign Guestbook"></div>
              </form><br /><br />""")
        if users.get_current_user():
            self.response.out.write("Logged in as "+users.get_current_user().nickname()+"""<br /><a href="logout">Logout</a>""")
        else:
            self.response.out.write("""<a href="login">Login</a>""")
            

        greetings = db.GqlQuery("SELECT * FROM Greeting ORDER BY date DESC LIMIT 10")

        for greeting in greetings:
            if greeting.author:
                self.response.out.write('<b>%s</b> wrote:' % greeting.author.nickname())
            else:
                self.response.out.write('An anonymous person wrote:')
            self.response.out.write('<blockquote>%s</blockquote>' %
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
