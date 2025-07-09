#!/bin/bash
# This script deletes customers with no orders in the past year and logs the count with a timestamp.

cd "$(dirname "$0")/../.."  # Navigate to the Django root project directory

deleted_count=$(python3 manage.py shell <<EOF
from crm.models import Customer, Order
from django.utils import timezone
from datetime import timedelta

one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.exclude(id__in=Order.objects.filter(created_at__gte=one_year_ago).values_list('customer_id', flat=True))
count = inactive_customers.count()
inactive_customers.delete()
print(count)
EOF
)

echo "$(date): Deleted $deleted_count inactive customers" >> /tmp/customer_cleanup_log.txt
