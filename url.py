import webapp2
from blog import *
from plugin import *

rule = webapp2.WSGIApplication([('/', BlogFront),
                               ('/unit2/rot13', Rot13),
                               ('/unit2/signup', Signup),
                               ('/unit2/welcome', Welcome),
                               ('/blog/?', BlogFront),
                               ('/blog',BlogFront),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/newpost', NewPost),
                               ('/blog/remove/(.*)',RemovePost),
                               ('/blog/clean',CleanAllPost),
                               ('/blog/restore/([0-9]+)',RestorePost),
                               ('/blog/storage',PostStorage),
                               ('/blog/storage/clean',CleanStorage),
                               ('/blog/edit/(.*)',EditPost),
                               ('/kpi',KPI_random),
                               ],
                              debug=True)