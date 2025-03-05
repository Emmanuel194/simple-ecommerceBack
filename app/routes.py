from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, Product, Payment, User
from .pix_services import montar_payload_pix, gerar_qr_code_pix
from .product_services import get_all_products, add_new_product, update_existing_product, delete_existing_product
from .utils.token_utils import generate_token, token_required
from sqlalchemy import func


main = Blueprint('main', __name__)

### ROTAS DE PRODUTOS ###
@main.route('/products', methods=['GET'])
def get_products():
    return jsonify(get_all_products())


@main.route('/products', methods=['POST'])
def add_product():
    try:
        data = request.get_json()
        result = add_new_product(data)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@main.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        data = request.get_json()
        result = update_existing_product(product_id, data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@main.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        result = delete_existing_product(product_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


### ROTAS DE USUÁRIOS ###
@main.route('/users/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "user")  

    if not username or not password:
        return jsonify({"message": "Usuário e senha são obrigatórios!"}), 400

    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
    new_user = User(username=username, password=hashed_password, role=role)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuário cadastrado com sucesso!"}), 201


@main.route('/users/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Usuário ou senha inválidos!"}), 401

    token = generate_token(user)

    return jsonify({"token": token}), 200


@main.route('/users/protected', methods=['GET'])
@token_required
def protected_route(current_user):
    return jsonify({"message": f"Bem-vindo {current_user.username}!", "role": current_user.role})


### ROTAS QRCODE E PAYMENTS ###
@main.route("/pix/qrcode", methods=["POST"])
def gerar_pix_qrcode():
    try:
        data = request.get_json()
        valor = float(data.get("valor"))
        descricao = data.get("descricao", "Pagamento na loja")
        chave_pix = "emanuel_lima2011@hotmail.com"
      
        payload_pix = montar_payload_pix(chave_pix, valor, descricao)

        qr_code_base64 = gerar_qr_code_pix(payload_pix)

        return jsonify({"qrcode": qr_code_base64, "payload": payload_pix})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@main.route('/payments', methods=['GET'])
def list_payments():
    status = request.args.get("status") 
    if status:
        payments = Payment.query.filter_by(status=status).all()
    else:
        payments = Payment.query.all()
    return jsonify([payment.to_dict() for payment in payments])


@main.route('/payments/<int:payment_id>/confirm', methods=['PUT'])
def confirm_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    if payment.status == "Confirmado":
        return {"error": "Pagamento já está confirmado."}, 400

    payment.status = "Confirmado"
    db.session.commit()
    return {"message": "Pagamento confirmado com sucesso!", "payment_id": payment.id}


@main.route('/payments/<int:payment_id>/cancel', methods=['PUT'])
def cancel_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    if payment.status == "Cancelado":
        return {"error": "Pagamento já está cancelado."}, 400

    payment.status = "Cancelado"
    db.session.commit()
    return {"message": "Pagamento cancelado com sucesso!", "payment_id": payment.id}


@main.route('/sales-statistics', methods=['GET'])
def get_sales_statistics():
    results = (
        db.session.query(
            func.strftime('%m', Payment.created_at).label('month'), 
            func.count(Payment.id).label('sales_count') 
        )
        .filter(Payment.status == "Confirmado")  
        .group_by(func.strftime('%m', Payment.created_at))  
        .order_by(func.strftime('%m', Payment.created_at))  
        .all()
    )
    
    data = [{"month": row.month, "sales": row.sales_count} for row in results]

    return jsonify(data)
