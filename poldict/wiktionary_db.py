import sqlite3


class PageDb:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)

    def create(self):
        self.conn.executescript(
            """
            DROP TABLE IF EXISTS pages;
        
            CREATE TABLE pages (
                title TEXT,
                text TEXT,
                PRIMARY KEY(title)
            );
            """)

    def close(self):
        self.conn.close()

    def save_page(self, title, text):
        self.conn.execute('INSERT INTO pages (title, text) VALUES (?, ?)',
                          (title, text))
        self.conn.commit()

    def get_page(self, title):
        res = self.conn.execute('SELECT text FROM pages WHERE title=?', (title,))
        return res.fetchone()[0]

