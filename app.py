from flask import Flask, redirect, render_template, request, url_for
import pymysql


app = Flask(__name__)

# Database connection info
db_host = "carrentalmanagementsystem.cp2we2aaom6h.us-east-2.rds.amazonaws.com"
db_user = "root"
db_password = "carrental.."
db_name = "CarRentalDB"


# Create a connection to the database
def get_db_connection():
    connection = pymysql.connect(host=db_host,
                                 user=db_user,
                                 password=db_password,
                                 db=db_name,
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


@app.route('/', methods=['GET', 'POST'])
def index():
    search_param = 'Make'
    search = ''
    username = request.args.get('username', 'ajayreddy')
    search_param = request.args.get('search_param', 'Make')
    search = request.args.get('search', '')

    # Get sort and search parameters from the query string
    sort = request.args.get('sort', 'VehicleID')  # Default sort by VehicleID
    order = request.args.get('order', 'asc')  # Default sort order

    query = """
    SELECT 
        v.VehicleID, 
        v.Make, 
        v.Model, 
        v.Type, 
        v.Year, 
        v.RateDaily, 
        v.NearestAirportCity, 
        l.City as LocationCity,
        l.State as LocationState,
        l.Country as LocationCountry,
        f.FuelType,
        o.OwnerID,
        r.RenterTripsTaken,
        r.ReviewCount,
        r.Rating
    FROM 
        Vehicles v
    LEFT JOIN Locations l ON v.LocationID = l.LocationID
    LEFT JOIN FuelTypes f ON v.FuelTypeID = f.FuelTypeID
    LEFT JOIN Owners o ON v.OwnerID = o.OwnerID
    LEFT JOIN RentalActivity r ON v.VehicleID = r.VehicleID
    """

    numberOfRows = """
    SELECT 
        COUNT(*)
    FROM 
        Vehicles v
    LEFT JOIN Locations l ON v.LocationID = l.LocationID
    LEFT JOIN FuelTypes f ON v.FuelTypeID = f.FuelTypeID
    LEFT JOIN Owners o ON v.OwnerID = o.OwnerID
    LEFT JOIN RentalActivity r ON v.VehicleID = r.VehicleID
    """
    # If there is a search term, add a WHERE clause to the SQL query
    if search:
        temp_search_param = ''
        if search_param == 'LocationCity':
           temp_search_param = 'City'
        elif search_param == 'LocationState':
            temp_search_param = 'State'
        elif search_param == 'LocationCountry':
            temp_search_param = 'Country'
        else:
            temp_search_param = search_param

        query += f" WHERE {temp_search_param} LIKE %s"
        numberOfRows += f" WHERE {temp_search_param} LIKE %s"
        search_pattern = f"%{search}%"
    
    # Add ORDER BY clause to SQL query
    query += f" ORDER BY {sort} {order}"

    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    offset = (page - 1) * per_page

    # Add limit and offset to your query
    paginated_query = query + " LIMIT %s OFFSET %s"

    # Execute the query with search terms if applicable
    conn = get_db_connection()
    cursor = conn.cursor()
    if search:
        cursor.execute(paginated_query, (search_pattern, per_page, offset))
    else:
        cursor.execute(paginated_query, (per_page, offset))
    vehicles = cursor.fetchall()
    
    if search:
        cursor.execute(numberOfRows, (search_pattern))
    else:
        cursor.execute(numberOfRows)
    count_result = cursor.fetchone()

    # Extract the total count from the result
    total_count = count_result['COUNT(*)'] if count_result else 0

    cursor.close()
    conn.close()

    total_pages = (total_count + per_page - 1) // per_page

    return render_template('index.html', vehicles=vehicles, sort=sort, order=order, search_param=search_param, search=search, page=page, total_pages=total_pages, per_page=per_page, username=username)

@app.route('/plot')
def plot_view():
    search_param = request.args.get('search_param', 'Make')
    search = request.args.get('search', '')

    query = """
    SELECT 
        COUNT(*),
        l.State as LocationState
    FROM 
        Vehicles v
    LEFT JOIN Locations l ON v.LocationID = l.LocationID
    LEFT JOIN FuelTypes f ON v.FuelTypeID = f.FuelTypeID
    LEFT JOIN Owners o ON v.OwnerID = o.OwnerID
    LEFT JOIN RentalActivity r ON v.VehicleID = r.VehicleID
    """
    if search:
        temp_search_param = ''
        if search_param == 'LocationCity':
           temp_search_param = 'City'
        elif search_param == 'LocationState':
            temp_search_param = 'State'
        elif search_param == 'LocationCountry':
            temp_search_param = 'Country'
        else:
            temp_search_param = search_param

        query += f" WHERE {temp_search_param} LIKE %s"
        search_pattern = f"%{search}%"
    query += " GROUP BY State"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    if search:
        cursor.execute(query, (search_pattern))
    else:
        cursor.execute(query)
    
    vehicleDataByState = cursor.fetchall()
    x_data = []
    y_data = []

    for item in vehicleDataByState:
        x_data.append(item['LocationState'])
        y_data.append(item['COUNT(*)'])

    return render_template('plot.html', x_data=x_data, y_data=y_data)

@app.route('/plotScatter')
def plot_view_1():
    search_param = request.args.get('search_param', 'Make')
    search = request.args.get('search', '')

    query = """
    SELECT 
        r.RenterTripsTaken,
        r.Rating
    FROM 
        Vehicles v
    LEFT JOIN Locations l ON v.LocationID = l.LocationID
    LEFT JOIN FuelTypes f ON v.FuelTypeID = f.FuelTypeID
    LEFT JOIN Owners o ON v.OwnerID = o.OwnerID
    LEFT JOIN RentalActivity r ON v.VehicleID = r.VehicleID
    """
    if search:
        temp_search_param = ''
        if search_param == 'LocationCity':
           temp_search_param = 'City'
        elif search_param == 'LocationState':
            temp_search_param = 'State'
        elif search_param == 'LocationCountry':
            temp_search_param = 'Country'
        else:
            temp_search_param = search_param

        query += f" WHERE {temp_search_param} LIKE %s LIMIT 1000"
        search_pattern = f"%{search}%"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    if search:
        cursor.execute(query, (search_pattern))
    else:
        cursor.execute(query)
    
    vehicles = cursor.fetchall()

    return render_template('plot_2.html', vehicles = vehicles)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        return redirect(url_for('index', username=username))
    return render_template('login.html')

@app.route('/create', methods=["POST"])
def create():
    # Add Creation Logic from Form Data
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Insert or ignore into FuelTypes
            sql = "INSERT IGNORE INTO FuelTypes (FuelType) VALUES (%s)"
            cursor.execute(sql, (request.form['FuelType'],))
            connection.commit()

            # Get FuelTypeID
            sql = "SELECT FuelTypeID FROM FuelTypes WHERE FuelType = %s"
            cursor.execute(sql, (request.form['FuelType'],))
            fuel_type_id = cursor.fetchone()['FuelTypeID']

            # Insert into Locations
            sql = """
                INSERT INTO Locations (Latitude, Longitude, City, State, Country)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (request.form['Latitude'], request.form['Longitude'], request.form['LocationCity'], request.form['LocationState'], request.form['LocationCountry']))
            location_id = connection.insert_id()
            connection.commit()

            # Insert into Owners (assuming you know the owner or create new)
            sql = "INSERT INTO Owners () VALUES ()"
            cursor.execute(sql)
            owner_id = connection.insert_id()
            connection.commit()

            # Insert into Vehicles
            sql = """
                INSERT INTO Vehicles (Make, Model, Type, Year, FuelTypeID, RateDaily, OwnerID, LocationID, NearestAirportCity)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (request.form['Make'], request.form['Model'], request.form['Type'], request.form['Year'], fuel_type_id, request.form['RateDaily'], owner_id, location_id, request.form['NearestAirportCity']))
            vehicle_id = connection.insert_id()
            connection.commit()

            # Insert into RentalActivity if applicable
            sql = """
                INSERT INTO RentalActivity (VehicleID, RenterTripsTaken, ReviewCount, Rating)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (vehicle_id, request.form.get('RenterTripsTaken', 0), request.form.get('ReviewCount', 0), request.form.get('Rating', 0)))
            connection.commit()

    finally:
        connection.close()
    
    return redirect(url_for('index')) 

@app.route('/create_vehicle')
def create_vehicle():
    return render_template('create.html')

@app.route('/edit', methods=['POST'])
def edit():
    connection = get_db_connection()
    vehicle_id = request.form['vehicle_id']

    try:
        with connection.cursor() as cursor:
            # Update FuelTypes table if necessary
            if 'FuelType' in request.form:
                # Ensure the FuelType exists or insert new
                sql = """
                INSERT INTO FuelTypes (FuelType) 
                VALUES (%s) ON DUPLICATE KEY UPDATE FuelTypeID=LAST_INSERT_ID(FuelTypeID)
                """
                cursor.execute(sql, (request.form['FuelType'],))
                fuel_type_id = connection.insert_id()
                connection.commit()

                # Update Vehicles table with the new FuelTypeID
                sql = "UPDATE Vehicles SET FuelTypeID = %s WHERE VehicleID = %s"
                cursor.execute(sql, (fuel_type_id, vehicle_id))

            # Update Locations table if necessary
            if all(key in request.form for key in ['Latitude', 'Longitude', 'LocationCity', 'LocationState', 'LocationCountry']):
                sql = """
                UPDATE Locations
                SET Latitude = %s, Longitude = %s, City = %s, State = %s, Country = %s
                WHERE LocationID = (SELECT LocationID FROM Vehicles WHERE VehicleID = %s)
                """
                cursor.execute(sql, (request.form['Latitude'], request.form['Longitude'], request.form['LocationCity'], request.form['LocationState'], request.form['LocationCountry'], vehicle_id))

            # Update Vehicles table
            sql = """
            UPDATE Vehicles
            SET Make = %s, Model = %s, Type = %s, Year = %s, RateDaily = %s, NearestAirportCity = %s
            WHERE VehicleID = %s
            """
            cursor.execute(sql, (
                request.form['Make'], request.form['Model'], request.form['Type'], 
                request.form['Year'], request.form['RateDaily'], request.form['NearestAirportCity'], 
                vehicle_id
            ))

            # Update RentalActivity table if necessary
            if any(key in request.form for key in ['RenterTripsTaken', 'ReviewCount', 'Rating']):
                sql = """
                UPDATE RentalActivity
                SET RenterTripsTaken = %s, ReviewCount = %s, Rating = %s
                WHERE VehicleID = %s
                """
                cursor.execute(sql, (
                    request.form.get('RenterTripsTaken', 0), 
                    request.form.get('ReviewCount', 0), 
                    request.form.get('Rating', 0), 
                    vehicle_id
                ))

            connection.commit()
    except Exception as e:
        print("An error occurred:", e)
        connection.rollback()
    finally:
        connection.close()
        return redirect(url_for('index'))

@app.route('/get_vehicle/<int:id>')
def get_vehicle(id):
    # Retrieve the vehicle data from the database
    vehicle = get_vehicle_by_id(id)
    return render_template('Edit.html', vehicle=vehicle)

@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
        # Assuming you get form data to update the vehicle
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Check if the vehicle exists and fetch associated LocationID and OwnerID
            sql = "SELECT LocationID, OwnerID FROM Vehicles WHERE VehicleID = %s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
            if result is None:
                return "Vehicle not found", 404

            location_id = result['LocationID']
            owner_id = result['OwnerID']

            # Delete from RentalActivity first
            sql = "DELETE FROM RentalActivity WHERE VehicleID = %s"
            cursor.execute(sql, (id,))

            # Delete the vehicle itself
            sql = "DELETE FROM Vehicles WHERE VehicleID = %s"
            cursor.execute(sql, (id,))
            
            # Check if no other vehicles are linked to this LocationID and delete if not
            sql = "SELECT COUNT(*) AS count FROM Vehicles WHERE LocationID = %s"
            cursor.execute(sql, (location_id,))
            if cursor.fetchone()['count'] == 0:
                sql = "DELETE FROM Locations WHERE LocationID = %s"
                cursor.execute(sql, (location_id,))

            # Check if no other vehicles are linked to this OwnerID and delete if not
            sql = "SELECT COUNT(*) AS count FROM Vehicles WHERE OwnerID = %s"
            cursor.execute(sql, (owner_id,))
            if cursor.fetchone()['count'] == 0:
                sql = "DELETE FROM Owners WHERE OwnerID = %s"
                cursor.execute(sql, (owner_id,))

            connection.commit()
    except Exception as e:
        print("An error occurred:", e)
        connection.rollback()
        return "Error during deletion", 500
    finally:
        connection.close()
        return redirect(url_for('index'))

def get_vehicle_by_id(vehicle_id):
    # get Vehicle By ID
    query = f"""
        SELECT 
        v.VehicleID, 
        v.Make, 
        v.Model, 
        v.Type, 
        v.Year, 
        v.RateDaily, 
        v.NearestAirportCity,
        l.Latitude,
        l.Longitude, 
        l.City as LocationCity,
        l.State as LocationState,
        l.Country as LocationCountry,
        f.FuelType,
        o.OwnerID,
        r.RenterTripsTaken,
        r.ReviewCount,
        r.Rating
        FROM 
            Vehicles v
        LEFT JOIN Locations l ON v.LocationID = l.LocationID
        LEFT JOIN FuelTypes f ON v.FuelTypeID = f.FuelTypeID
        LEFT JOIN Owners o ON v.OwnerID = o.OwnerID
        LEFT JOIN RentalActivity r ON v.VehicleID = r.VehicleID
        WHERE v.VehicleID = {vehicle_id}
        """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    vehicle = cursor.fetchone()

    return vehicle

if __name__ == "__main__":
    app.run(debug=True)
