# Sign-Me-Up

Sign-Me-Up is a Django REST framework -based user registration API that allows users to sign up, verify their email addresses, and create user accounts. It provides a secure and scalable solution for managing user registration in your web application.

## Features

- User registration with email verification
- Token-based authentication for user login
- User profile management
- Customizable password strength requirements
- RESTful API endpoints for easy integration with frontend frameworks

## Installation

1. Clone the repository to your local machine:

```shell
git clone https://github.com/runo-hr/Sign-Me-Up.git

```
2. Navigate to the project directory:

```shell
cd Sign-Me-Up
```

3. Check if you have `virtualenv` installed:

```shell
virtualenv --version
```

  - If you see an error, you need to install `virtualenv`. You can install it using `pip`:

```shell
pip install virtualenv
```

1. Create a virtual environment:

```shell
virtualenv env
```


5. Activate the virtual environment:

```shell
# For Windows
env\Scripts\activate

# For macOS and Linux
source env/bin/activate
```

6. Install the required packages:

```shell
pip install -r requirements.txt
```

## Configuration
Configure the project by setting the following environment variables:

- `DEBUG`: Set it to `True` for development mode and `False` for production mode.
- `EMAIL_HOST`: The hostname of the email server. Example: `smtp.gmail.com`
- `EMAIL_PORT`: The port number of the email server. Example: `587`
- `EMAIL_BACKEND`: The email backend to use. Example: `django.core.mail.backends.smtp.EmailBackend`
- `EMAIL_HOST_USER`: The username for authenticating with the email server. Example: `your_email@example.com`
- `EMAIL_HOST_PASSWORD`: The password for authenticating with the email server.
- `EMAIL_USE_TLS`: Set it to `True` to use TLS encryption for email communication.
- `SECRET_KEY`: The secret key used for cryptographic operations.
- `NAME`: The name of the PostgreSQL database.
- `USER`: The username for authenticating with the PostgreSQL database.
- `PASSWORD`: The password for authenticating with the PostgreSQL database.

You can set these environment variables by creating a `.env` file in the project root directory. (same folder as settings.py). Make sure to replace the values with your own configuration.

## Usage

To interact with the Sign-Me-Up API, you can use tools like [Postman](https://www.postman.com/) to send HTTP requests to the API endpoints. Here's how you can use Postman:

1. Install Postman on your machine from the [Postman website](https://www.postman.com/downloads/).
2. Launch Postman and create a new request.
3. Set the request method (e.g., POST, GET) and URL for the desired API endpoint.
4. Add any required headers or request parameters.
5. Send the request and view the response.

The following API endpoints are available:

- **User Registration**: Register a new user.
  - Method: POST
  - URL: `http://localhost:8000/accounts/register/`
  - Fields: `username`, `email`, `password`

- **User Login**: Log in a user and obtain an authentication token.
  - Method: POST
  - URL: `http://localhost:8000/accounts/login/`
  - Fields: `username`, `password`

- **User Profile**: Get the profile information of the authenticated user.
  - Method: GET
  - URL: `http://localhost:8000/accounts/profile/`
  - Requires authentication: Yes

- **Verify Email**: Verify the user's email address using the verification token received via email.
  - Method: GET
  - URL: `http://localhost:8000/accounts/verify-email/`
  - Requires authentication: No


Make sure to replace `http://localhost:8000/` in the API URL with the appropriate base URL if running the API on a different host or port.

## Contributing

Contributions are welcome! If you would like to contribute to Sign-Me-Up, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Implement your changes and ensure that the tests pass.
4. Commit and push your changes to your forked repository.
5. Open a pull request, and provide a detailed description of your changes.

