from .models import db, Product

def get_all_products():
  
    products = Product.query.all()
    return [product.to_dict() for product in products]


def add_new_product(data):
  
    new_product = Product(
        name=data["name"],
        description=data.get("description"),
        price=data["price"],
        stock=data["stock"],
        image=data.get("image")  
    )
    db.session.add(new_product)
    db.session.commit()
    return {"message": "Produto adicionado com sucesso!", "product": new_product.to_dict()}


def update_existing_product(product_id, data):
    product = Product.query.get_or_404(product_id)
    product.name = data.get("name", product.name)
    product.description = data.get("description", product.description)
    product.price = data.get("price", product.price)
    product.stock = data.get("stock", product.stock)
    product.image = data.get("image", product.image)  

    db.session.commit()
    return {"message": "Produto atualizado com sucesso!", "product": product.to_dict()}


def delete_existing_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)  
    db.session.commit()
    return {"message": "Produto excluído com sucesso!"}

