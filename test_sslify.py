from werkzeug import testapp
from werkzeug.test import create_environ, run_wsgi_app
from wsgi_sslify import sslify

def test_redirect_to_http():
    app = sslify(testapp.test_app)
    env = create_environ()
    app_iter, status, headers = run_wsgi_app(app, env)
    assert status == '301 Moved Permanently'
    assert headers['Location'].startswith('https://')

def test_https_doesnt_redirect():
    app = sslify(testapp.test_app)
    env = create_environ()
    env['wsgi.url_scheme'] = 'https'
    app_iter, status, headers = run_wsgi_app(app, env)
    assert status == '200 OK'

def test_https_proxy_doesnt_redirect():
    app = sslify(testapp.test_app)
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

def test_permanent():
    app = sslify(testapp.test_app, permanent=False)
    env = create_environ()
    app_iter, status, headers = run_wsgi_app(app, env)
    assert status == '302 Found'
    assert headers['Location'].startswith('https://')

