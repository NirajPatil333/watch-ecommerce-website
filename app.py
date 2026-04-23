from flask import Flask, render_template , session, redirect, url_for 
import json

app = Flask(__name__)
app.secret_key ='secret123'    #for encrypt

# product data loading 
def load_products():
    with open('products.json') as f :
        return json.load(f)
    

#home 
@app.route('/')
def home():
    products = load_products()

    cart_count = len(session.get('cart' , []))
    return render_template('index.html', products=products, cart_count=cart_count)


# route for product
@app.route('/product/<int:id>')
def product_details(id):
    products = load_products()

    product = None
    for p in products:
        if p['id'] == id:
            product = p
            break

    if product is None:
        return "product is not found"
    
    cart_count =len(session.get('cart',[]))
    return render_template('product.html', product=product, cart_count=cart_count)

# route for add-to-cart
@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):
    products = load_products()

    product = next((p for p in products if p['id'] == id), None)

    if product:
        if 'cart' not in session: 
            session['cart'] =[]

        cart = session['cart'] 


        found = False
        for item in cart:
            if item['id']==id:
                item['quantity'] +=1
                found=True
                break

        if  not found:
            cart.append(
                {
                    'id': product['id'],
                    'name':product['name'],
                    'price':product['price'],
                    'image':product['image'],
                    "quantity":1
                }
            )
        session['cart']= cart
        session.modified=True
    
        
    return redirect(url_for('home'))  

# cart page route
@app.route('/cart')
def cart():
    cart_items =session.get('cart',[])
    cart_count = len(cart_items)

    total=0
    for item in cart_items:
        total += item['price'] * item['quantity']
    return render_template('cart.html' , cart=cart_items, cart_count=cart_count , total=total)

# Remove item in cart 
@app.route('/remove/<int:id>')
def remove_item(id):
    cart = session.get('cart',[])

    cart = [item for item in cart if item['id'] != id ]

    session['cart'] = cart
    session.modified = True

    return redirect(url_for('cart'))

@app.route('/clear')
def clear_item():
    session.pop('cart',None)

    return redirect(url_for('cart'))


@app.route('/checkout')
def checkout():
    cart_items = session.get('cart',[])

    total =0
    for items in cart_items:
        total += items['price'] * items['quantity']

    return render_template('checkout.html' , cart=cart_items, total=total)


@app.route('/place_order', methods=['post'])
def place_order():
    session.pop('cart', None)

    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True) 