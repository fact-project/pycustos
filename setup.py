from setuptools import setup

setup(
    name='custos',
    version='0.0.6',
    description='A framework for monitoring and notifying',
    url='https://github.com/fact-project/pycustos',
    author='Dominik Neise, Maximilian Noethe, Sebastian Mueller',
    author_email='maximilian.noethe@tu-dortmund.de',
    license='MIT',
    packages=[
        'custos',
        'custos.checks',
        'custos.notify',
        ],
    install_requires=[
        'requests',
        'apscheduler',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest>=3.0.0'],
    zip_safe=False,
)
