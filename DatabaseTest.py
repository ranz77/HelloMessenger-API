def test_database(cursor):
    cursor.execute("insert into auth values ('id', 'token')")
    cursor.execute("select id from auth where token = 'token';")
    return cursor.fetchone()

def test_add(cursor):
    cursor.execute("insert into auth values ('id1', 'token1')")
    return "success!"

def test_get(cursor):
    cursor.execute("select id from auth where token = 'token1'")
    return cursor.fetchone()
