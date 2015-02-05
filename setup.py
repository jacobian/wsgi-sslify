from setuptools import setup

setup(
    name = "wsgi-sslify",
    description = "WSGI middleware to force HTTPS.",
    version = "1.0",
    author = "Jacob Kaplan-Moss",
    author_email = "jacob@jacobian.org",
    url = "http://github.com/jacobian/wsgi-sslify",
    py_modules = ['wsgi_sslify'],
    install_requires = ['werkzeug>=0.10.1'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware'
    ]
)
