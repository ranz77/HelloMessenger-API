def reset_database(cursor):
    try:
        cursor.execute("delete from auth")
        return 'success!'
    finally:
        return 'failed'
