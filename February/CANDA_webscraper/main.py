# Standard library imports
import os
import re
import time
import random
from datetime import datetime
from typing import Dict, List, Optional, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin

# Third-party imports
import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def create_directory(directory_path: str) -> None:
    """
    Ensure directory exists, creating it if necessary.

    Args:
        directory_path: Path of directory to create
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Created directory: {directory_path}")


# Pre-compile category keywords for faster lookup
CATEGORY_KEYWORDS = {
    'jeans': ['jeans', 'denim', 'baggy', 'skinny jeans', 'straight jeans', 'wide leg'],
    'shirts': ['shirt', 'bluse', 'blouse', 'top', 'hemd', 't-shirt', 'tshirt', 't shirt', 'tee', 'body'],
    'sweaters': ['pullover', 'sweater', 'sweatshirt', 'hoodie', 'cardigan', 'strickjacke'],
    'dresses': ['kleid', 'dress', 'robe'],
    'skirts': ['rock', 'skirt'],
    'pants': ['hose', 'pants', 'trousers', 'leggings', 'joggers'],
    'jackets': ['jacke', 'jacket', 'blazer', 'coat', 'mantel', 'blouson'],
    'underwear': ['unterwäsche', 'underwear', 'bra', 'slip', 'panty'],
    'accessories': ['schal', 'scarf', 'mütze', 'cap', 'hat', 'schmuck', 'jewelry', 'tasche', 'bag']
}

# Create a flat keyword to category mapping for O(1) lookups
KEYWORD_TO_CATEGORY = {}
for category, keywords in CATEGORY_KEYWORDS.items():
    for keyword in keywords:
        KEYWORD_TO_CATEGORY[keyword] = category


def categorize_product(combined_text: str) -> str:
    """
    Return product category based on text analysis.

    Args:
        combined_text: Combined product text to analyze

    Returns:
        String representing the product category
    """
    # Ensure text is lowercase for case-insensitive matching
    text = combined_text.lower()

    # First try direct keyword matching (fastest)
    for keyword, category in KEYWORD_TO_CATEGORY.items():
        if keyword in text:
            return category

    # Fallback to category-by-category search
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return category

    return 'other'


# Pre-compile product type keywords for faster matching
PRODUCT_TYPES = [
    'jeans', 't-shirt', 'tshirt', 'hoodie', 'sweater', 'dress', 'skirt',
    'leggings', 'blazer', 'blouse', 'top', 'cardigan', 'jacket', 'coat',
    'joggers', 'shorts', 'underwear', 'scarf', 'hat', 'bag'
]


def get_product_type(combined_text: str) -> str:
    """
    Extract specific product type from product info.

    Args:
        combined_text: Combined product text to analyze

    Returns:
        String representing the product type
    """
    text = combined_text.lower()

    for product_type in PRODUCT_TYPES:
        if product_type in text:
            return product_type

    # If no specific type found, use the category
    for category in ['jeans', 'shirt', 'sweater', 'dress', 'skirt', 'pant', 'jacket', 'underwear', 'accessory']:
        if category in text or f"{category}s" in text:
            return category

    return 'other'


# Create a session with retry mechanism
def get_session() -> requests.Session:
    """
    Create a requests session with retry mechanism.

    Returns:
        Configured requests session
    """
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
    })
    return session


def extract_product_data(product: BeautifulSoup, url: str) -> Optional[Dict[str, Any]]:
    """
    Extract data from a product container element.

    Args:
        product: BeautifulSoup object representing the product container
        url: URL of the product page

    Returns:
        Dictionary containing extracted product data, or None if extraction fails
    """
    try:
        # Try different selectors for title
        title_elem = product.select_one('.sc-KXCwU.dAUKCu.sc-PgYfk.kLcJAn') or \
            product.select_one('h3') or \
            product.select_one('.product-title')

        # Try different selectors for price
        price_elem = product.select_one('.sc-KXCwU.eraGkl.sc-hvwqhb.ekSxsH') or \
            product.select_one('.price') or \
            product.select_one('[data-testid="price"]')

        # Get image and link elements
        image_elem = product.select_one('img')
        link_elem = product.select_one('a')

        # Extract data
        title = title_elem.text.strip() if title_elem else "Title not found"

        price = "Price not found"
        if price_elem:
            price = price_elem.text.strip().replace('€', '').strip()

        image_url = ""
        if image_elem:
            image_url = image_elem.get(
                'src') or image_elem.get('data-src') or ""
            if not image_url and image_elem.get('srcset'):
                image_url = image_elem.get('srcset').split(',')[
                    0].strip().split(' ')[0]

        product_url = ""
        if link_elem and link_elem.get('href'):
            product_url = link_elem.get('href')
            if not product_url.startswith('http'):
                product_url = urljoin(url, product_url)

        product_id = ""
        product_name = ""
        if product_url:
            # Try the existing regex first:
            id_match = re.search(r'product-(\d+)', product_url)
            if id_match:
                product_id = id_match.group(1)
            else:
                # Fallback for digits after the last dash:
                fallback_match = re.search(r'-([0-9]+)(?:[/?]|$)', product_url)
                if fallback_match:
                    product_id = fallback_match.group(1)

            # Extract product name from URL
            name_match = re.search(r'/([^/]+)-\d+/$', product_url)
            if name_match:
                product_name = name_match.group(1).replace('-', ' ')

        # Combine text for categorization (do this once to avoid redundant operations)
        combined_text = f"{title.lower()} {product_url.lower()} {product_name.lower()}"

        category = categorize_product(combined_text)
        product_type = get_product_type(combined_text)

        return {
            'product_id': product_id,
            'title': title,
            'price': price,
            'category': category,
            'type': product_type,
            'image_url': image_url,
            'product_url': product_url,
            'scrape_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        print(f"Error extracting product data: {e}")
        return None


def scrape_page(url: str, session: requests.Session) -> List[Dict[str, Any]]:
    """
    Scrape product data from a single page using the provided session.

    Args:
        url: URL of the page to scrape
        session: Requests session to use for scraping

    Returns:
        List of dictionaries containing product data
    """
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Look for product containers with various selectors
        selectors = [
            '.sc-lgIphe.eUXsHr',
            '.sc-eaUbBy.eXzvqR.sc-eYcCYJ.ivCUrY',
            '.product-item',
            '[data-testid="product-tile"]'
        ]

        product_containers = []
        for selector in selectors:
            containers = soup.select(selector)
            if containers:
                product_containers = containers
                break

        products = []
        for product in product_containers:
            product_data = extract_product_data(product, url)
            if product_data:
                products.append(product_data)

        return products

    except requests.exceptions.RequestException as e:
        return []
    except Exception as e:
        return []


def update_csv_file(new_products: List[Dict[str, Any]], file_path: str) -> List[Dict[str, Any]]:
    """
    Update or create a CSV file with new/updated product information.

    Args:
        new_products: List of new product data to update
        file_path: Path to the CSV file to update

    Returns:
        List of merged product data
    """
    existing_products = {}

    # Read existing data if file exists
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            for _, row in df.iterrows():
                pid = str(row.get('product_id', ''))
                if pid and pid != 'nan':
                    existing_products[pid] = row.to_dict()
            print(
                f"Read {len(existing_products)} existing records from {file_path}")
        except Exception as e:
            print(f"Error reading existing CSV file: {e}")

    new_count = 0
    updated_count = 0
    merged_data = []

    # Process new products
    for new_product in new_products:
        pid = str(new_product.get('product_id', ''))
        if not pid:
            merged_data.append(new_product)
            new_count += 1
            continue

        if pid in existing_products:
            existing_product = existing_products[pid]
            if new_product['price'] != existing_product['price']:
                existing_product['price'] = new_product['price']
                existing_product['scrape_date'] = new_product['scrape_date']
                updated_count += 1
            merged_data.append(existing_product)
            del existing_products[pid]
        else:
            merged_data.append(new_product)
            new_count += 1

    # Add remaining existing products
    merged_data.extend(existing_products.values())

    # Write to file
    try:
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        df = pd.DataFrame(merged_data)
        df.to_csv(file_path, index=False)

        print(f"Successfully updated {file_path}")
        print(f"- Added {new_count} new products")
        print(f"- Updated prices for {updated_count} existing products")
        print(f"- Total products in file: {len(merged_data)}")

        return merged_data
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return merged_data


def get_valid_links(base_url: str, session: requests.Session, max_links: int = 20) -> List[str]:
    """
    Find valid product listing pages efficiently.

    Args:
        base_url: Base URL of the website to start from
        session: Requests session to use for scraping
        max_links: Maximum number of links to check

    Returns:
        List of valid product listing page URLs
    """
    print(f"Visiting C&A homepage: {base_url}")
    valid_links = set()
    visited_links = set()

    try:
        # Get homepage
        response = session.get(base_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract potential shop links
        all_links = [link['href'] for link in soup.find_all('a', href=True)
                     if link['href'] and not link['href'].startswith('#')]

        # Process relative URLs and filter to shop links
        links_to_check = []
        for link in all_links:
            full_url = urljoin(base_url, link)
            if '/shop/' in full_url and base_url in full_url:
                links_to_check.append(full_url)

        links_to_check = list(set(links_to_check))  # Remove duplicates
        print(f"Found {len(links_to_check)} unique shop links to check")

        # Check links concurrently
        def check_link(url: str) -> Optional[str]:
            if url in visited_links:
                return None

            visited_links.add(url)
            try:
                response = session.get(url, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                # Check for product containers
                selectors = [
                    '.sc-eaUbBy.eXzvqR.sc-eYcCYJ.ivCUrY',
                    '.sc-lgIphe.eUXsHr',
                    '.product-item',
                    '[data-testid="product-tile"]'
                ]

                for selector in selectors:
                    elements = soup.select(selector)
                    if elements:
                        print(
                            f"Found valid shop page: {url} with {len(elements)} products")
                        return url

                return None
            except Exception as e:
                print(f"Error checking {url}: {e}")
                return None

        # Use ThreadPoolExecutor for concurrent checking
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(
                check_link, url): url for url in links_to_check[:max_links]}
            for future in as_completed(future_to_url):
                result = future.result()
                if result:
                    valid_links.add(result)

        return list(valid_links)

    except Exception as e:
        print(f"Error accessing the C&A homepage: {e}")
        return list(valid_links)


def save_products_by_category(all_products: List[Dict[str, Any]], output_dir: str) -> None:
    """
    Save products organized by category and type.

    Args:
        all_products: List of all product data
        output_dir: Directory to save the categorized product files
    """
    if not all_products:
        print("No products to save by category/type.")
        return

    # Group products by category and type
    by_category = {}
    by_type = {}

    for product in all_products:
        category = product['category']
        product_type = product['type']

        by_category.setdefault(category, []).append(product)
        by_type.setdefault(product_type, []).append(product)

    # Save category files
    categories_dir = os.path.join(output_dir, "categories")
    create_directory(categories_dir)

    for category, products in by_category.items():
        if category in ['jeans', 'shirts', 'sweaters', 'dresses', 'skirts', 'pants', 'jackets', 'underwear', 'accessories']:
            file_path = os.path.join(categories_dir, f"{category}.csv")
            df = pd.DataFrame(products)
            df.to_csv(file_path, index=False)
            print(f"Saved {len(products)} products to {file_path}")

    # Removed code that writes CSV files for product types


def main() -> None:
    """
    Main function to run the optimized C&A web scraper.
    """
    output_dir = "February/CANDA_webscraper/listings"
    create_directory(output_dir)
    print("Starting optimized C&A web scraper...")

    # Track overall execution time
    start_time = time.time()

    try:
        # Create a session for all requests
        session = get_session()

        # Find valid product pages
        base_url = "https://www.c-and-a.com/de/de"
        valid_links = get_valid_links(base_url, session)

        if not valid_links:
            print("No valid links found to scrape.")
            return

        # Save found links
        links_file = os.path.join(output_dir, "scraped_links.txt")
        with open(links_file, 'w', encoding='utf-8') as f:
            for link in valid_links:
                f.write(f"{link}\n")

        print(f"Found {len(valid_links)} valid pages to scrape.")

        # Scrape pages concurrently
        all_products = []
        debug_products = []

        def scrape_with_delay(link: str) -> List[Dict[str, Any]]:
            # Add a small random delay to avoid being blocked
            time.sleep(random.uniform(0.5, 2))
            return scrape_page(link, session)

        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_url = {executor.submit(
                scrape_with_delay, url): url for url in valid_links}
            pbar = tqdm(total=len(valid_links), desc="Scraping pages")

            for future in as_completed(future_to_url):
                pbar.update(1)
                url = future_to_url[future]
                try:
                    products = future.result()
                    if products:
                        for product in products:
                            if product.get('product_id'):
                                all_products.extend(products)
                            else:
                                debug_products.append(product)
                except Exception:
                    pass

            pbar.close()

        if all_products:
            # Deduplicate in-memory before saving
            unique_map = {}
            for pr in all_products:
                pid = pr.get('product_id')
                if pid:
                    unique_map[pid] = pr  # overwrite if exists => latest data
            final_products = list(unique_map.values())

            main_file = os.path.join(output_dir, "all_products.csv")
            df = pd.DataFrame(final_products)
            df.to_csv(main_file, index=False)
            print(f"Saved {len(final_products)} total products to {main_file}")

            save_products_by_category(final_products, output_dir)
        else:
            print("No products were scraped from any valid links.")

        if debug_products:
            debug_file = os.path.join(output_dir, "debug_products.csv")
            df = pd.DataFrame(debug_products)
            df.to_csv(debug_file, index=False)
            print(
                f"Saved {len(debug_products)} products without IDs to {debug_file}")

    except KeyboardInterrupt:
        print("\nScraping interrupted by user. Partial data may have been saved.")
    except Exception as e:
        print(f"\nAn error occurred during scraping: {e}")

    finally:
        # Calculate and display execution time
        end_time = time.time()
        duration = end_time - start_time
        hours, remainder = divmod(duration, 3600)
        minutes, seconds = divmod(remainder, 60)

        print(
            f"\nTotal execution time: {int(hours)}h {int(minutes)}m {int(seconds)}s")


if __name__ == "__main__":
    main()
