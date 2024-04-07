# EMS (Employee Management System) API
## Description
The EMS_API is a headless API written in Python using the Django framework. It provides basic CRUD operations for managing employees, projects, tasks, and salary information. The API is containerized using Docker, making it easy to deploy and manage.

## Features
- Employee Management: CRUD operations for managing employee details.
- Project Management: Track and manage projects.
- Task Management: Create, update, and delete tasks associated with projects.
- Salary Management: Handle salary information for employees.
- Authentication: Secure endpoints with jwt authentication.

## Technologies Used
- Python 3.8+
- Django
- PostgreSQL
- Docker

## Getting Started
### Prerequisites
- Docker

## Setup
To run it locally on your machine do the following:
1. Clone the repository
    ``` 
    git clone https://github.com/vicganoh/ems_api.git
    cd ems_api
    ```
2. Open your terminal to Build and run the Docker container:
    ``` 
    docker-compose -f local.yaml up --build -d
    ```
3. The API will be accessible at http://localhost:8000.
4. To create an admin account to access the django admin page: Run the following command in your terminal and access django admin page at http://localhost:8000/admin
    ``` 
    docker-compose -f local.yaml exec web python manage.py createsuperuser
    ```

## Usage
1. Access the API documentation at http://localhost:8000/api/v1/docs/ for detailed information on available endpoints.
2. Use tools like curl, Postman, or your preferred API client to interact with the endpoints.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any improvements or new features.
