# User Search by Country Location

The project is an API I developed using FastAPI and SQLAlchemy that allows for the management of users and their addresses. The API provides endpoints for creating users along with their addresses, as well as for searching users by their country of residence. In this example, I've used SQLite as the database, but it can be configured to work with other databases compatible with SQLAlchemy.

## Requirements to Run the Project

### Clone the Repository

- Clone the repository to your machine:

```python
git clone https://github.com/Magno-12/PRGX_challenge
```

- Create a virtual environment using the following installation and activation commands:

```python
pip install virtualenv
virtualenv env
```

**On Windows:**
```python
env\Scripts\activate
```

**On macOS and Linux:**
```python
source env/bin/activate
```

- Ensure you have Python 3.x installed on your system. You will also need to install the project's dependencies. You can do this using pip:

```python
pip install -r requirements.txt
```

- Run the FastAPI application:

```python
uvicorn main:app --reload
```

## Test in Postman

### User creation

1. Open Postman and make sure your FastAPI application is running (uvicorn main:app --reload).

2. Create a new POST request with the URL: http://127.0.0.1:8000/users/.

3. In the "Body" tab, select "raw" and choose "JSON (application/json)".

4. Use the following JSON as the request body to create a new user with an address:

```json
{
  "user": {
    "first_name": "John",
    "last_name": "Doe",
    "email": "johndoe@example.com",
    "password": "secretpassword"
  },
  "addresses": [
    {
      "street": "123 Main St",
      "city": "City",
      "country": "Country"
    }
  ]
}

```

5. Click "send" to send the request

### User Search by Country

1. Create a new GET request with the URL: http://127.0.0.1:8000/users/?country=Country.

2. Click "Send" to send the request.

country=Country is the name of the country that was registered when the user was created

## Test in Swagger

You can perform tests in Swagger directly from the FastAPI interface. Here's how to do it:

1. Open your web browser and navigate to http://127.0.0.1:8000/docs.
2. This will take you to the automatically generated Swagger interface for your API.

### User Creation

1. In the "POST /users/" section, expand the POST request and click "Try it out."
2. In the input area, place the following JSON as the request body:

```json
{
  "user": {
    "first_name": "John",
    "last_name": "Doe",
    "email": "johndoe@example.com",
    "password": "secretpassword"
  },
  "addresses": [
    {
      "street": "123 Main St",
      "city": "City",
      "country": "Country"
    }
  ]
}

```

### User Search by Country

1. In the "GET /users/" section, expand the GET request and click "Try it out."
2. In the input area, enter "Country" in the "country" field, then click "Execute" to send the request.

## Development Explanation

I developed this code to create a FastAPI-based API for managing user data and their associated addresses. In this project, I defined three Pydantic models: UserModel, AddressModel, and UserWithAddressesModel, which represent user information, address details, and a combination of both, respectively. I configured an SQLite database using SQLAlchemy for data storage. The API supports two main functionalities: user creation and user retrieval based on their country of residence. For user creation, I perform validation to ensure that emails are unique, and if not, raise an error. Then, I insert the user and address data into the database. The second endpoint allows users to search for individuals living in a specific country, returning their information in a structured JSON format. This code serves as a foundation for building a user management system with FastAPI and SQLAlchemy.

## Integration Test explanation

I've included test cases for FastAPI application using the TestClient from FastAPI's testclient module. The primary objective of these tests is to verify the proper functionality of our API endpoints.

The test_create_user function begins by sending a POST request to create a new user with predefined data. It is essential to verify that the response returns a status code of 200, indicating that the user creation was successful. Additionally, I ensure that the response aligns with expectations, confirming that the user data matches the expected values, with the password field excluded for security reasons.

Moving on to the test_get_users_by_country function, its goal is to test the ability to retrieve users by country using a GET request. My goal is to validate that the response status code is indeed 200, which means a successful request. Additionally, I check that the response contains at least one user, and for each user within the response, I check for the presence of the expected fields such as first name, last name, and email. The password field is excluded from the response or explicitly set to None to maintain security best practices.


