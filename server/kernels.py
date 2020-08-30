import apsw
from database import Database

trending_db = Database()

def run(db, height, final_height, recalculate_claim_hashes):

    # Fetch changed/new claims from claims.db
    trending_db.begin()
    for row in db.execute(f"""
                         SELECT claim_hash,
                            1E-8*(amount + support_amount) AS lbc
                         FROM claim
                         WHERE claim_hash IN
                         ({','.join('?' for _ in recalculate_claim_hashes)});
                         """, recalculate_claim_hashes):
        claim_hash, lbc = row
        trending_db.insert_claim(claim_hash, lbc)

    trending_db.commit()



#if __name__ == "__main__":
#    conn = apsw.Connection(":memory:")
#    test_db = conn.cursor()
#    test_db.execute("CREATE TABLE 
