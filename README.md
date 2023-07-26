# Sign-Me-Up

Sign-Me-Up is a Django REST framework -based user registration and management API.  
It provides a seamless solution for handling user registration, authentication, profile management, and more.   
With Sign-Me-Up, you can quickly integrate user management functionality into your Django projects, allowing you to focus on building other parts of your application.

## Features
The Django project will be preconfigured with the following features:

- User registration with email verification
- Token-based authentication for user login
- User profile management
- Customizable password strength requirements
- RESTful API endpoints for easy integration with frontend frameworks.

## Installation
Navigate to the desired project directory.  

Check if you have `virtualenv` installed globally:

```shell
virtualenv --version
```

If you see an error, you need to install `virtualenv`. You can install it using `pip`:

```shell
pip install virtualenv
```

Create a virtual environment:

```shell
virtualenv env
```

Activate the virtual environment:

```shell
# For Windows
venv\Scripts\activate

# For macOS and Linux
source venv/bin/activate
```
Install signmeup using pip

```bash
pip install signmeup
```
Start a project
```bash
signmeup startproject <project_name>
```

Structure of the created project:
```
<project_name>/
├── accounts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── middleware.py
│   ├── migrations/
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   └── views.py
├── <project_name>/
│   ├── __init__.py
│   ├── .env
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
└── manage.py

```



## Configuration  
A `.env` file is added to the core of the project.  
Configure the project by defining the following environment variables:  
  
Email Variables
- `EMAIL_HOST`: The hostname of the email server. Example: `smtp.gmail.com`
- `EMAIL_PORT`: The port number of the email server. Example: `587`
- `EMAIL_BACKEND`: The email backend to use. Example: `django.core.mail.backends.smtp.EmailBackend`
- `EMAIL_HOST_USER`: The username for authenticating with the email server. Example: `your_email@example.com`
- `EMAIL_HOST_PASSWORD`: The password for authenticating with the email server.
- `EMAIL_USE_TLS`: Set it to `True` to use TLS encryption for email communication.

Database Variables
- `NAME`: The name of the PostgreSQL database.
- `USER`: The username for authenticating with the PostgreSQL database.
- `PASSWORD`: The password for authenticating with the PostgreSQL database.

General variables
- `DEBUG`: Set it to `True` for development mode and `False` for production mode.
- `SECRET_KEY`: The secret key used for cryptographic operations.

For Database and general variables, you wiil need to uncomment the following in `settings.py:

```
# Added by signmeup: Define the databases in the .env file at the same location as this settings.py file

#DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('NAME'), 
#         'USER': os.getenv('USER'), 
#         'PASSWORD': os.getenv('PASSWORD'), 
#         'HOST': os.getenv('HOST'), 
#         'PORT': os.getenv('PORT'),
#     }
# }
```
```
# Added by signmeup: Define the secret_key in the .env file at the same location as this settings.py file

# SECRET_KEY = os.getenv('SECRET_KEY') 

# Added by signmeup: Define the debug in the .env file at the same location as this settings.py file

# DEBUG = os.getenv('DEBUG') 
```
## API Endpoints
The following API endpoints are available:

- **User Registration**: Register a new user.
  - Method: POST
  - URL: `http://localhost:8000/accounts/register/`
  - Fields: `username`, `email`, `password`

- **Verify Email**: Verify the user's email address using the verification token received via email.
  - Method: GET
  - URL: `http://localhost:8000/accounts/verify-email/`
  - Requires authentication: No
  
- **User Login**: Log in a user and obtain an authentication token.
  - Method: POST
  - URL: `http://localhost:8000/accounts/login/`
  - Fields: `username`, `password`

- **User Logout**: Log out the authenticated user.
  - Method: POST
  - URL: `http://localhost:8000/accounts/logout/`
  - Requires authentication: Yes
  
- **Get User Profile**: Get the profile information of the authenticated user.
  - Method: GET
  - URL: `http://localhost:8000/accounts/profile/`
  - Requires authentication: Yes

- **Update User Profile**: Update the profile information of the authenticated user.
  - Method: POST
  - URL: `http://localhost:8000/accounts/profile/`
  - Requires authentication: Yes


- **Delete User**: Delete the authenticated user's account.
  - Method: DELETE
  - URL: `http://localhost:8000/accounts/delete/`
  - Requires authentication: Yes
  
## Testing API endpoints

To interact with the API endpoints for your newly created project, you can use tools like [Postman](https://www.postman.com/) to send HTTP requests to the API endpoints. Here's how you can use Postman:

1. Install Postman on your machine from the [Postman website](https://www.postman.com/downloads/).
2. Launch Postman and create a new request.
3. Set the request method (e.g., POST, GET) and URL for the desired API endpoint.
4. Add any required headers or request parameters.
5. Send the request and view the response.


Make sure to replace `http://localhost:8000/` in the API URL with the appropriate base URL if running the API on a different host or port.

## Contributing

Contributions are welcome! If you would like to contribute to Sign-Me-Up, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Implement your changes and ensure that the tests pass.
4. Commit and push your changes to your forked repository.
5. Open a pull request, and provide a detailed description of your changes.

