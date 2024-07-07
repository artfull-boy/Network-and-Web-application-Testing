import time
import json
from gvm.connections import TLSConnection
from gvm.protocols.gmp import Gmp
from gvm.transforms import EtreeTransform

def run_openvas_scan(target_ip, username, password, output_file):
    # Connect to the Greenbone Vulnerability Manager
    connection = TLSConnection(hostname='localhost', port=9392, timeout=12000)
    with Gmp(connection=connection, transform=EtreeTransform()) as gmp:
        gmp.authenticate(username, password)

        # Create target
        response = gmp.create_target(name='OpenVAS Scan Target', hosts=[target_ip])
        target_id = response.xpath('//@id')[0]

        # Create scan config (using the Full and Fast configuration)
        response = gmp.get_scan_configs(filter_string='Full and fast')
        scan_config_id = response.xpath('//scan_config/@id')[0]

        # Create a task
        response = gmp.create_task(
            name='OpenVAS Scan Task',
            config_id=scan_config_id,
            target_id=target_id
        )
        task_id = response.xpath('//@id')[0]

        # Start the task
        response = gmp.start_task(task_id)
        report_id = response.xpath('//@id')[0]

        # Wait for the scan to complete
        while True:
            response = gmp.get_task(task_id=task_id)
            status = response.xpath('//task/status/text()')[0]
            if status == 'Done':
                break
            print(f"Scan progress: {status}")
            time.sleep(30)

        print("Scan completed")

        # Get the report
        response = gmp.get_report(report_id=report_id, filter_string='apply_overrides=0 levels=hmlc')
        report = response.xpath('//report')[0]

        # Organize the results into a structured format
        organized_results = {
            "target": target_ip,
            "report_id": report_id,
            "results": []
        }

        for result in report.xpath('.//result'):
            organized_result = {
                "id": result.xpath('id/text()')[0],
                "name": result.xpath('name/text()')[0],
                "severity": result.xpath('severity/text()')[0],
                "description": result.xpath('description/text()')[0],
                "solution": result.xpath('solution/text()')[0],
                "reference": result.xpath('reference/text()')[0] if result.xpath('reference/text()') else None,
                "location": result.xpath('location/text()')[0] if result.xpath('location/text()') else None,
            }
            organized_results["results"].append(organized_result)

        # Save the organized results to a file
        with open(output_file, "w") as file:
            json.dump(organized_results, file, indent=2)

    return organized_results

# Example usage
target_ip = "192.168.56.101"
username = 'admin'  # Replace with your actual OpenVAS username
password = '5e753206-bbca-4a32-9ff2-94d0148b8768'  # Replace with your actual OpenVAS password
output_file = "./results/openvas_results.json"
openvas_results = run_openvas_scan(target_ip, username, password, output_file)
print(json.dumps(openvas_results, indent=2))
