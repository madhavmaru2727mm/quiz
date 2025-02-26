document.addEventListener("DOMContentLoaded", function () {
    let productInput = document.getElementById("product-name");
    let quantityInput = document.getElementById("quantity");
    let productList = document.getElementById("product-list");
    let invoiceList = document.getElementById("invoice-list");
    let addProductBtn = document.getElementById("add-product");
    let printInvoiceBtn = document.getElementById("print-invoice");
    let saveProductBtn = document.getElementById("save-product");
    let newProductName = document.getElementById("new-product-name");
    let newProductPrice = document.getElementById("new-product-price");
    let productMessage = document.getElementById("product-message");

    // Load products in dropdown
    function loadProducts() {
        fetch("/search?q=")
            .then(response => response.json())
            .then(data => {
                productList.innerHTML = "";
                Object.keys(data).forEach(product => {
                    let option = document.createElement("option");
                    option.value = product;
                    productList.appendChild(option);
                });
            });
    }

    loadProducts();

    // Handle product selection and move to quantity input
    productInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            quantityInput.focus();
        }
    });

    // Handle quantity input and move back to product name
    quantityInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            addProductBtn.click();
        } else if (event.key === "ArrowLeft") {
            event.preventDefault();
            productInput.focus();
        }
    });

    // Add product to invoice
    addProductBtn.addEventListener("click", function () {
        let product = productInput.value.trim();
        let quantity = parseInt(quantityInput.value);

        if (!product || isNaN(quantity) || quantity <= 0) {
            alert("Please enter a valid product and quantity.");
            return;
        }

        fetch(`/search?q=${product}`)
            .then(response => response.json())
            .then(data => {
                if (data[product]) {
                    let price = data[product];
                    let total = price * quantity;
                    let item = document.createElement("li");
                    item.textContent = `${product} - ${quantity} x ₹${price} = ₹${total}`;
                    invoiceList.appendChild(item);

                    // Clear fields
                    productInput.value = "";
                    quantityInput.value = "";
                    productInput.focus();
                } else {
                    alert("Product not found.");
                }
            });
    });

    // Save new product
    saveProductBtn.addEventListener("click", function () {
        let name = newProductName.value.trim();
        let price = parseInt(newProductPrice.value);

        if (!name || isNaN(price) || price <= 0) {
            alert("Enter valid product details.");
            return;
        }

        fetch("/add_product", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, price })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                productMessage.textContent = "Product added";
                productMessage.style.color = "green";
                loadProducts();  // Refresh product list
                newProductName.value = "";
                newProductPrice.value = "";
            } else {
                productMessage.textContent = "Failed to add product";
                productMessage.style.color = "red";
            }
        });
    });

    // Print invoice
    printInvoiceBtn.addEventListener("click", function () {
        let invoiceContent = document.querySelector(".invoice").innerHTML;
        let newWindow = window.open("", "", "width=600,height=400");
        newWindow.document.write(`<h1>ABC Store</h1>`);
        newWindow.document.write(invoiceContent);
        newWindow.document.close();
        newWindow.print();
    });
});
