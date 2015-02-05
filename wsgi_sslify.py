import werkzeug.wsgi

class sslify(object):
    def __init__(self, app, hsts=True, proxy_header='X-Forwarded-Proto'):
        self.app = app
        self.proxy_header = proxy_header

    def __call__(self, environ, start_response):
        if self.is_secure(environ):
            return self.app(environ, start_response)
        else:
            headers = [('Location', self.construct_secure_url(environ))]
            start_response('301 Moved Permanently', headers)
            return []

    def is_secure(self, environ):
        if environ.get('wsgi.url_scheme', 'http') == 'https':
            return True
        
        if self.proxy_header:
            header = 'HTTP_' + self.proxy_header.upper().replace('-', '_')
            if environ.get(header, 'http') == 'https':
                return True

        return False

    def construct_secure_url(self, environ):
        url = werkzeug.wsgi.get_current_url(environ)
        if url.startswith('http://'):
            url = 'https://' + url[7:]
        return url