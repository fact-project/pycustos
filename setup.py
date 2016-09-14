from setuptools import setup

setup(
    name='custos',
    version='0.0.2',
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
    test_requires=[
        'pytest',
    ],
    entry_points={
        'console_scripts': [],
    },
    zip_safe=False,
)
