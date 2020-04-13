from setuptools import setup, find_packages

setup(
    name='raspberry_home',
    version='0.1',
    packages=find_packages(include=['raspberry_home', 'raspberry_home.*']),
    package_data={'raspberry_home': ['assets/*', 'assets/*/**']},
    url='https://github.com/merskip/raspberry-home',
    license='',
    author='Piotr Merski',
    author_email='merskip@gmail.com',
    description='Manage your home with Raspberry Pi',
    install_requires=['Pillow', 'SQLAlchemy'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'run-simulator = raspberry_home.main:run_simulator'
        ]
    },
)
