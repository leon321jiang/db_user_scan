import pymysql

# Connection parameters
host_name = 'mydbinstance.cu53kqprya26.us-west-2.rds.amazonaws.com'  # Replace with your host, often it's 'localhost' or an IP address
db_host = 'mytestsql_db'      # Replace with the name of your database
db_user = 'db_admin'    # Replace with your MySQL admin user
db_password = 'QASEFduey34!'  # Replace with your MySQL admin password

# User details to create
new_username = 'new_user4'  # Replace with the new username you want to create
new_password = 'new_password1'  # Replace with the new user's password
new_user_host = '%'  # '%' allows connection from any host, replace with a specific hostname or IP if needed
new_role = 'new_role1'

# Connect to the MySQL server
connection = pymysql.connect(host=host_name, user=db_user, password=db_password)

try:
    with connection.cursor() as cursor:
        # Create a new user with all privileges on the specific database
        sql = f"CREATE USER '{new_username}'@'{new_user_host}' IDENTIFIED BY '{new_password}';"
        cursor.execute(sql)
        
        # Grant all privileges on the database to the new user
        sql = f"GRANT ALL PRIVILEGES ON `{db_host}`.* TO '{new_username}'@'{new_user_host}';"
        cursor.execute(sql)

        # It is important to flush privileges to ensure that the changes take effect
        sql = "FLUSH PRIVILEGES;"
        cursor.execute(sql)

        #create a new role 
        sql = f"CREATE ROLE '{new_role}';"

        # Commit the changes
        connection.commit()

        print(f"User {new_username} created successfully and granted all privileges on database {db_host}.")

except pymysql.MySQLError as e:
    print(f"Error: {e}")
    
finally:
    connection.close()
