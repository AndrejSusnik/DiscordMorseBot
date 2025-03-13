import db.db as db
import enum

class TimeMode(enum.Enum):
    DAILY = 0
    MOTHLY = 1
    ALLTIME = 2

class User:
    def __init__(self):
        self.id = None
        self.discord_name = None 
        self.display_name = None

        self.attempts = None

    def __eq__(self, value):
        return self.id == value.id

    def __str__(self):
        return f'User: {self.id}, {self.discord_name}, {self.display_name}'

    @staticmethod
    def create(discord_name, display_name=''):
        cur = db.conn.cursor()
        cur.execute('''
        INSERT INTO users (discord_name, display_name)
        VALUES (?, ?)
        ''', (discord_name, display_name))
        cur.close()
        db.conn.commit()

        return User.get_by_discord_name(discord_name) 

    @staticmethod
    def get_by_discord_name(discord_name):
        cur = db.conn.cursor()
        usr = cur.execute('''
        SELECT * FROM users
        WHERE discord_name = ?
        ''', (discord_name,)).fetchone()

        cur.close()

        if usr:
            user = User()
            user.id = usr[0]
            user.discord_name = usr[1]
            user.display_name = usr[2]

            return user
        else:
            None

        return None
    
    @staticmethod
    def get_by_id(id):
        cur = db.conn.cursor()
        usr = cur.execute('''
        SELECT * FROM users
        WHERE id = ?
        ''', (id,)).fetchone()

        cur.close()

        if usr:
            user = User()
            user.id = usr[0]
            user.discord_name = usr[1]
            user.display_name = usr[2]

            return user
        else:
            None

        return None

    def get_stats(self, mode: TimeMode):
        pass

    @staticmethod
    def get_ranking(mode: TimeMode):
        # get all attempts made in specified mode
        # group by user
        # sum the score
        # order by score
        # return the display_name and score 

        cur = db.conn.cursor()

        if mode == TimeMode.ALLTIME:
            sql = '''
            SELECT u.discord_name, SUM(a.score) as score
            FROM users u
            JOIN attempts a ON u.id = a.user_id
            WHERE a.passed = 1
            GROUP BY u.id
            ORDER BY score DESC
            '''
        elif mode == TimeMode.MOTHLY:
            # get rankings in the current month
            sql = '''
            SELECT u.discord_name, SUM(a.score) as score
            FROM users u
            JOIN attempts a ON u.id = a.user_id
            WHERE a.passed = 1 AND a.date > date('now', '-1 month')
            GROUP BY u.id
            ORDER BY score DESC
            '''
        elif mode == TimeMode.DAILY:
            sql = '''
            SELECT u.discord_name, SUM(a.score) as score
            FROM users u
            JOIN attempts a ON u.id = a.user_id
            WHERE a.passed = 1 AND a.date > date('now', '-1 day')
            GROUP BY u.id
            ORDER BY score DESC
            '''

        cur.execute(sql)
        ranking = cur.fetchall()
        
        cur.close()
        return "\n".join([f'{r[0]}: {r[1]}' for r in ranking])
    

if __name__ == "__main__":
    # usr = User.create('test', 'test')
    # usr2 = User.get_by_discord_name('test')

    # print(usr)
    # print(usr2)

    # print(usr == usr2)
    ranking = User.get_ranking(TimeMode.ALLTIME)
    Ranking = User.get_ranking(TimeMode.MOTHLY)
    ranking = User.get_ranking(TimeMode.DAILY)

