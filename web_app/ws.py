import cherrypy
import opengraph
import pdb

import json
# import pandas as pd
# import getgraph

# this should be implemented in document db
url_db = {}
msg_url_mapping={}



class MyWebService:
    exposed = True

    @cherrypy.tools.accept(media='application/json')

    def POST(self, **kwargs):
        print ('---------args: %s ' % kwargs)
        url = kwargs['url']
        print ("about parsing %s" % url)
        if url == None:
            return "error"
        else:
            #check if url does exist
            if len(url_db) == 0:
                url_id = 1
            else:
                url_id = str(max([int(_) for _ in url_db.keys()]) + 1)
            print (url_id)
            pdb.set_trace()
            gf=opengraph.OpenGraph('http://%s' % url)
            print(gf.to_json)
            print (gf.to_html)
        return "ok"


    def GET(self, url=None):
        if url == None:
            return ('no URL')
        elif url in url_db:
            url_record = url_db[id]
            return ('found')
        else:
            return ('No url %s ' % url)


if __name__ == '__main__':
    cherrypy.tree.mount(
        MyWebService(), '/stories',
        {'/':
             {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
         }
    )
    config = {'server.socket_host': '0.0.0.0',
              'server.socket_port' : 8080}
    cherrypy.config.update(config)

# same as  cherrypy.quickstart(MyWebService())
cherrypy.engine.start()
cherrypy.engine.block()
