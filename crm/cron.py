from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    """
    Logs a heartbeat message to confirm CRM is alive and optionally verifies GraphQL 'hello' query.
    """
    now = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    status = "CRM is alive"

    try:
        # GraphQL client setup
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=False,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=False)

        # Perform test query
        query = gql("""query { hello }""")
        result = client.execute(query)

        if result.get("hello") != "Hello world!":
            status = "CRM is alive (but GraphQL check failed)"
    except Exception:
        status = "CRM is alive (GraphQL unreachable)"

    # Append to heartbeat log
    with open('/tmp/crm_heartbeat_log.txt', 'a') as log_file:
        log_file.write(f"{now} {status}\n")


def update_low_stock():
    """
    Calls GraphQL mutation to restock low-stock products and logs updates.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    transport = RequestsHTTPTransport(
        url='http://localhost:8000/graphql',
        verify=False,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=False)

    mutation = gql("""
    mutation {
        updateLowStockProducts {
            updatedProducts {
                name
                stock
            }
            success
        }
    }
    """)

    try:
        result = client.execute(mutation)
        data = result.get("updateLowStockProducts", {})
        products = data.get("updatedProducts", [])
        message = data.get("success", "Restock completed")

        with open("/tmp/low_stock_updates_log.txt", "a") as log_file:
            log_file.write(f"{now} - {message}\n")
            for p in products:
                log_file.write(f"{now} - {p['name']} restocked to {p['stock']}\n")

    except Exception as e:
        with open("/tmp/low_stock_updates_log.txt", "a") as log_file:
            log_file.write(f"{now} - Error: {str(e)}\n")
