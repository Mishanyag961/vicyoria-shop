from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'victoria_secret_neon_key_2026'

# Список товарів
products = [
    {
        'id': 1,
        'name': 'Сукня неонова',
        'price': 1200,
        'description': 'Елегантна вечірня сукня чудової якості. Ідеально підходить для святкових подій.',
        'main_image': 'https://picsum.photos/id/1025/400/400',
        'images': [
            'https://picsum.photos/id/1025/400/400',
            'https://picsum.photos/id/1062/400/400',
            'https://picsum.photos/id/1084/400/400'
        ]
    },
    {
        'id': 2,
        'name': 'Стильний піджак',
        'price': 1800,
        'description': 'Сучасний жіночий піджак вільного крою. Чудово поєднується як із джинсами, так і зі спідницею.',
        'main_image': 'https://picsum.photos/id/1059/400/400',
        'images': [
            'https://picsum.photos/id/1059/400/400',
            'https://picsum.photos/id/1060/400/400'
        ]
    },
    {
        'id': 3,
        'name': 'Шовкова блуза',
        'price': 850,
        'description': 'Ніжна та легка блуза з шовковим ефектом. Приємна до тіла та дуже стильна.',
        'main_image': 'https://picsum.photos/id/1070/400/400',
        'images': [
            'https://picsum.photos/id/1070/400/400'
        ]
    }
]

orders = []

@app.route('/')
def index():
    cart = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    success = request.args.get('success', False)
    return render_template('index.html', products=products, cart=cart, total=total, success=success)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', [])
    product = next((p for p in products if p['id'] == product_id), None)
    
    if product:
        found = False
        for item in cart:
            if item['id'] == product_id:
                item['quantity'] += 1
                found = True
                break
        if not found:
            cart.append({
                'id': product['id'],
                'name': product['name'],
                'price': product['price'],
                'quantity': 1
            })
        session['cart'] = cart

    return redirect(url_for('index'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    return redirect(url_for('index'))

@app.route('/checkout', methods=['POST'])
def checkout():
    name = request.form.get('name')
    phone = request.form.get('phone')
    address = request.form.get('address')
    cart = session.get('cart', [])

    if cart:
        order_data = {
            'name': name,
            'phone': phone,
            'address': address,
            'items': cart
        }
        orders.append(order_data)
        session['cart'] = []

    return redirect(url_for('index', success=True))

@app.route('/admin')
def admin():
    return render_template('admin.html', orders=orders, products=products)

@app.route('/add_product', methods=['POST'])
def add_product():
    global products
    new_id = max([p['id'] for p in products], default=0) + 1
    image_url = request.form.get('main_image')
    
    new_product = {
        'id': new_id,
        'name': request.form.get('name'),
        'price': int(request.form.get('price')),
        'description': request.form.get('description'),
        'main_image': image_url,
        'images': [image_url]
    }
    
    products.append(new_product)
    return redirect(url_for('admin'))

@app.route('/delete_product/<int:product_id>')
def delete_product(product_id):
    global products
    products = [p for p in products if p['id'] != product_id]
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
