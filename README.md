# Train Ticket Booking API

## Test user
Use next superuser:
- login: admin@gmail.com
- password: admin12345


## Project Description
This project is a management system for train ticket booking, providing an efficient way to manage train routes, ticket purchases, and user authentication.It allows you to:

- View available train routes.
- Purchase train tickets.
- Manage orders through a user-friendly API.

## Key Features
- JWT Authenticated
- Admin panel
- Filtering station and journey
- Train and train type management
- Station and route management
- Journey scheduling
- 🎟Ticket booking system
- Order management
- User authentication & authorization


## Database Structure
The project includes the following models:
- TrainType — defines types of trains.
- Train — stores train details (name, type, cargo, seats, etc.).
- Station — represents train stations with location data.
- Route — defines train routes between stations with distance.
- Journey — represents a train's scheduled journey on a specific route.
- Order — stores user ticket orders.


## Installation and Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repository.git
   cd your-repository

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate #For Linux/macOS
   

   python -m venv venv
   venv\Scripts\activate #For windows
   
3. Install dependencies:
   ```bash
   pip install -r requirements.txt

4. Apply database migrations:
   ```bash
   python manage.py migrate

5. Run the development server:
   ```bash
   python manage.py runserver
6. Open http://127.0.0.1:8000/api/schema/swagger-ui/ in your browser to see all available endpoints.

## Run with Docker

1. Run next command:
   ```bash
   docker-compose build
   docker-compose up
2. To create superuser inside Docker:
   ```bash
   docker-compose exec train python manage.py createsuperuser
3. Open http://127.0.0.1:8001/api/schema/swagger-ui/ in your browser to see all available endpoints.
