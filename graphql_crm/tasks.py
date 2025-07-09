from celery import shared_task
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

@shared_task
def generate_crm_report():
    """
    Generates a CRM report with total customers, orders, and revenue.
    Logs result to /tmp/crm_report_log.txt
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        transport = RequestsHTTPTransport(
            url='http://localhost:8000/graphql',
            verify=False,
            retries=3
        )
        client = Client(transport=transport, fetch_schema_from_transport=False)

        query = gql("""
        query {
            totalCustomers
            totalOrders
            totalRevenue
        }
        """)

        result = client.execute(query)
        customers = result.get('totalCustomers', 0)
        orders = result.get('totalOrders', 0)
        revenue = result.get('totalRevenue', 0.0)

        with open('/tmp/crm_report_log.txt', 'a') as f:
            f.write(f"{now} - Report: {customers} customers, {orders} orders, {revenue} revenue\n")

    except Exception as e:
        with open('/tmp/crm_report_log.txt', 'a') as f:
            f.write(f"{now} - Error generating report: {str(e)}\n")
