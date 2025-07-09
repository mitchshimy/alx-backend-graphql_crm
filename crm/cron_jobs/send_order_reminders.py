#!/usr/bin/env python3
"""
Script to fetch orders from the last 7 days and log reminders.
"""

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime, timedelta

# Setup GraphQL client
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
    verify=False,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=False)

# Date filtering
seven_days_ago = (datetime.now() - timedelta(days=7)).date().isoformat()

# GraphQL query
query = gql("""
query GetRecentOrders($since: Date!) {
  orders(orderDate_Gte: $since) {
    edges {
      node {
        id
        customer {
          email
        }
      }
    }
  }
}
""")

variables = {"since": seven_days_ago}

try:
    result = client.execute(query, variable_values=variables)
    orders = result.get("orders", {}).get("edges", [])

    with open("/tmp/order_reminders_log.txt", "a") as log_file:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for order in orders:
            node = order["node"]
            order_id = node["id"]
            email = node["customer"]["email"]
            log_file.write(f"{now}: Reminder - Order #{order_id}, Email: {email}\n")

    print("Order reminders processed!")

except Exception as e:
    print(f"Error processing order reminders: {e}")
