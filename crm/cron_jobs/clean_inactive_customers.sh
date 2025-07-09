#!/bin/bash
# Deletes customers with no orders in the past year and logs the deletion count.

# Get current working directory (cwd) of this script
SCRIPT_CWD="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Navigate to Django project root (2 levels up from cwd)
cd "$SCRIPT_CWD/../.." || {
    echo "Failed to change to project root directory"
    exit 1
}

# Run cleanup logic and get number of deleted customers
deleted_count=$(python3 manage.py shell <<EOF
from crm.models import Customer, Order
from django.utils import timezone
from datetime import timedelta

one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.exclude(
    id__in=Order.objects.filter(created_at__gte=one_year_ago).values_list('customer_id', flat=True)
)
count = inactive_customers.count()
inactive_customers.delete()
print(count)
EOF
)

# Log cleanup result
if [ -n "$deleted_count" ]; then
    echo "$(date): Deleted $deleted_count inactive customers" >> /tmp/customer_cleanup_log.txt
else
    echo "$(date): No customers deleted (or error occurred)" >> /tmp/customer_cleanup_log.txt
fi
