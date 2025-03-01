# Car Rental Management System

A Flask-based web application for managing a car rental service. This project provides a web interface to view, add, update, and delete vehicles along with related information such as locations, fuel types, owners, and rental activity. It also includes data visualization endpoints and a CSV import utility.

## Features

- **Vehicle Listings**: Display vehicles with pagination, sorting, and search functionality.
- **Data Visualization**: 
  - Bar chart view of vehicle counts by state (`/plot`).
  - Scatter plot view of renter trips versus ratings (`/plotScatter`).
- **CRUD Operations**: Create, read, update, and delete vehicle entries.
- **CSV Data Import**: Load data from a CSV file into the database using the provided `loadCSVData.py` script.
- **User Login**: Simple login mechanism (for demonstration purposes).

## Technology Stack

- **Backend**: Python, Flask
- **Database**: MySQL (using `pymysql` for database connections)
- **Data Import**: Pandas and SQLAlchemy
- **Frontend**: HTML templates (rendered via Flask)

## Getting Started

### Prerequisites

- Python 3.x
- MySQL database (or an AWS RDS instance as configured in the code)
- [pip](https://pip.pypa.io/en/stable/)

### Installation

1. **Clone the repository:**
```bash
   git clone https://github.com/Ajayreddy-1234/Car-Rental-Management-System.git
   cd Car-Rental-Management-System
```
2. **Create and activate a virtual environment:**
```bash
  python -m venv venv
  source venv/bin/activate  # On Windows use: venv\Scripts\activate
```
3. **Install dependencies:**
```bash
  pip install -r requirements.txt
```
## Database Setup
Update Credentials:
The database connection details are hardcoded in both app.py and loadCSVData.py. Update these credentials:

Database Name: CarRentalDB
### Database Schema

Ensure that your MySQL database has the necessary tables:

- **Vehicles**
- **Locations**
- **FuelTypes**
- **Owners**
- **RentalActivity**

You may need to create these tables manually or run an SQL script if provided.

## Running the Application:
Start the Flask development by running:
```bash
  python app.py
```
Then open your browser and navigate to http://127.0.0.1:5000/ to access the application

## Application Structure

- **app.py**: Main Flask application file that defines routes and handles CRUD operations.
- **templates/**: HTML templates for rendering pages (e.g., `index.html`, `create.html`, `Edit.html`, `login.html`, `plot.html`, `plot_2.html`).
- **static/**: Static files such as CSS, JavaScript, and images.
- **loadCSVData.py**: Script for importing CSV data into the database.
- **requirements.txt**: List of required Python packages.
- **venv/**: Virtual environment (excluded from version control).

## Endpoints

- **`/`**: Main page showing vehicle listings with search, sort, and pagination.
- **`/plot`**: Displays a bar chart of vehicle counts by state.
- **`/plotScatter`**: Displays a scatter plot of renter trips taken versus ratings.
- **`/login`**: Login page (for demonstration; no authentication is enforced).
- **`/create`**: Endpoint to add a new vehicle.
- **`/create_vehicle`**: Form page to create a new vehicle entry.
- **`/edit`**: Endpoint to update an existing vehicle.
- **`/get_vehicle/<int:id>`**: Fetch details of a vehicle for editing.
- **`/delete/<int:id>`**: Endpoint to delete a vehicle entry.

## Deployment

For production deployment, consider using a WSGI server like Gunicorn. An example command to run the app using Gunicorn:

```bash
gunicorn app:app
```

Make sure to properly configure environment variables and secure your database credentials when deploying to production.

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests with improvements or bug fixes.

