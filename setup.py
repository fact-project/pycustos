from setuptools import setup

extras_require = {
    'twilio': ['twilio~=6.0'],
    'telegram': ['telepot'],
}
extras_require['all'] = extras_require['twilio'] + extras_require['telegram']

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='custos',
    version='0.1.1',
    description='A framework for monitoring and notifying',
    long_description=long_description,
    url='https://github.com/fact-project/pycustos',
    author='Dominik Neise, Maximilian Noethe, Sebastian Mueller',
    author_email='maximilian.noethe@tu-dortmund.de',
    license='MIT',
    packages=[
        'custos',
        'custos.checks',
        'custos.notify',
    ],
    extras_require=extras_require,
    install_requires=[
        'requests',
        'apscheduler',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest>=3.0.0'],
    zip_safe=False,
)
