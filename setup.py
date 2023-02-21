from setuptools import setup, find_packages

setup(
    name='testcompany_petproject',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "flask",
        "flask-sqlalchemy",
        "python-dotenv",
        "psycopg2-binary",
        "Flask-Migrate",
        "mysqlclient",
        "mysql-connector-python",
        "Pillow",
        "pylint",
    ],
    entry_points={
        'console_scripts': [
            'testcompany_petproject = testcompany_petproject.__main__:main'
        ]
    }
)
