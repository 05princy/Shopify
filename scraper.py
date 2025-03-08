# #SCRAPING ITEM DETAILS FROM THE STORE AND NUMBER OF PAGES MENTIONED BY THE USER 
import requests
from bs4 import BeautifulSoup
import streamlit as st

# Function to scrape products from a given store and page
def scrape_products(store_name, item_type, num_pages):
    all_products = []

    # Iterate over the specified number of pages
    for page in range(1, num_pages + 1):
        url = f"https://dealsheaven.in/store/{store_name}?page={page}"
        response = requests.get(url)
        
        if response.status_code != 200:
            st.write(f"Failed to fetch page {page} for {store_name}. Status code: {response.status_code}")
            continue
        
        soup = BeautifulSoup(response.content, 'html.parser')
        product_list = soup.find_all('div', class_='product-item-detail')

        # Filter products based on the item type
        for product in product_list:
            title = product.find('h3').text.strip() if product.find('h3') else "No Title"
            if item_type.lower() in title.lower():
                price = product.find('p', class_='price').text.strip() if product.find('p', class_='price') else "No Price"
                special_price = product.find('p', class_='spacail-price').text.strip() if product.find('p', class_='spacail-price') else "No Special Price"
                link = product.find('a', previewlistener="true")['href'] if product.find('a', previewlistener="true") else "No Link"
                image = product.find('img')['src'] if product.find('img') else "No Image"
                
                # Append the product details to the all_products list
                all_products.append({
                    'Title': title,
                    'Price': price,
                    'Special Price': special_price,
                    'Link': link,
                    'Image': image
                })
    
    return all_products

# Streamlit UI
st.title("Deals Heaven Scraper")

# Input for store name
store_name = st.text_input("Enter the store name (e.g., 'flipkart', 'amazon'):")

# Input for item type
item_type = st.text_input("Enter the type of item you want (e.g., 'shirt'): ")

# Input for number of pages
num_pages = st.number_input("Enter the number of pages to scrape:", min_value=1, value=1)

# Button to scrape products
if st.button("Scrape Products"):
    if store_name and item_type:
        products = scrape_products(store_name, item_type, num_pages)
        if products:
            # Displaying the results in the UI
            for product in products:
                st.image(product['Image'], caption=product['Title'])
                st.write(f"*Title:* {product['Title']}")
                st.write(f"*Price:* {product['Price']}")
                st.write(f"*Special Price:* {product['Special Price']}")
                st.write(f"[View Deal]({product['Link']})")
                st.write("---")
        else:
            st.write("No products found matching your criteria.")
    else:
        st.write("Please enter both the store name and item type.")