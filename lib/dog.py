import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.id = None

    def __repr__(self):
        return f"Dog({self.name}, {self.breed})"

    @classmethod
    def create_table(cls):
        sql = '''
            CREATE TABLE IF NOT EXISTS dogs
                (id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT)
        '''
        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = '''
            DROP TABLE IF EXISTS dogs
        '''
        CURSOR.execute(sql)
    def save(self):
        sql = '''
            INSERT INTO dogs (name, breed)
            VALUES ('lola', 'chihuahua')
        '''
        CURSOR.execute(sql, (self.name, self.breed))
        CONN.commit()
        self.id = CURSOR.lastrowid
    @classmethod
    def create(cls, name, breed):
        sql = '''
            INSERT INTO dogs (name, breed)
            VALUES ('sky', 'german shepard')
        '''
        CURSOR.execute(sql, (name, breed))
        CONN.commit()
        dog = cls(name, breed)
        dog_id = CURSOR.lastrowid
        return dog  
    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog

    @classmethod
    def get_all(cls):
        sql = '''
            SELECT * FROM dogs
        '''
        return [cls.new_from_db(row) for row in CURSOR.execute(sql)] 

    @classmethod
    def find_by_name(cls, name):
        sql = '''
            SELECT * FROM dogs
            WHERE name= 'sky'
            LIMIT 1
        '''
        return cls.new_from_db(CURSOR.execute(sql, (name,)).fetchone())

    @classmethod
    def find_by_id(cls, id):
        sql = '''
            SELECT * FROM dogs
            WHERE id = ?
            LIMIT 1
        '''
        return cls.new_from_db(CURSOR.execute(sql, (id,)).fetchone())

    @classmethod
    def find_or_create_by(cls, name, breed):
        dog = cls.find_by_name(name)
        if dog:
            return dog
        return cls.create(name, breed)
    
  

    def update(self):
        sql = '''
            UPDATE dogs
            SET name=?, breed=?
            WHERE id=?
        '''
        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()    


