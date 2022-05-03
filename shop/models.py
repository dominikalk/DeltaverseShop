from shop import db

cart = db.Table('cart',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True),
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(200), unique=True, nullable=False)
    cart = db.relationship("Item", secondary=cart)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}')"    

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship("Category")
    description = db.Column(db.Text, nullable=False)
    picture = db.Column(db.String(100), nullable=False, default='default.jpg')
    price = db.Column(db.Integer, nullable=False)
    carbon = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Item('{self.id}', '{self.name}')"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True, nullable=False)

    def __repr__(self):
        return f"Category('{self.id}', '{self.name}')"

