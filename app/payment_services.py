from .models import db, Product, Payment

def validate_payment(data):
    pix_key = data.get("pix_key")
    amount = data.get("amount")
    description = data.get("description", "Sem descrição")

    if not pix_key or not amount:
        return {"error": "Chave PIX e valor são obrigatórios"}, 400

    product = Product.query.filter_by(price=amount).filter(Product.stock > 0).first()
    if not product:
        return {"error": "Nenhum produto correspondente ou disponível encontrado"}, 404

    payment = Payment(
        pix_key=pix_key,
        amount=amount,
        description=description,
        status="Pendente" 
    )
    db.session.add(payment)
    db.session.commit()

    return {"message": "Pagamento gerado com sucesso!", "payment_id": payment.id}, 201
