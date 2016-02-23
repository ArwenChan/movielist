import sqlite3


def store(movies, year):
    conn = sqlite3.connect('movies.db')
    curs = conn.cursor()
    query = 'INSERT or IGNORE  into Movies values (NULL,?,?,?,?,?,?,?)'
    for movie in movies:
        sqlmovie = [movie['name'][0], movie['name'][1] if len(movie['name']) > 1 else None, ' / '.join(movie['info']), movie['rating'], movie['rates_nums'], year, 0]
        curs.execute(query, sqlmovie)

    conn.commit()
    conn.close()


def renew():
    conn = sqlite3.connect('movies.db')
    curs = conn.cursor()
    try:
        curs.execute('''
            CREATE TABLE Movies(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name1 TEXT UNIQUE,
            name2 TEXT,
            info TEXT,
            rating FLOAT,
            rates_nums INTEGER,
            year TEXT,
            seen BOOLEAN
                )
        ''')

        conn.commit()
    except:
        pass
    # Movies maybe exist.
    conn.close()

if __name__ == '__main__':
    renew()
