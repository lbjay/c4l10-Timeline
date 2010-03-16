
from rdflib import ConjunctiveGraph, URIRef, Literal
import simplejson
from datetime import datetime, timedelta
from time import mktime

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado import template

import namespaces as ns
from graphstore import g

base_uri = 'http://irc.code4lib.org/'
loader = template.Loader('/home/jluker/projects/c4l10_timeline/templates')

class BaseHandler(tornado.web.RequestHandler):
    def render_posts(self, posts, format='html'):
        output = []
        for p in posts:
            try:
                content = list(g.objects(p, ns.sioc.content))[0]
                created = list(g.objects(p, ns.dct.created))[0]
                user = list(g.objects(p, ns.sioc.has_creator))[0]
                output.append({
                    'content': content, 
                    'user': user, 
                    'datestamp': created,
                })
            except IndexError:
                print p
                raise
        if format == 'json':
            self.set_header('Content-Type', 'application/json')
            self.write(simplejson.dumps(posts))
        elif format == 'html':
            t = loader.load('posts.html')
            self.write(t.generate(posts=output))

    def posts_by_user(self, username):
        user_uri = URIRef("%suser/%s" % (base_uri, username))
        return list(g.subjects(ns.sioc.has_creator, user_uri))

    def posts_by_date(self, start_dt):
        end_dt = start_dt + timedelta(days=1)
        return self.posts_by_daterange(start_dt, end_dt)

    def posts_by_daterange(self, start_dt, end_dt):
        startepoch = int(mktime(start_dt.timetuple()))
        endepoch = int(mktime(end_dt.timetuple()))
        return self.posts_by_epochrange(start_dt, end_dt)

    def posts_by_epochrange(self, start, end):
        nsinit = { 'sioc': ns.sioc, 'dct': ns.dct, 'rdf': ns.rdf, 'xsd': ns.xsd } # ns.nsdict()
        #bindings = { '?start': start, '?end': end }
        sparql = """SELECT ?p WHERE 
            { ?p rdf:type sioc:Post . 
              ?p dct:created ?created 
              FILTER(
                ?created >= xsd:date('%s') && 
                ?created < xsd:date('%s')
              ) 
            }""" % (start, end)
        posts = g.query(sparql, initNs=nsinit) # , initBindings=bindings)
        return [x[0] for x in posts]

    def sparql_result(self, sparql):
        pass
        
class TestHandler(BaseHandler):
    def get(self, foo):
        for k,v in self.__dict__.items():
            self.write("%s = %s\n" % (k, v))

class UserPostsHandler(BaseHandler):
    def get(self, username, format='html'):
        posts = self.posts_by_user(username)
        self.render_posts(posts, format)

class DatePostsHandler(BaseHandler):
    def get(self, date, format='html'):
        start_dt = datetime.strptime(date, "%Y-%m-%d")
        posts = self.posts_by_date(start_dt)
        self.render_posts(posts, format)

class DateRangePostsHandler(BaseHandler):
    def get(self, startdate, enddate, format='html'):
        start_dt = datetime.strptime(startdate, "%Y-%m-%d")
        end_dt = datetime.strptime(enddate, "%Y-%m-%d")
        posts = self.posts_by_daterange(start_dt, end_dt)
        self.render_posts(posts, format)

class EpochRangePostsHandler(BaseHandler):
    def get(self, startepoch, endepoch, format='html'):
        posts = self.posts_by_epochrange(int(startepoch), int(endepoch))
        self.render_posts(posts, format)

class DefaultPostsHandler(BaseHandler):
    def get(self):
        today = datetime.today().strftime('%Y-%m-%d')
        self.redirect('/posts/date/%s' % today)

application = tornado.web.Application([
    (r"/log/(\w+)", TestHandler),
    (r"/posts/?$", DefaultPostsHandler),
    (r"/posts/user/(\w+)\.?(\w+)?$", UserPostsHandler),
    (r"/posts/date/([\d\-]{10})/?$", DatePostsHandler),
    (r"/posts/date/([\d\-]{10}):([\d\-]{10})/?$", DateRangePostsHandler),
    (r"/posts/epoch/(\d+):(\d+)/?$", EpochRangePostsHandler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

