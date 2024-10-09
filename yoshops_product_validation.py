import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import re

def fetch_page_content(url):
    try:
        # Use urllib to open the URL
        with urllib.request.urlopen(url) as response:
            return response.read()
    except Exception as e:
        print(f"Error fetching the page: {e}")
        return None

def extract_product_data(soup):
    product_data = []
    
    # Loop through all the products found on the page
    for product in soup.find_all('div', class_='product'):
        try:
            # Get product URL
            product_url = product.find('a')['href']
            
            # Get product name
            product_name = product.find('h2', class_='product-title').get_text(strip=True)
            
            # Get product details
            product_details = product.find('div', class_='product-description').get_text(strip=True)
            
            # Check if the product image is missing
            image = product.find('img')
            if image is None or 'no-image' in image['src']:
                image_status = 'Image missing'
            else:
                image_status = 'Image present'
                
            # Add product data to list
            product_data.append({
                'URL': product_url,
                'Product Name': product_name,
                'Product Details': product_details,
                'Image Status': image_status,
                'Contact No': 'Not Available',  # Placeholder (could scrape from other part of page if available)
                'Address': 'Not Available'      # Placeholder (could scrape from other part of page if available)
            })
        except Exception as e:
            print(f"Error extracting product data: {e}")
    
    return product_data

def save_to_excel(product_data, filename='products_data.xlsx'):
    # Convert product data to a pandas DataFrame
    df = pd.DataFrame(product_data)
    
    # Save to Excel
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}")

def main():
    # Ask the user for input
    choice = input("Enter 1 for 'Yoshops.com' or 2 to input main categories/subcategories URL: ")

    if choice == '1':
        url = 'https://yoshops.com'
    elif choice == '2':
        url = input("Please enter the main categories/subcategories URL: ")
    else:
        print("Invalid choice.")
        return
    
    # Fetch page content
    page_content = fetch_page_content(url)
    if page_content is None:
        return
    
    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(page_content, 'html.parser')
    
    # Extract product data
    product_data = extract_product_data(soup)
    
    if product_data:
        # Save the product data to an Excel file
        save_to_excel(product_data)
    else:
        print("No product data found.")

if __name__ == "__main__":
    main()