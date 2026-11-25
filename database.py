from pathlib import Path
from contextlib import contextmanager
from flask import session, flash
import oracledb

BASE = Path(__file__).parent


# Oracle database connection
DSN = 'orsrv1.cs.torontomu.ca:1521/orcldb'
credentials = {}

# Database tables and their primary keys
TABLES = {
    'AUTHOR': ('AUTHORID',),
    'PUBLISHER': ('PUBLISHERID',),
    'BOOKS': ('BOOKID',),
    'BOOK_COPY': ('BOOKID', 'COPY_NUMBER'),
    'POSTAL_LOCATION': ('POSTAL_CODE',),
    'MEMBERS_3NF': ('MEMBERID',),
    'LIBRARIAN': ('LIBRARIANID',),
    'FINE': ('FINEID',),
    'WRITES': ('AUTHORID', 'BOOKID'),
    'BORROWS': ('MEMBERID', 'BOOKID', 'BORROW_DATE'),
    'RESERVES': ('MEMBERID', 'BOOKID', 'RESERVATION_DATE')
}

# Connect to Oracle
@contextmanager
def database():
    user, password = credentials[session['login_id']]
    with oracledb.connect(
        user=user,
        password=password,
        dsn=DSN
    ) as conn:
        with conn.cursor() as cur:
            yield conn, cur

# Execute SQL files
# Skip tables that already exist
def script(cur, name):
    skipped = 0
    for sql in (BASE / (name + '.sql')).read_text().split(';'):
        sql = sql.strip()
        if sql:
            # Skip tables that already exist
            if name == 'create' and sql.upper().startswith('CREATE TABLE '):
                table_name = sql.split()[2].upper()
                cur.execute(
                    "SELECT COUNT(*) FROM user_tables WHERE table_name = :t",
                    t=table_name
                )
                count = cur.fetchone()[0]
                if count > 0:
                    print(table_name + " already exists. Skipping.")
                    continue
            # Execute SQL statement
            try:
                cur.execute(sql)
            except oracledb.DatabaseError as e:
                # Skip duplicate records when populating
                if name == 'populate' and e.args[0].code == 1:
                    print("Duplicate record. Skipping:", sql)
                    skipped += 1
                    continue
                # Report all other database errors
                raise
    if skipped > 0:
        flash(str(skipped) + " duplicate inserts skipped.")
