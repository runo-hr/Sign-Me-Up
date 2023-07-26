from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='signmeup',
    version='0.0.3',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'asgiref==3.7.2',
        'Django==4.2.2',
        'django-cors-headers==4.1.0',
        'djangorestframework==3.14.0',
        'Pillow==10.0.0',
        'psycopg2==2.9.6',
        'python-dotenv==1.0.0',
        'pytz==2023.3',
        'sqlparse==0.4.4',
        'typing_extensions==4.6.3',
        'tzdata==2023.3',
    ],
    entry_points={
        'console_scripts': [
            'signmeup=signmeup.cli:main',
        ],
    },
)
