from flask import Flask, render_template, request, jsonify, session
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

categories = ["peralatan rumah tangga", "kendaraan", "sumber listrik rumah"]

products = {
    "peralatan rumah tangga": {
        "A": {"name": "Kompor Listrik A", "price": 2000000, "description": "Kompor listrik hemat energi"},
        "B": {"name": "Kompor Listrik B", "price": 1800000, "description": "Kompor listrik ramah lingkungan"},
        "C1": {"name": "Kompor Gas C1", "price": 1000000, "description": "Kompor gas konvensional"},
        "C2": {"name": "Kompor Gas C2", "price": 1200000, "description": "Kompor gas konvensional premium"}
    },
    "kendaraan": {
        "A": {"name": "Mobil Listrik A", "price": 500000000, "description": "Mobil listrik jarak jauh"},
        "B": {"name": "Mobil Listrik B", "price": 450000000, "description": "Mobil listrik kota"},
        "C1": {"name": "Mobil Bensin C1", "price": 200000000, "description": "Mobil bensin ekonomis"},
        "C2": {"name": "Mobil Bensin C2", "price": 250000000, "description": "Mobil bensin performa tinggi"}
    },
    "sumber listrik rumah": {
        "A": {"name": "Panel Surya A", "price": 25000000, "description": "Panel surya kapasitas besar"},
        "B": {"name": "Panel Surya B", "price": 20000000, "description": "Panel surya efisiensi tinggi"},
        "C1": {"name": "Genset C1", "price": 10000000, "description": "Genset standar"},
        "C2": {"name": "Genset C2", "price": 12000000, "description": "Genset low noise"}
    }
}

contexts = [
    "Mengenai jumlah, dan kualitas infrastruktur",
    "Mengenai ketersediaan produk di pasar",
    "Mengenai jumlah pengguna produk tersebut"
]

@app.route('/')
def index():
    session.clear()
    session['round'] = 1
    session['comparison'] = 1
    session['category'] = random.choice(categories)
    session['context'] = random.choice(contexts)
    return render_template(
        'index.html', 
        product_a=products[session['category']]["A"],
        product_b=products[session['category']]["B"],
        category=session['category'],
        context=session['context'],
        round=session['round'],
        comparison=session['comparison']
        )

@app.route('/compare', methods=['POST'])
def compare():
    choice = request.form.get('choice')
    category = session.get('category')
    comparison = session.get('comparison', 1)
    current_round = session.get('round', 1)

    if comparison == 1:
        session['winner'] = choice
        next_product = "C1"
    elif comparison == 2:
        next_product = "C2"
    else:
        # Final choice made for this round
        payoff = calculate_payoff(products[category][choice])
        current_round += 1
        
        if current_round > 3:
            session.clear()
            return jsonify({"completed": True, "payoff": payoff})
        
        # Set up next round
        category = random.choice(categories)
        session['round'] = current_round
        session['comparison'] = 1
        session['category'] = category
        session['context'] = random.choice(contexts)
        
        return jsonify({
            "newRound": True,
            "payoff": payoff,
            "product_a": products[category]["A"],
            "product_b": products[category]["B"],
            "category": category,
            "context": session['context'],
            "round": current_round,
            "comparison": 1
        })

    session['comparison'] = comparison + 1
    return jsonify({
        "product_a": products[category][session['winner']],
        "product_b": products[category][next_product],
        "category": category,
        "context": session['context'],
        "round": current_round,
        "comparison": session['comparison']
    })

def calculate_payoff(product):
    category = session.get('category')
    if category == "peralatan rumah tangga":
        return product['price'] / 500
    elif category == "kendaraan":
        return product['price'] / 10000
    elif category == "sumber listrik rumah":
        return product['price'] / 500
    else:
        return 0  # Default case, should not happen

if __name__ == '__main__':
    app.run(debug=True)