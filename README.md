Pyramids Pharmacy Project
Prerequisites
Before running this project, make sure you have the following installed on your system:

Docker (v20.10.0 or higher)
Docker Compose (v2.0.0 or higher)
Git


Getting Started
1. Clone the Repository
git clone https://github.com/mohamedmousa1989/pyramids-pharmacy.git
cd pyramids-pharmacy
2. Environment Setup
The project uses Docker Compose for local development. All necessary environment variables are already configured in the docker-compose.yml file.

Default database credentials:

Database name: pyramids_pharmacy
Username: postgres
Password: postgres
Port: 5436 (host) -> 5432 (container)
3. Build and Run the Project
bash

Copy
# Build and start the containers
docker-compose up --build

# To run in detached mode (background)
docker-compose up -d --build
The application will be available at: http://localhost:8000

4. Common Commands
View running containers
bash

Copy
docker-compose ps
View application logs
bash

Copy
# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View logs for specific service
docker-compose logs web
docker-compose logs db
Stop the application
bash

Copy
docker-compose down
Access the Django shell
bash

Copy
docker-compose exec web python manage.py shell
Create database migrations
bash

Copy
docker-compose exec web python manage.py makemigrations
Apply migrations
bash

Copy
docker-compose exec web python manage.py migrate
Create a superuser
bash

Copy
docker-compose exec web python manage.py createsuperuser
5. Database Management
The PostgreSQL database is accessible on port 5436. You can connect to it using any database management tool with these credentials:

Host: localhost
Port: 5436
Database: pyramids_pharmacy
Username: postgres
Password: postgres