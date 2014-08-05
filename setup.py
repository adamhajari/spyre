from setuptools import setup, find_packages

setup(
    name='DataSpyre',
    version='0.0.1',
    description='DataSpyre makes it easy to build interactive web applications,  and requires no knowledge of HTML, CSS, or Javascript.',
    url='https://github.com/adamhajari/spyre',
    author='Adam Hajari',
    author_email='adam@nextbigsound.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: CherryPy',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Environment :: Web Environment',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
    ],
    keywords='web application template data visualization',
    packages=['spyre'],
    install_requires=[
        "numpy",
        "scipy",
        "pandas",
        "patsy",
        "cherrypy",
        "simplejson",
        "jinja2",
        "matplotlib",
        "ggplot",
    ]
)
