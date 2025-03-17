# Train Ticket Booking API
### Use the following command to load prepared data from fixture to test and debug your code: 
    python manage.py loaddata data.json
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
   
3. Create the .env file:
- Fill in the necessary values in the `.env` file (`POSTGRES_HOST`, `POSTGRES_DB`, `POSTGRES_PORT`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `SECRET_KEY`). 
- The `.env.example` file contains placeholders for all required variables.
- Leave `PGDATA`, `DJANGO_SETTINGS_MODULE` unchanged .
   ```bash
   cp .env.example .env

4. Install dependencies:
   ```bash
   pip install -r requirements.txt

5. Apply database migrations:
   ```bash
   python manage.py migrate

6. Run the development server:
   ```bash
   python manage.py runserver
7. Open http://127.0.0.1:8000/api/schema/swagger-ui/ in your browser to see all available endpoints.

## Run with Docker

1. Open your `.env` file and change the value of `DJANGO_SETTINGS_MODULE` to `train_station.settings.postgres` . Do the same with your Edit Configurations project.


2. Run next command:
   ```bash
   docker-compose build
   docker-compose up
3. To create superuser inside Docker:
   ```bash
   docker-compose exec train python manage.py createsuperuser
4. Open http://127.0.0.1:8001/api/schema/swagger-ui/ in your browser to see all available endpoints.
