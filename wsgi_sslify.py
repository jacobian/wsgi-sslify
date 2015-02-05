import werkzeug.wsgi

YEAR_IN_SECS = 31536000

class sslify(object):
    def __init__(self, app, hsts=True, max_age=YEAR_IN_SECS, subdomains=False,
                 permanent=True, proxy_header='X-Forwarded-Proto'):
        self.app = app
        self.hsts = hsts
        self.max_age = max_age
        self.subdomains = subdomains
        self.permanent = permanent
        self.proxy_header = proxy_header

    def __call__(self, environ, start_response):
        if self.is_secure(environ):
            if self.hsts:
                def wrapped_start_response(status, headers, exc_info=None):
                    hsts_policy = 'max-age=%s' % self.max_age
                    if self.subdomains:
                        hsts_policy += '; includeSubDomains'
                    headers.append(('Strict-Transport-Security', hsts_policy))
                    return start_response(status, headers, exc_info)
                return self.app(environ, wrapped_start_response)
            else:
                return self.app(environ, start_response)
        
        else:
            headers = [('Location', self.construct_secure_url(environ))]
            if self.permanent:
                status = '301 Moved Permanently'
            else:
                status = '302 Found'
            start_response(status, headers)
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