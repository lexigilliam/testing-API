from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

# import sqlite3
# from db import db

# class UserModel(db.Model): 
#     __tablename__ = 'users'
    
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80))
#     password = db.Column(db.String(80))

#     def __init__(self, _id, username, password):
#         self.id = _id #id is a python keyword so we use _id
#         self.username = username
#         self.password = password
    
#     @classmethod
#     def find_by_username(cls, username):
#         connection = sqlite3.connect('data.db')
#         cursor = connection.cursor()

#         query = "SELECT * FROM users WHERE username=?"
#         result = cursor.execute(query,(username,)) #always needs to be in the form of a tuple
#         row = result.fetchone()
#         if row:
#             # user = cls(row[0], row[1], row[2]) #need to make a class method because we call the class here
#             user = cls(*row) 
#         else:
#             user = None
        
#         connection.close()
#         return user

#     @classmethod
#     def find_by_id(cls, _id):
#         connection = sqlite3.connect('data.db')
#         cursor = connection.cursor()

#         query = "SELECT * FROM users WHERE id=?"
#         result = cursor.execute(query,(_id,)) 
#         row = result.fetchone()
#         if row:
#             user = cls(*row) 
#         else:
#             user = None
        
#         connection.close()
#         return user