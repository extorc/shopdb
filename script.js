// Sample Data for Products and Orders
let products = [
    { name: "Laptop", category: "Electronics", stock: 10, price: 50000 },
    { name: "Smartphone", category: "Electronics", stock: 20, price: 30000 }
];

let orders = [
    { id: "#1001", customer: "Rahul Sharma", amount: 75000, status: "Completed" },
    { id: "#1002", customer: "Neha Verma", amount: 50000, status: "Processing" }
];

// Function to Update Dashboard Stats
function updateDashboard() {
    document.getElementById("total-sales").innerText = `₹${orders.reduce((sum, order) => sum + order.amount, 0)}`;
    document.getElementById("total-orders").innerText = `${orders.length} Orders`;
    document.getElementById("total-products").innerText = `${products.length} Products in Stock`;
}

// Load Products Table
function loadProducts() {
    let table = document.getElementById("productTable");
    table.innerHTML = `
        <tr>
            <th>Product</th>
            <th>Category</th>
            <th>Stock</th>
            <th>Price</th>
            <th>Actions</th>
        </tr>
    `;

    products.forEach((product, index) => {
        let row = table.insertRow();
        row.innerHTML = `
            <td>${product.name}</td>
            <td>${product.category}</td>
            <td>${product.stock}</td>
            <td>₹${product.price}</td>
            <td>
                <button onclick="editProduct(${index})">Edit</button>
                <button onclick="deleteProduct(${index})">Delete</button>
            </td>
        `;
    });

    updateDashboard();
}

// Add New Product
document.getElementById("addProductBtn")?.addEventListener("click", function() {
    let name = prompt("Enter Product Name:");
    let category = prompt("Enter Category:");
    let stock = parseInt(prompt("Enter Stock Quantity:"), 10);
    let price = parseFloat(prompt("Enter Price (₹):"));

    if (name && category && stock > 0 && price > 0) {
        products.push({ name, category, stock, price });
        loadProducts();
    } else {
        alert("Invalid input. Please try again.");
    }
});

// Edit Product Stock
function editProduct(index) {
    let newStock = parseInt(prompt("Enter new stock quantity:"), 10);
    if (!isNaN(newStock) && newStock > 0) {
        products[index].stock = newStock;
        loadProducts();
    } else {
        alert("Invalid input.");
    }
}

// Delete Product
function deleteProduct(index) {
    if (confirm("Are you sure you want to delete this product?")) {
        products.splice(index, 1);
        loadProducts();
    }
}

// Load Orders Table
function loadOrders() {
    let table = document.getElementById("orderTable");
    table.innerHTML = `
        <tr>
            <th>Order ID</th>
            <th>Customer</th>
            <th>Amount</th>
            <th>Status</th>
        </tr>
    `;

    orders.forEach(order => {
        let row = table.insertRow();
        row.innerHTML = `
            <td>${order.id}</td>
            <td>${order.customer}</td>
            <td>₹${order.amount}</td>
            <td>${order.status}</td>
        `;
    });

    updateDashboard();
}

// Place a New Order
document.getElementById("placeOrderBtn")?.addEventListener("click", function() {
    let customer = prompt("Enter Customer Name:");
    let amount = parseFloat(prompt("Enter Order Amount (₹):"));

    if (customer && amount > 0) {
        let newOrderId = `#10${orders.length + 3}`;
        orders.push({ id: newOrderId, customer, amount, status: "Pending" });
        loadOrders();
    } else {
        alert("Invalid input. Please try again.");
    }
});

// Load Pages
window.onload = function() {
    if (document.getElementById("total-sales")) updateDashboard();
    if (document.getElementById("productTable")) loadProducts();
    if (document.getElementById("orderTable")) loadOrders();
};
