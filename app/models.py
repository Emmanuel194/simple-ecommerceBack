from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(200))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "image": self.image,
        }

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pix_key = db.Column(db.String(100), nullable=False)  
    amount = db.Column(db.Float, nullable=False)  
    description = db.Column(db.String(200), nullable=True)  
    status = db.Column(db.String(20), default="Pendente")  
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp()) 

    def to_dict(self):
        return {
            "id": self.id,
            "pix_key": self.pix_key,
            "amount": self.amount,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

class User(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default="user")  
