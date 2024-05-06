# EcoEcho API

Welcome to the EcoEcho API documentation! This API serves as the backend for the EcoEcho platform, a social media platform designed for US National Park enthusiasts. Built with Python Flask and SMOREst, and utilizing Marshmallow for schema validation, this API provides endpoints to manage user data, park information, activity reviews, and more.

## Setup

To run the EcoEcho API locally, follow these steps:

1. Clone the Repository:

```bash
git clone https://github.com/your/repository.git
cd eco-echo-api
```

1. Install Dependencies:

```bash
pip install -r requirements.txt
```

`. Database Configuration:
Set up your MySQL database and configure the connection details in config.py.

1. Run the Application:

```bash
flask run --reload
```

Note that the --reload flag enables automatic reloading of the application when changes are detected.

## Endpoints

The EcoEcho API provides the following endpoints:

### User Endpoints:
- `/api/users`: CRUD operations for managing user accounts.
- `/api/users/<user_id>`: Retrieve, update, or delete a specific user.

### Park Endpoints
- `/api/parks`: CRUD operations for managing park information.
- `/api/parks/<park_id>`: Retrieve, update, or delete a specific park.

### Activity Endpoints
- `/api/activities`: CRUD operations for managing park activities.
- `/api/activities/<activity_id>`: Retrieve, update, or delete a specific activity.

### Review Endpoints
- `/api/activity_reviews`: CRUD operations for managing activity reviews.
- `/api/park_reviews`: CRUD operations for managing park reviews.
- `/api/user_activity_reviews`: CRUD operations for managing user activity reviews.
- `/api/user_park_reviews`: CRUD operations for managing user park reviews.

### Wishlist Endpoints
- `/api/wishlists`: CRUD operations for managing user wishlists.

### Authentication Endpoints [coming soon...]
- `/api/auth/login`: Endpoint for user authentication and obtaining access tokens.
- `/api/auth/register`: Endpoint for user registration.

## Authentication [coming soon...]

The EcoEcho API will use JWT (JSON Web Tokens) for securing endpoints that require user authentication. Users can obtain an access token by logging in or registering through the appropriate authentication endpoints.

## Schema Validation

Marshmallow is utilized for schema validation, ensuring that data sent to the API adheres to predefined schemas. This helps maintain data integrity and consistency throughout the application.

## ER Model
![EcoEcho ER Model](https://github.com/f3igao/eco-echo-api/assets/22878381/b141381a-7c21-4f78-81be-db56f085099b)


## Contributing

Contributions to the EcoEcho API are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on GitHub.
Thank you for using the EcoEcho API! Happy coding and happy exploring! 🌲�
