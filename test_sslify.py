from werkzeug import testapp
from werkzeug.test import create_environ, run_wsgi_app
from wsgi_sslify import sslify

app = sslify(testapp.test_app)

def test_redirect_to_http():
    env = create_environ()
    app_iter, status, headers = run_wsgi_app(app, env)
    assert status == '301 Moved Permanently'
    assert headers['Location'].startswith('https://')

def test_https_doesnt_redirect():
    env = create_environ()
    env['wsgi.url_scheme'] = 'https'
    app_iter, status, headers = run_wsgi_app(app, env)
    assert status == '200 OK'

def test_https_proxy_doesnt_redirect():
    env = create_environ()
    env['HTTP_X_FORWARDED_PROTO'] = 'https'
    app_iter, status, headers = run_wsgi_app(app, env)
    assert status == '200 OK'

def test_https_proxy_custom_header():
    app = sslify(testapp.test_app, proxy_header='X-PROTO')
    env = create_environ()
    env['HTTP_X_PROTO'] = 'https'
    app_iter, status, headers = run_wsgi_app(app, env)
    assert status == '200 OK'
