#!/usr/bin/env python3
"""
Custom Integration Script: Wazuh Manager -> n8n Webhook
Location: /var/ossec/integrations/custom-n8n.py
Permissions: chmod 750, chown root:ossec
"""
import sys
import json
import requests

def main():
    if len(sys.argv) < 2:
        sys.exit(1)

    alert_filepath = sys.argv[1]
    
    try:
        with open(alert_filepath, 'r', encoding='utf-8') as f:
            alert_json = json.load(f)
    except Exception as e:
        with open("/var/ossec/logs/ossec.log", "a", encoding='utf-8') as log_file:
            log_file.write(f"Error leyendo archivo de alerta {alert_filepath}: {str(e)}\n")
        sys.exit(1)

    webhook_url = "http://10.3.100.11:5678/webhook-test/wazuh-alerts"
    
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(webhook_url, data=json.dumps(alert_json), headers=headers, timeout=5)
        response.raise_for_status()
    except Exception as e:
        with open("/var/ossec/logs/ossec.log", "a", encoding='utf-8') as log_file:
            log_file.write(f"Error en integracion Wazuh-n8n: {str(e)}\n")

    sys.exit(0)

if __name__ == "__main__":
    main()
