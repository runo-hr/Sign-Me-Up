import os
import sys
import argparse
import pkg_resources

from django.core.management import call_command


def create_project(project_name):
    """
    Create a new Django project using the signmeup template.

    This function sets up a new Django project with the given project name.
    It creates the project directory and initializes the project using Django's 'startproject' command.
    Additionally, it creates an 'accounts' app using Django's 'startapp' command, and updates various configuration files.

    Args:
        project_name (str): The name of the new Django project.

    Returns:
        None
    """
    # Add the current directory (project path) to sys.path
    sys.path.append(os.getcwd())

    # Create Django project using the project name provided by the user
    call_command('startproject', project_name)

    # Change to the newly created project directory
    os.chdir(project_name)

    # Run Django's startapp command for the 'accounts' app
    call_command('startapp', 'accounts')

    create_env_file(project_name)


    # Update core urls.py for the new project
    update_urls_file(project_name, ['accounts'])

    # Update the settings.py file with the required apps in INSTALLED_APPS
    update_settings_file(project_name)

    # Update the app-level files
    update_app_files()


def create_env_file(project_name):
    """
    Create the .env file with the environment variables for the Django project.

    This function generates a .env file in the same directory as the 'settings.py' file
    for the specified Django project. The .env file will contain environment variables
    related to email configuration, database connection, and general settings.

    Args:
        project_name (str): The name of the new Django project.
    """
    # Path to the .env file
    env_file_path = os.path.join(project_name, '.env')

    # Variables for different sections of the .env file
    env_variables = {
        'EMAIL': {
            'EMAIL_HOST': ('your_email_host', 'smtp.gmail.com'),
            'EMAIL_PORT': ('your_email_port', '587'),
            'EMAIL_HOST_USER': ('your_email_user', 'yourname@email.com'),
            'EMAIL_HOST_PASSWORD': ('your_email_password', ''),
            'EMAIL_USE_TLS': ('True', 'NOTE: Change to False if not using TLS'),
            'EMAIL_BACKEND': ('django.core.mail.backends.smtp.EmailBackend', ''),
        },
        'DATABASE': {
            'NAME': ('your_db_name', ''),
            'USER': ('your_db_user', ''),
            'PASSWORD': ('your_db_password', ''),
            'HOST': ('your_db_host', 'localhost'),
            'PORT': ('your_db_port', '5432'),
        },
        'GENERAL': {
            'SECRET_KEY': ('your_secret_key', 'NOTE: Keep this secret in production'),
            'DEBUG': ('True', 'NOTE: Set to False in production'),
        }
    }

    # Write the variables to the .env file
    with open(env_file_path, 'w') as env_file:
        for section, variables in env_variables.items():
            env_file.write(f"# {section} variables\n")
            for key, (value, comment) in variables.items():
                if comment:
                    env_file.write(f'{key}="{value}"  # {comment}\n')
                else:
                    env_file.write(f'{key}="{value}"\n')
            env_file.write("\n")




def update_urls_file(project_name, apps):
    """
    Update the urls.py file in the core of the project with URL patterns for the specified apps.

    Args:
        project_name (str): The name of the new Django project.
        apps (list): A list of app names (as strings) for which URL patterns should be added.

    Returns:
        None
    """
    # Path to the urls.py file in the core of the project
    core_urls_file_path = os.path.join(project_name, 'urls.py')

    # Read the content of the existing urls.py file
    with open(core_urls_file_path, 'r') as core_urls_file:
        content = core_urls_file.read()

    # Generate URL patterns for the specified apps
    app_url_patterns = [
        f"path('{app}/', include('{app}.urls')),"
        for app in apps
    ]

    # Find the position to insert the new URL patterns
    urlpatterns_start = content.find('urlpatterns = [')

    if urlpatterns_start != -1:
        # Insert the new URL patterns after the urlpatterns line
        urlpatterns_line = 'urlpatterns = ['
        urlpatterns_end = content.find('\n', urlpatterns_start)

        new_content = (
            content[:urlpatterns_end] +
            '\n    ' + '\n    '.join(app_url_patterns) +
            content[urlpatterns_end:]
        )

        # Insert the import_lines at the top
        import_lines = """
# Import include from django.urls
from django.urls import include
"""
        new_content = import_lines + new_content

        # Write the updated content back to the urls.py file
        with open(core_urls_file_path, 'w') as core_urls_file:
            core_urls_file.write(new_content)




def update_settings_file(project_name):
    """
    Update the settings.py file of the project with required configurations.

    Args:
        project_name (str): The name of the new Django project.
    """
    # Path to the settings.py file
    settings_file_path = os.path.join(project_name, 'settings.py')
    # Open the settings.py file and read its content
    with open(settings_file_path, 'r') as settings_file:
        content = settings_file.read()

    # Define the new settings to be added as comments
    new_settings = {
        'SECRET_KEY': "os.getenv('SECRET_KEY')",
        'DEBUG': "os.getenv('DEBUG')",
        'DATABASES': """{
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('NAME'), 
#         'USER': os.getenv('USER'), 
#         'PASSWORD': os.getenv('PASSWORD'), 
#         'HOST': os.getenv('HOST'), 
#         'PORT': os.getenv('PORT'),
#     }
# }

"""
    }

    # Add comments for new settings
    for setting_name, setting_value in new_settings.items():
        setting_start = content.find(setting_name)
        setting_end = content.find('\n', setting_start)
        if setting_start != -1 and setting_end != -1:
            setting_line = content[setting_start:setting_end]
            content = content[:setting_start] + f"""
# Added by signmeup: Define the {setting_name.lower()} in the .env file at the same location as this settings.py file
# {setting_name} = {setting_value} """ + '\n' + content[setting_start:]

    # Apps to add to INSTALLED_APPS
    apps_to_add = [
        "'rest_framework'",
        "'rest_framework.authtoken'",
        "'accounts'",
    ]
    # Find the position of 'INSTALLED_APPS' in the settings.py content
    apps_start = content.find('INSTALLED_APPS')
    apps_end = content.find('\n]', apps_start)

    # Insert the new apps after the existing INSTALLED_APPS list
    if apps_start != -1 and apps_end != -1:
        apps_list = content[apps_start:apps_end]
        for app in apps_to_add:
            if app not in apps_list:
                content = content.replace(apps_list, f"{apps_list}\n\n    {app}, # App added by signmeup")

    # Middleware settings
    middleware_to_add = [
        "'accounts.middleware.TokenExpirationMiddleware'"
    ]
    # Find the position of 'MIDDLEWARE' in the settings.py content
    middleware_start = content.find('MIDDLEWARE')
    middleware_end = content.find('\n]', middleware_start)

    # Insert the new middleware after the existing MIDDLEWARE list
    if middleware_start != -1 and middleware_end != -1:
        middleware_list = content[middleware_start:middleware_end]
        for middleware in middleware_to_add:
            if middleware not in middleware_list:
                # Add the middleware to MIDDLEWARE with a comment
                content = content.replace(middleware_list, f"{middleware_list}\n\n    {middleware}, # Middleware added by signmeup")

    # Add the import lines 
    import_lines = f"""
# Added by signmeup
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()  

# Email settings: Added by signmeup
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')

# Custom user model: Added by signmeup
AUTH_USER_MODEL = 'accounts.CustomUser'
"""    
    # Find the first import statement in the content
    import_start = content.find('import')
    import_end = content.find('\n', import_start)

    if import_start != -1 and import_end != -1:
        # Insert the import_lines after the first import statement
        content = content[:import_end] + '\n\n' + import_lines + content[import_end:]


    # Write the updated content back to the settings.py file
    with open(settings_file_path, 'w') as settings_file:
        settings_file.write(content)


def update_app_files():
    """
    Update the app-level files with the content from the signmeup package.

    Note:
        This function assumes that the 'accounts' app already exists in the project.
    """
    # Source directory containing the app-level files
    source_app_dir = pkg_resources.resource_filename('signmeup.accounts', '')

    # Destination directory for the newly created app
    destination_app_dir = os.path.join(os.getcwd(), 'accounts')

    # List of files to add and update
    files_to_update = [
        ('urls.py', os.path.join(source_app_dir, 'urls.py')),
        ('serializers.py', os.path.join(source_app_dir, 'serializers.py')),
        ('middleware.py', os.path.join(source_app_dir, 'middleware.py')),
        ('admin.py', os.path.join(source_app_dir, 'admin.py')),
        ('models.py', os.path.join(source_app_dir, 'models.py')),
        ('tests.py', os.path.join(source_app_dir, 'tests.py')),
        ('views.py', os.path.join(source_app_dir, 'views.py'))   
    ]

    for file_name, source_file_path in files_to_update:
        destination_file_path = os.path.join(destination_app_dir, file_name)

        try:
            with open(destination_file_path, 'r') as destination_file:
                existing_content = destination_file.read()
        except FileNotFoundError:
            existing_content = ""

        with open(source_file_path, 'r') as source_file:
            content = source_file.read()

        if existing_content != content:
            with open(destination_file_path, 'w') as destination_file:
                destination_file.write(content)


def main():
    """
    Entry point of the signmeup command-line interface (CLI).

    This function parses the command-line arguments provided by the user and executes the appropriate action.
    The CLI supports the 'startproject' command to create a new Django project using the signmeup template.

    Command-line arguments:
    - startproject: Create a new Django project.

    Usage:
        signmeup startproject <project_name>

    Args:
        None

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description='Create a new Django project using the signmeup template.')
    subparsers = parser.add_subparsers(dest='command')
    subparser_startproject = subparsers.add_parser('startproject', help='Create a new Django project.')

    subparser_startproject.add_argument('project_name', metavar='project_name', type=str, nargs='?', help='The name of the new Django project.')

    args = parser.parse_args()

    if args.command == 'startproject':
        if args.project_name:
            create_project(args.project_name)
        else:
            print('Error: Please provide a project name.')
            print('Usage: signmeup startproject project_name')
            sys.exit(1)
    else:
        print('Invalid command. Please use "signmeup startproject <project_name>".')
        sys.exit(1)


if __name__ == '__main__':
    main()
