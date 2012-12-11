import os
import re
from string import letters

import webapp2

from google.appengine.ext import db

from data import *
from render import *

##### blog stuff

class BlogFront(BlogHandler):
    def get(self):
        posts = db.GqlQuery("select * from Post order by created desc limit 10")
        self.render('more_front.html', posts = posts)


class PostPage(BlogHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        if not post:
            self.error(404)
            return
        self.render("permalink.html", post = post)
    def post(self,post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        author=self.request.get('author')
        content=self.request.get('content')
        if author and content:
            c= Comment(parent=blog_key(),post=post,author=author,content=content)
            c.put()
            self.redirect("/blog/"+str(post_id))
        else:
            error="author and content, please"

class NewPost(BlogHandler):
    def get(self):
        self.render("newpost.html")

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(parent = blog_key(), subject = subject, content = content)
            p.put()
            self.redirect('/blog')
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject, content=content, error=error)

class RemovePost(BlogHandler):
    def get(self,post_id):
        key = db.Key.from_path('Post',int(post_id),parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)

        p_backup = Post_backup(parent=blog_key() ,subject=post.subject,content=post.content,created=post.created)
        p_backup.put()
        post.delete()
        self.redirect('/blog')

class EditPost(BlogHandler):
    def get(self,post_id):
        key = db.Key.from_path('Post',int(post_id),parent=blog_key())
        post = db.get(key)
        if not post:
            self.error(404)
        self.render("editpost.html",subject=post.subject,content=post.content)
    def post(self,post_id):
        subject = self.request.get('subject')
        content = self.request.get('content')
        key = db.Key.from_path('Post',int(post_id),parent=blog_key())
        new_post = db.get(key)
        if subject and content:
            new_post.subject=subject
            new_post.content=content
            new_post.put()
            self.redirect('/blog/')
        else:
            error = "subject and content, please!"
            self.render("editpost.html", subject=subject, content=content, error=error)


class PostStorage(BlogHandler):
    def get(self):
        posts_b = db.GqlQuery("select * from Post_backup order by created desc limit 10")
        self.render('post_storage.html', posts = posts_b)

class RestorePost(BlogHandler):
    def get(self,post_id):
        key = db.Key.from_path('Post_backup',int(post_id),parent=blog_key())
        p_backup=db.get(key)
        post=Post(parent=blog_key(),subject=p_backup.subject,content=p_backup.content,created=p_backup.created)
        post.put()
        p_backup.delete()
        self.redirect('/blog')

class CleanAllPost(BlogHandler):
    def get(self):
        posts=db.GqlQuery("select * from Post")
        for p in posts:
            p_b=Post_backup(parent=blog_key() ,subject=p.subject,content=p.content,created=p.created)
            p_b.put()
        db.delete(posts)
        self.redirect('/blog')
class CleanStorage(BlogHandler):
    def get(self):
        p_backup=db.GqlQuery("select * from Post_backup")
        db.delete(p_backup)
        self.redirect('/blog/storage')


###### Unit 2 HW's
class Rot13(BlogHandler):
    def get(self):
        self.render('rot13-form.html')

    def post(self):
        rot13 = ''
        text = self.request.get('text')
        if text:
            rot13 = text.encode('rot13')

        self.render('rot13-form.html', text = rot13)


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Signup(BlogHandler):

    def get(self):
        self.render("signup-form.html")

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username = username,
                      email = email)

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.redirect('/unit2/welcome?username=' + username)

class Welcome(BlogHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else:
            self.redirect('/unit2/signup')


