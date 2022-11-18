from db import db
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Books(db.Model):
    __tablename__ = 'Books'

    id = db.Column(db.String, name="uuid", primary_key=True, default=generate_uuid)
    title = db.Column(db.String(80))
    author = db.Column(db.String(80))
    read = db.Column(db.Boolean)

    def __init__(self, title, author, read):
        self.id = generate_uuid()
        self.title = title
        self.author = author
        self.read = read

    def json(self):
        return {'id': self.id, 'title':self.title, 'author':self.author, 'read':self.read}

    @classmethod      
    def find_by_id(cls, id):   
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_books(cls):
        return [book.json() for book in cls.query.all()]


