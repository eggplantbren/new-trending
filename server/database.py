import apsw

DECAY_TIMESCALE = 500

class Database:
    def __init__(self):
        self.conn = apsw.Connection("trending.db")
        self.db = self.conn.cursor()

        self.pragmas()
        self.begin()
        self.create_tables()
        self.commit()

    def pragmas(self):
        self.execute("PRAGMA JOURNAL_MODE = WAL;")
        self.execute("PRAGMA SYNCHRONOUS = 0;")

    def execute(self, *args, **kwargs):
        return self.db.execute(*args, **kwargs)

    def begin(self):
        self.execute("BEGIN;")

    def commit(self):
        self.execute("COMMIT;")

    def create_tables(self):
        self.execute("""
        CREATE TABLE IF NOT EXISTS claims
            (claim_hash BYTES NOT NULL PRIMARY KEY)
            WITHOUT ROWID;
            """)

        self.execute("""
        CREATE TABLE IF NOT EXISTS kernels
            (id        INTEGER NOT NULL PRIMARY KEY,
             claim     BYTES NOT NULL,
             t0        INTEGER NOT NULL,
             old_lbc   REAL NOT NULL,
             new_lbc   REAL NOT NULL,
             amplitude REAL NOT NULL,
             t_peak    REAL NOT NULL,
             sharpen   REAL NOT NULL,
             FOREIGN KEY (claim) REFERENCES claims (claim_hash));
            """)

        self.execute("""
        CREATE TABLE IF NOT EXISTS trending_scores
            (claim BYTES NOT NULL,
             time  INTEGER NOT NULL,
             score REAL NOT NULL,
             PRIMARY KEY (claim, time),
             FOREIGN KEY (claim) REFERENCES claims (claim_hash))
            WITHOUT ROWID;
            """)

