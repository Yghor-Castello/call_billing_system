# Call Billing System API

## Description

REST API developed with Django and Django REST Framework for managing phone calls and billing. The application allows users to input, view, and manage detailed call records, as well as automatically calculate call costs based on duration, rate schedules, and applicable fees. Authentication is handled via JWT tokens.

## Technologies Used

- **Django** and **Django REST Framework**
- **PostgreSQL** (via Docker)
- **Docker** and **Docker Compose**
- **JWT Authentication**

## Features

- **Call Management**: Register and view phone call details, including origin, destination, duration, and timestamp.
- **Billing Management**: Automatically calculate call costs based on call duration, time-of-day rates, and applicable fees.
- **JWT Authentication**: Ensure secure access, allowing users to manage only their own call records and invoices.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Yghor-Castello/call_billing_system
cd call-billiing-system-api
```

### 2. Configure and Start with Docker

```
docker-compose up --build
```

### 3. Apply Migrations and Create a Superuser

```
docker-compose exec backend python manage.py migrate
```
```
docker-compose exec backend python manage.py createsuperuser
```

### 4. Load Fixtures to Populate the Database

```
docker-compose exec backend python manage.py loaddata billing_fixture.json
```

### 5. Access the API

- The API will be available at http://localhost:8000/.

### 6. Running Tests

```
docker-compose exec backend pytest
```

### 7. Insomnia Collection

- To test the API using Insomnia, navigate to the insomnia_collection folder and import the JSON file into your Insomnia workspace.

- http://localhost:8000/api/phone-bills?phone_number=99988526423&period=2016-02
- http://localhost:8000/api/phone-bills?phone_number=99988526423&period=2017-12
- http://localhost:8000/api/phone-bills?phone_number=99988526423
- http://localhost:8000/api/phone-bills?phone_number=99988526423&period=2015-01