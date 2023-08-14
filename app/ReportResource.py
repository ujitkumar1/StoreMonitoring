import os

from flask_restful import Resource

from app import ReportUtils
from app.log import log


class ReportResource(Resource):
    """
    RESTful resource class for handling report requests.

    Attributes:
        None
    """

    def get(self, report_id):
        """
        Handles the GET request for report data.

        Args:
            report_id (str): The ID of the report to retrieve.

        Returns:
            dict: A dictionary containing the status of the report request.
                  If the report is running, returns {"status": "Running"}.
                  If the report is complete, returns {"Status": "Complete", "File Path": "csv_file_path/report_<report_id>.csv"}.
                  If an error occurs, returns {"error": "An error occurred"} with a 500 status code.
        """
        try:
            log.info("Received GET request for report_id: %s", report_id)

            # Get the status and CSV data for the report

            status, csv_data = ReportUtils.ReportUtils.get_report_status_and_data(report_id)

            if status == "Running":
                log.debug("Report with ID %s is still running", report_id)
                return {"status": status}, 200
            elif status == "Complete":
                csv_filename = f"report_{report_id}.csv"
                csv_file_path = f"reports"

                if csv_data is not None:
                    # Write CSV data to a file
                    with open(os.path.join(csv_file_path, csv_filename), "w") as f:
                        f.write(csv_data)

                log.debug("Report with ID %s is complete", report_id)
                return {'Status': "Complete", "File Path": f"csv_file_path/{csv_filename}"}
        except Exception as e:
            log.error("An error occurred while processing report request: %s", str(e))
            return {"error": "An error occurred"}, 500
