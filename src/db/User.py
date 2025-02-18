import db.db as db

class User:
    def __init__(self):
        self.id = None
        self.discord_name = None 
        self.display_name = None

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
    

if __name__ == "__main__":
    usr = User.create('test', 'test')
    usr2 = User.get_by_discord_name('test')

    print(usr)
    print(usr2)

    print(usr == usr2)

