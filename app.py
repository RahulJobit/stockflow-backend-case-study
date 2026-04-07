@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json

    if not data.get('name') or not data.get('sku'):
        return {"error": "Missing required fields"}, 400

    existing = Product.query.filter_by(sku=data['sku']).first()
    if existing:
        return {"error": "SKU already exists"}, 400

    try:
        product = Product(
            name=data['name'],
            sku=data['sku'],
            price=float(data['price'])
        )

        db.session.add(product)
        db.session.flush()

        inventory = Inventory(
            product_id=product.id,
            warehouse_id=data['warehouse_id'],
            quantity=data.get('initial_quantity', 0)
        )

        db.session.add(inventory)
        db.session.commit()

        return {"message": "Product created", "product_id": product.id}, 201

    except Exception:
        db.session.rollback()
        return {"error": "Something went wrong"}, 500
