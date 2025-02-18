import db.db as db
from db.User import User

class Attempt:
    def __init__(self):
        self.id = None
        self.user_id = None
        self.date = None
        self.attempt_time = None
        self.score = None
        self.passed = None

        self.user = None

    def __str__(self):
        return f'Attempt: {self.id}, {self.user_id}, {self.date}, {self.attempt_time}, {self.score}'

    @staticmethod
    def create(user_id, date, attempt_time, score, passed):
        cur = db.conn.cursor()
        cur.execute('''
        INSERT INTO attempts (user_id, date, attempt_time, score, passed)
        VALUES (?, ?, ?, ?, ?)
        ''', (user_id, date, attempt_time, score, passed))
        db.conn.commit()

        att = Attempt.get_by_id(cur.lastrowid)
        cur.close()
        return att

    @staticmethod
    def get_by_id(id):
        attempt = db.conn.execute('''
        SELECT * FROM attempts
        WHERE id = ?
        ''', (id,)).fetchone()

        if attempt:
            att = Attempt()
            att.id = attempt[0]
            att.user_id = attempt[1]
            att.date = attempt[2]
            att.attempt_time = attempt[3]
            att.score = attempt[4]
            att.passed = attempt[5]

            att.user = User.get_by_id(att.user_id)

            return att
        else:
            return None

if __name__ == "__main__":
    usr = User.create('test')
    att = Attempt.create(usr.id, '2021-01-01', 100, 100) 


