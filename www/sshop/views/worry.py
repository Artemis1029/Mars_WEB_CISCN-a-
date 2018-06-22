import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    def get(self):
        self.write_error(404)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('public/500.html')
        elif status_code == 500:
            self.render('public/500.html')
        else:
            self.write('error:' + str(status_code))