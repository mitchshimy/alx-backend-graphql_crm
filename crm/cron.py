from datetime import datetime

def log_crm_heartbeat():
    """
    Logs a heartbeat message with timestamp to confirm CRM is alive.
    """
    now = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    with open('/tmp/crm_heartbeat_log.txt', 'a') as log_file:
        log_file.write(f"{now} CRM is alive\n")
