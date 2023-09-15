from flask import Flask, jsonify, request
import requests
app = Flask(__name__)


# Sample Cart data
carts = {}

# Cart Services Endpoints

# Endpoint 1: Get current content of a user's cart
@app.route('/cart/<int:user_id>', methods = ['GET'])
def show_cart(user_id):
  if user_id in carts:
    return jsonify(carts[user_id])
  else:
    return jsonify({"message": "Cart not found"}), 404


# Function to get product by product_id
def get_product(product_id):
  ProductService_url = 'http://127.0.0.1:5001/' #local machine url
  # ProductService_url = 
  response = requests.get(f'{ProductService_url}/products/{product_id}')
  if response.status_code == 200:
      product = response.json()
      return product
  else:
      return None

# Endpoint 2: Add product to cart
@app.route('/cart/<int:user_id>/add/<int:product_id>', methods = ['POST'])
def add_to_cart(user_id, product_id):
  product = get_product(product_id)
  if not product:
    return jsonify({"error": "Product not found"}), 404
  
  quantity_to_add = request.json.get('quantity', 1)

  # Already have a cart structure where products are stored with quantities
  if user_id in carts:
    # Product is already there just increase the quantity
    if product_id in carts[user_id]:
      carts[user_id][product_id]["quantity"] += quantity_to_add
    # Product is new so add the info to the cart and amount of quantity
    else:
      carts[user_id][product_id] = {
        "product": product,
        "quantity": quantity_to_add
      }
  else:
    # Create a new cart for the user
    carts[user_id] = {
      product_id: {
        "product": product,
        "quantity": quantity_to_add
      }
    }
  return jsonify({"message": "Product added to cart", "Product": product, "Quantity": quantity_to_add}), 201



# Endpoint 3: Delete a product from cart
@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods = ['POST'])
def delete_from_cart(user_id, product_id):
  if user_id in carts and product_id in carts[user_id]:
    quantity_to_remove = request.json.get('quantity', 1)

    if quantity_to_remove <= 0:
      return jsonify({"error": "Invalid quantity"}), 400
    
    # delete the entire product if quantity is over or remove some if not 
    if carts[user_id][product_id]["quantity"] <= quantity_to_remove:
      del carts[user_id][product_id]
    else:
      carts[user_id][product_id]["quantity"] -= quantity_to_remove
    return jsonify({"message": f"Removed {quantity_to_remove} from cart", "Product": product_id}), 200
  
  else:
    return jsonify({"error": "Product not found in the cart"}), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002) # might need to change in render 
    