function selectProduct(product) {
    fetch('/compare', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `choice=${product}`
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        if (data.completed) {
            alert(`Experiment completed! Final payoff: ${data.payoff}`);
            window.location.reload();
        } else if (data.newRound) {
            document.getElementById('payoff-info').innerText = `Payoff for last round: ${data.payoff}`;
            document.getElementById('payoff-info').style.display = 'block';
            updateProductComparison(data);
        } else {
            updateProductComparison(data);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please refresh the page and try again.');
    });
}

function updateProductComparison(data) {
    // Update round number, category, and comparison
    document.getElementById('round-number').innerText = data.round;
    document.getElementById('category').innerText = data.category;
    document.getElementById('context-info').innerText = data.context;
    document.getElementById('comparison-number').innerText = data.comparison;

    // Update product A
    document.getElementById('product-a-name').innerText = data.product_a.name;
    document.getElementById('product-a-description').innerText = data.product_a.description;
    document.getElementById('product-a-price').innerText = data.product_a.price.toLocaleString();

    // Update product B
    document.getElementById('product-b-name').innerText = data.product_b.name;
    document.getElementById('product-b-description').innerText = data.product_b.description;
    document.getElementById('product-b-price').innerText = data.product_b.price.toLocaleString();
}

// Add this function to handle initial page load
function initializePage() {
    const productA = {
        name: document.getElementById('product-a-name').innerText,
        description: document.getElementById('product-a-description').innerText,
        price: parseInt(document.getElementById('product-a-price').innerText.replace(/,/g, ''))
    };
    const productB = {
        name: document.getElementById('product-b-name').innerText,
        description: document.getElementById('product-b-description').innerText,
        price: parseInt(document.getElementById('product-b-price').innerText.replace(/,/g, ''))
    };
    const category = document.getElementById('category').innerText;
    const context = document.getElementById('context-info').innerText;
    const round = parseInt(document.getElementById('round-number').innerText);
    const comparison = parseInt(document.getElementById('comparison-number').innerText);

    updateProductComparison({
        product_a: productA,
        product_b: productB,
        category: category,
        context: context,
        round: round,
        comparison: comparison
    });
}

// Call initializePage when the page loads
window.onload = initializePage;