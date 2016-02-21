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


def test_https_proxy_header_disabled():
    app = sslify(testapp.test_app, proxy_header=None)
    env = create_environ()
    env['HTTP_X_FORWARDED_PROTO'] = 'https'
    app_iter, status, headers = run_wsgi_app(app, env)
    assert status == '301 Moved Permanently'
    assert headers['Location'].startswith('https://')


def test_https_proxy_custom_header():
    app = sslify(testapp.test_app, proxy_header='X-PROTO')
    env = create_environ()
    env['HTTP_X_PROTO'] = 'https'
    app_iter, status, headers = run_wsgi_app(app, env)
    assert status == '200 OK'


def test_https_proxy_custom_header_ignores_default_header():
    app = sslify(testapp.test_app, proxy_header='X-PROTO')
    env = create_environ()
    env['HTTP_X_FORWARDED_PROTO'] = 'https'
    app_iter, status, headers = run_wsgi_app(app, env)
    assert status == '301 Moved Permanently'
    assert headers['Location'].startswith('https://')


def test_permanent():
    app = sslify(testapp.test_app, permanent=False)
    env = create_environ()
    app_iter, status, headers = run_wsgi_app(app, env)
    assert status == '302 Found'
    assert headers['Location'].startswith('https://')


def test_hsts_defaults():
    app = sslify(testapp.test_app)
    env = create_environ()
    env['wsgi.url_scheme'] = 'https'
    app_iter, status, headers = run_wsgi_app(app, env)
    assert status == '200 OK'
    assert headers['Strict-Transport-Security'] == 'max-age=31536000'


def test_hsts_off():
    app = sslify(testapp.test_app, hsts=False)
    env = create_environ()
    env['wsgi.url_scheme'] = 'https'
    app_iter, status, headers = run_wsgi_app(app, env)
    assert status == '200 OK'
    assert 'Strict-Transport-Security' not in headers


def test_hsts_custom_max_age():
    app = sslify(testapp.test_app, max_age=60)
    env = create_environ()
    env['wsgi.url_scheme'] = 'https'
    app_iter, status, headers = run_wsgi_app(app, env)
    assert status == '200 OK'
    assert headers['Strict-Transport-Security'] == 'max-age=60'


def test_hsts_subdomains():
    app = sslify(testapp.test_app, subdomains=True)
    env = create_environ()
    env['wsgi.url_scheme'] = 'https'
    app_iter, status, headers = run_wsgi_app(app, env)
    assert status == '200 OK'
    assert headers['Strict-Transport-Security'] == 'max-age=31536000; includeSubDomains'
