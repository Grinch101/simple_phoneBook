from setuptools import setup


setup(
        name='flask_crm', # module's name
        version='1.0',
        py_modules=['app'], # the file that needs to be installed
        install_requirs=[
                'flask',
                'Flask-JWT'],
        entry_points='''
                [console_scripts]
                app=app:app
        '''
)
