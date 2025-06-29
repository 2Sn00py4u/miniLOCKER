""" --- crypting ---
print(hash:=encrypting("admin", "admin"))
print(decrypting(hash, "admin"))
print(compare_encrypted("admin", "admin", hash))"""

"""  --- duck_dbms ---
dbms = DBMS("backend\\l0ck3rdb.duckdb")
print(dbms.execute("SELECT * FROM users", True))

print(dbms.deleteValues("users", "username = 'user'"))
print(dbms.execute("SELECT * FROM users", True))"""
