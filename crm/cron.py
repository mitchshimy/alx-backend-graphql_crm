from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime

def log_crm_heartbeat():
    # Set up GraphQL client
    transport = RequestsHTTPTransport(url='http://localhost:8000/graphql')
    client = Client(transport=transport, fetch_schema_from_transport=True)
    
    # Query the hello field
    query = gql("""
        query {
            hello
        }
    """)
    
    try:
        response = client.execute(query)
        status = "OK" if response.get('hello') == "Hello, GraphQL!" else "ERROR"
    except Exception as e:
        status = f"ERROR: {str(e)}"
    
    # Log heartbeat with timestamp
    with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
        f.write(f"{datetime.now().strftime('%d/%m/%Y-%H:%M:%S')} CRM is alive - Status: {status}\n")


def update_low_stock():
    transport = RequestsHTTPTransport(url='http://localhost:8000/graphql')
    client = Client(transport=transport, fetch_schema_from_transport=True)
    mutation = gql("""
        mutation {
            updateLowStockProducts {
                products {
                    name
                    stock
                }
                message
            }
        }
    """)
    try:
        response = client.execute(mutation)
        products = response.get('updateLowStockProducts', {}).get('products', [])
        message = response.get('updateLowStockProducts', {}).get('message', 'No products updated')
        with open('/tmp/low_stock_updates_log.txt', 'a') as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
            for product in products:
                f.write(f"  Product: {product['name']}, New Stock: {product['stock']}\n")
    except Exception as e:
        with open('/tmp/low_stock_updates_log.txt', 'a') as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Error: {str(e)}\n")
