import apsw
import math

DECAY_TIMESCALE = 500
DELAY_POWER = 0.4


def soften(lbc):
    """
    Nonlinear softening function.
    """
    if lbc < 1E2:
        return (lbc/1E2)           # Maxes out at 1
    elif lbc < 1E3:
        return (lbc/1E2)**0.5      # Maxes out at 10^(1/2)
    elif lbc < 1E4:
        return 3.1622776601683795*(lbc/1E3)**0.33333333  # Maxes out at 10^(5/6)
    elif lbc < 1E5:
        return 6.812920690579613*(lbc/1E4)**0.25   # Maxes out at 10^(13/12)
    elif lbc < 1E6:
        return 12.115276586285882*(lbc/1E5)**0.2   # Maxes out at 10^(77/60)
    else:
        return 19.20141938638802*(lbc/1E6)**0.16666667


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
            (claim_hash BYTES NOT NULL PRIMARY KEY,
             lbc        REAL NOT NULL)
            WITHOUT ROWID;
            """)

        self.execute("""
        CREATE TABLE IF NOT EXISTS kernels
            (claim     BYTES NOT NULL,
             t0        INTEGER NOT NULL,
             old_lbc   REAL NOT NULL,
             new_lbc   REAL NOT NULL,
             amplitude REAL NOT NULL,
             t_peak    REAL NOT NULL,
             sharpen   REAL NOT NULL,
             PRIMARY KEY (claim, t0),
             FOREIGN KEY (claim) REFERENCES claims (claim_hash))
            WITHOUT ROWID;
            """)

        self.execute("""
        CREATE TABLE IF NOT EXISTS trending_scores
            (claim BYTES NOT NULL,
             time  INTEGER NOT NULL,
             score REAL NOT NULL DEFAULT 0.0,
             PRIMARY KEY (claim, time),
             FOREIGN KEY (claim) REFERENCES claims (claim_hash))
            WITHOUT ROWID;
            """)

    def insert_claim(self, time, claim_hash, lbc):
        """
        Insert a claim.
        """
        # Insert the claim.
        self.execute("INSERT INTO claims VALUES (?, ?);",
                     (claim_hash, lbc))

        # Insert the kernel
        self.insert_kernel(claim_hash, time, 0.0, lbc)

    def insert_kernel(self, claim_hash, t0, old_lbc, new_lbc):
        t_peak = t0 + new_lbc**DELAY_POWER
        A = soften(new_lbc) - soften(old_lbc)
        A += 10.0*soften(new_lbc - old_lbc) \
                /((new_lbc + 100.0) / 100.0)**2
        sharpen = 1.0
        if new_lbc >= 100.0:
            sharpen = 1.0 + 2*math.log10(new_lbc/100.0)

        self.execute("INSERT INTO kernels VALUES (?, ?, ?, ?, ?, ?, ?);",
                     (claim_hash, t0, old_lbc, new_lbc,
                      A, t_peak, sharpen))

        # Apply the kernel
        for t in range(t0, t0+2001):
            y = math.exp(-abs(t - t_peak)/DECAY_TIMESCALE)
            y = A*y**sharpen
            self.execute("INSERT INTO trending_scores VALUES (?, ?, ?)\
                          ON CONFLICT (claim, time) DO UPDATE\
                          SET score = score + ?;",
                          (claim_hash, t, y, y))



if __name__ == "__main__":
    database = Database()
    database.begin()
    database.insert_claim(0, "hello", 1.0)
    database.insert_kernel("hello", 50, 1.0, 1000.0)
    database.commit()


