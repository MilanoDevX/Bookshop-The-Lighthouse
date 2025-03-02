from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    full_name = db.Column(db.String(200), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name
            # do not serialize the password, its a security breach
        }
    

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=False, nullable=False)
    books = db.relationship("Book", back_populates="author") 

    def __repr__(self):
        return f'<Author {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Book(db.Model):
    __tablename__ = "Books" # para dar nombre a la tabla en psql
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id")) # This is necessary because the relationship stablished in Author class.
    author = db.relationship("Author", back_populates="books")
    
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __repr__(self):
        return f'<Book {self.id}>'

    def serialize(self):
        author_data = self.author.serialize() if self.author != None else "Unknown" # It serializes the author instance including his id and name (see serialize func in Author class)
                                                                                    # Also, it verifies if author exists. If not, assign "Unknown" value.
        return {
            "id": self.id,
            "title": self.title,
            "author": author_data
        }
    