from setuptools import setup

setup(
    name='django_opentracing',
    version='0.1.0',
    url='https://github.com/kcamenzind/django_opentracing/',
    download_url='https://github.com/kcamenzind/django_opentracing/tarball/0.1.0',
    license='MIT',
    author='Kathy Camenzind',
    author_email='kcamenzind@lightstep.com',
    description='OpenTracing support for Django applications',
    long_description=open('README.rst').read(),
    packages=['django_opentracing'],
    platforms='any',
    install_requires=[
        'django',
        'opentracing >= 2.0.0.dev0'
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