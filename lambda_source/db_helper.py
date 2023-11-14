def get_current_users_and_roles(db_name, db_host, db_user, db_password, db_engine):
    '''
    Main db helper to call respective helper based on engine types
    '''
    if db_engine == 'mysql':
        from db_helper_mysql import get_current_users_and_roles_mysql
        return get_current_users_and_roles_mysql(db_name, db_host, db_user, db_password)
    elif db_engine == 'postgres':
        from db_helper_postgres import get_current_users_and_roles_postgres
        return get_current_users_and_roles_postgres(db_name, db_host, db_user, db_password)
    elif db_engine == 'oracle':
        from db_helper_oracle import get_current_users_and_roles_oracle
        return get_current_users_and_roles_oracle(db_name, db_host, db_user, db_password)
    else:
        return {'statusCode': 500, 'body': f"Unsupported database engine {db_engine}"}    
