from google.appengine.ext import db
import re
from string import letters

from render import *



def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    ## Remove space of single post, show abstract in frontpage
    def part_render(self):
        self.beginning = ((self.content.lstrip())[:100]).replace('\n','<br>')
        return render_str("post_beginning.html",p=self)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p = self)

    def __unicode__(self):
        return self.subject

class Post_backup(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("oldpost.html", p = self)
    def __unicode__(self):
        return self.subject

class Comment(db.Model):
    author=db.StringProperty(required=True)
    content=db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    post = db.ReferenceProperty(Post,collection_name='comment')

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("comment.html", c = self)
    def __unicode__(self):
        return self.subject