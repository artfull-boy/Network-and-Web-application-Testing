import time
from zapv2 import ZAPv2
import json 

def run_owasp_zap(url, api_key, output_file):
    zap = ZAPv2(apikey=api_key)  # Initialize ZAP with the provided API key

    # Open the target URL
    zap.urlopen(url)
    time.sleep(2)  # Allow time for URL to open

    # Spider the target
    spider_scan_id = zap.spider.scan(url)
    while int(zap.spider.status(spider_scan_id)) < 100:
        print(f"Spider progress: {zap.spider.status(spider_scan_id)}%")
        time.sleep(2)

    print("Spider scan completed")

    # Start Active Scan
    active_scan_id = zap.ascan.scan(url)
    while int(zap.ascan.status(active_scan_id)) < 100:
        print(f"Active scan progress: {zap.ascan.status(active_scan_id)}%")
        time.sleep(5)

    print("Active scan completed")

    # Retrieve Alerts
    alerts = zap.core.alerts(baseurl=url)

    # Organize alerts into a structured format
    organized_alerts = {
        "url": url,
        "total_alerts": len(alerts),
        "alerts": []
    }

    for alert in alerts:
        organized_alert = {
            "alert": alert.get("alert"),
            "risk": alert.get("risk"),
            "confidence": alert.get("confidence"),
            "url": alert.get("url"),
            "param": alert.get("param"),
            "evidence": alert.get("evidence"),
            "description": alert.get("description"),
            "solution": alert.get("solution"),
            "reference": alert.get("reference"),
        }
        organized_alerts["alerts"].append(organized_alert)

    # Save the organized alerts to a file
    with open(output_file, "w") as file:
        json.dump(organized_alerts, file, indent=2)

    return organized_alerts


