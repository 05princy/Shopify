import streamlit as st
import requests
from bs4 import BeautifulSoup

# Step 1: Fetch all stores from the Deals Heaven website
store_url = "https://dealsheaven.in/stores"
response = requests.get(store_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract store names and URLs
store_nav = soup.find('ul', class_='navbar-nav')
store_links = store_nav.find_all('a', href=True)

stores = {}
for store in store_links:
    store_name = store.text.strip()
    store_url = store['href']
    if "store" in store_url:  # Ensure it's a store link
        stores[store_name] = store_url

# Streamlit UI - Premium Soft Design
st.set_page_config(page_title="🛍️ Shopify", page_icon="🛒", layout="wide")

# Custom CSS for a soft, elegant UI
st.markdown("""
    <style>
        body {
            background-color: #f8f9fa;
            color: #333;
            font-family: 'Arial', sans-serif;
        }
        .header {
            font-size: 28px;
            font-weight: bold;
            text-align: center;
            padding: 10px;
            background: linear-gradient(90deg, #6a11cb, #2575fc);
            -webkit-background-clip: text;
            color: transparent;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
            transition: 0.3s ease-in-out;
        }
        .header:hover {
            transform: scale(1.05);
        }
        .subheader {
            font-size: 18px;
            text-align: center;
            color: #666;
            margin-bottom: 20px;
        }
        .product-grid {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
        }
        .product-card {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 15px;
            margin: 15px;
            width: 300px;
            text-align: center;
            box-shadow: 4px 4px 12px rgba(0, 0, 0, 0.1);
        }
        .product-title {
            font-size: 16px;
            font-weight: bold;
            color: #444;
            margin-bottom: 6px;
        }
        .price {
            font-size: 16px;
            font-weight: bold;
            color: #5c636a;
            margin-bottom: 5px;
        }
        .discount {
            font-size: 14px;
            color: #4CAF50;
        }
        .special-price {
            font-size: 14px;
            color: #FF9800;
        }
        .button {
            display: inline-block;
            padding: 8px 12px;
            margin-top: 8px;
            font-size: 14px;
            font-weight: bold;
            color: #fff;
            background: #6c757d;
            border-radius: 6px;
            text-decoration: none;
            transition: 0.3s ease-in-out;
        }
        .button:hover {
            background: #5a6268;
            transform: scale(1.03);
        }
    </style>
""", unsafe_allow_html=True)

# Step 2: Streamlit user input to select the store
st.markdown("<div class='header'>🛒 Shopify</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>Compare the best deals across multiple online stores in a refined way.</div>", unsafe_allow_html=True)

store_choice = st.selectbox("Choose a store:", list(stores.keys()))

if store_choice:
    store_url = stores[store_choice]
    st.markdown(f"<h3 style='color: #6c757d;'>📢 Fetching deals from: {store_choice}</h3>", unsafe_allow_html=True)

    # Step 3: Scrape products for the selected store
    response = requests.get(store_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_items = soup.find_all('div', class_='product-item-detail')

    if not product_items:
        st.markdown(f"<p style='color: #dc3545;'>❌ No products found for {store_choice}. Try another store.</p>", unsafe_allow_html=True)
    else:
        st.markdown("<h3 style='color: #444;'>🛒 Latest Deals:</h3>", unsafe_allow_html=True)
        
        # Start product grid
        st.markdown("<div class='product-grid'>", unsafe_allow_html=True)

        # Display product details in an elegant UI
        for product in product_items:
            title = product.find('h3').text.strip() if product.find('h3') else "No Title"
            price = product.find('p', class_='price').text.strip() if product.find('p', class_='price') else "No Price"
            special_price = product.find('p', class_='spacail-price').text.strip() if product.find('p', class_='spacail-price') else "N/A"
            discount = product.find('div', class_='discount').text.strip() if product.find('div', class_='discount') else "No Discount"
            product_link = product.find('a')['href'] if product.find('a') else "#"

            # Display product in a modern, luxury card format
            st.markdown(f"""
                <div class='product-card'>
                    <p class='product-title'>🛍️ {title}</p>
                    <p class='price'>💰 Price: {price}</p>
                    <p class='special-price'>🔥 Special Price: {special_price}</p>
                    <p class='discount'>🎉 Discount: {discount}</p>
                    <a href="{product_link}" class='button' target="_blank">🔗 View Product</a>
                </div>
            """, unsafe_allow_html=True)

        # End product grid
        st.markdown("</div>", unsafe_allow_html=True)
