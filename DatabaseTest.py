def test_database(cursor):
    cursor.execute("select @@autocommit")
    return str(cursor.fetchone())

def test_add(cursor):
    cursor.execute("insert into auth values ('id1', 'token1')")
    return test_database(cursor)

def test_get(cursor):
    cursor.execute("select id from auth where token = 'token1'")
    return cursor.fetchone()
