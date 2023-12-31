import pymysql

def get_current_users_and_roles_mysql(db_host, db_name, db_user, db_password):
    '''
    return a list of users and roles for the given mysql db
    '''
    conn = None # Initialize conn to None outside of the try block
    # Connect to the RDS database and query for user data
    try:
        # Connection to the database
        conn = pymysql.connect(host=db_host, user=db_user, passwd=db_password, db=db_name, connect_timeout=5)
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # Assuming 'user_accounts' is a table in your database
            cursor.execute("SELECT user as user_name FROM mysql.user;")
            users = cursor.fetchall()  # Fetches all user rows
            for user in users:
                print(str('users') + user['user_name'])

            # Assuming 'user_roles' is a table or a field in your database
            cursor.execute("SELECT user AS role_name FROM mysql.user WHERE host = '%' AND NOT LENGTH(authentication_string);")
            #TODO the above command is not working properly and needs to be updated
            roles = cursor.fetchall()  # Fetches all role rows
            print('role fetching' + str(roles))
            for role in roles:
                print('roles' + role['role_name'])

        # Transform the query results into lists of usernames and role names
        user_list = [user['user_name'] for user in users]
        role_list = [role['role_name'] for role in roles]

        return user_list, role_list

    except pymysql.MySQLError as e:
        print("Error connecting to MariaDB Platform: {}".format(e))
        return [], []  # Return empty lists in case of error

    finally:
        if conn is not None and conn.open:
            conn.close()
