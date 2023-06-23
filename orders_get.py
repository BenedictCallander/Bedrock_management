import os
from datetime import datetime, timedelta
from woocommerce import API

# WooCommerce API credentials
url = "https://bedrock-computers.co.uk/"
consumer_key = "ck_e63f2847761567231436732f8c753e392fd81614"
consumer_secret = "cs_d40131313ebeeb4e1bd8b8fb67e41afd487685cf"

# Create the directory for storing order files
output_dir = 'orders/archive'
received_dir='orders/pending'
os.makedirs(output_dir, exist_ok=True)

def process_orders():
    # Calculate the date and time 24 hours ago
    start_date = datetime.now() - timedelta(hours=24)

    # Format the start date as required by the WooCommerce API
    start_date_formatted = start_date.strftime('%Y-%m-%dT%H:%M:%S')

    # Initialize the API object
    wcapi = API(url=url, consumer_key=consumer_key, consumer_secret=consumer_secret, version="wc/v3")

    # Prepare the query parameters
    params = {
        'after': start_date_formatted,
        'status': 'processing'
    }

    # Send the GET request to the WooCommerce API to retrieve orders
    orders = wcapi.get("orders", params=params).json()

    # Process each order
    for order in orders:
        order_id = order['id']
        output_file = os.path.join(output_dir, f"{order_id}.txt")
        output_file_received = os.path.join(received_dir, f"{order_id}.txt")

        # Skip if the order file already exists
        if os.path.exists(output_file):
            continue

        line_items = order['line_items']
        order_details = []

        for item in line_items:
            product_name = item['name']
            additions = item.get('meta_data', [])

            # Filter out metadata starting with '_'
            filtered_additions = [a for a in additions if not a['key'].startswith('_')]

            addition_text = ''.join([f"{a['key']}: {a['value']}\n" for a in filtered_additions])

            # Format the order details
            order_details.append(f"Product Name: {product_name}")
            order_details.append(f"Additions: {addition_text}")
            order_details.append("")

        # Write the order details to the file
        with open(output_file, 'w') as file:
            file.write('\n'.join(order_details))
        with open(output_file_received, 'w') as file:
            file.write('\n'.join(order_details))

# Process the orders
process_orders()