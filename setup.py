from setuptools import setup

setup(
    name='raspberry-home',
    version='0.1',
    packages=['raspberry-home'],
    url='https://github.com/merskip/raspberry-home',
    license='',
    author='Piotr Merski',
    author_email='merskip@gmail.com',
    description='Manage your home with Raspberry Pi',
    install_requires=['Pillow', 'SQLAlchemy'],
)
