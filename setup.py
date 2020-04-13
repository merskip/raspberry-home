from setuptools import setup, find_packages

setup(
    name='raspberry_home',
    version='0.1',
    description='Manage your home with Raspberry Pi',
    author='Piotr Merski',
    author_email='merskip@gmail.com',
    license='',
    url='https://github.com/merskip/raspberry-home',
    packages=find_packages(include=['raspberry_home', 'raspberry_home.*']),
    package_data={'raspberry_home': ['assets/*', 'assets/*/**']},
    zip_safe=False,
    install_requires=[
        'Pillow',
        'SQLAlchemy',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'run-simulator = raspberry_home.main:run_simulator'
        ]
    },
)
