from setuptools import setup
import versioneer

version=versioneer.get_version()
setup(
    name='django_opentracing',
    cmdclass=versioneer.get_cmdclass(),
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
        'django<2',
        'opentracing>=2.0,<2.1',
        'six',
    ],
    extras_require={
        'tests': [
            'coverage',
        ],
    },
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
