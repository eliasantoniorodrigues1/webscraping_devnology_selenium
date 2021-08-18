from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(260), nullable=False)
    review = db.Column(db.String(20))
    rating = db.Column(db.String(10))

    def __repr__(self):
        return f"{self.title} - {self.price} - {self.description} - {self.review} - {self.rating}"

# Route: GET ALL
@app.route('/products')
def get_products():
    products = Product.query.all()

    output = []
    for product in products:
        product_data = {'title': product.title, 'price': product.price,
                        'description': product.description,
                        'review': product.review,
                        'rating': product.rating
                        }
        output.append(product_data)
    return {'products': output}

# Route: Select a specific product:
@app.route('/products/<id>')
def get_product(id):
    product = Product.get_or_404(id)
    return {'title': product.title, 'price': product.price,
            'description': product.description,
            'review': product.review,
            'rating': product.rating
            }

# Route: adding product:
@app.route('/products', methods=['POST'])
def add_product():
    product = Product(title=request.json['title'],
                      price=request.json['price'],
                      description=request.json['description'],
                      review=request.json['review'],
                      rating=request.json['rating']
                      )
    db.session.add(product)
    db.session.commit()
    return {'id': product.id}

# Deleting an item:
@app.route('/products/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if product is None:
        return {'error': 'Product not found...'}
    db.session.delete(product)
    db.session.commit()
    return {'message': 'Product deleted...'}


if __name__ == '__main__':
    app.run(debug=True)
