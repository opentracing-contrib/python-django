from setuptools import setup

version = '0.1.6'
setup(
    name='django_opentracing',
    version=version,
    url='https://github.com/opentracing-contrib/python-django/',
    download_url='https://github.com/opentracing-contrib/python-django/tarball/'+version,
    license='BSD',
    author='Kathy Camenzind',
    author_email='kcamenzind@lightstep.com',
    description='OpenTracing support for Django applications',
    long_description=open('README.rst').read(),
    packages=['django_opentracing', 'tests'],
    platforms='any',
    install_requires=[
        'django',
        'opentracing >= 2.0.0.dev1'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)