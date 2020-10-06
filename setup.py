from setuptools import setup, find_packages

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    name='botlander',
    author="Lucas Eliaquim",
    author_email='lucas_m-santos@hotmail.com',
    version='1.0',
    description= 'Your package short description.',
    include_package_data=True,
    url='https://gitlab.com/LEMSantos/botlander',
    zip_safe=False,
    packages=find_packages(include=['botlander', 'botlander.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    install_requires=[
        'flask',
    ],
)
