import datetime
import random

from flask_restful import Resource

from app import db
from app.log import log
from app.models import TimeZone, ReportTask
from app.Task import generate_reports_task


class TriggerReportResource(Resource):
    def post(self):
        """
        Handle POST request to trigger report generation.

        Returns:
            dict: A dictionary containing the generated report ID or an error message.
        """
        try:
            log.info("Request received")

            # Get the current timestamp
            current_timestamp = datetime.datetime.utcnow()
            log.debug("Current time: %s", current_timestamp)

            # Generate a random report ID for
            report_id = ''.join(random.choice('0123456789abcdef') for _ in range(8))
            log.debug("Report ID: %s", report_id)

            # Retrieve all stores' timezones from the database
            stores = TimeZone.query.all()

            # Extract relevant information from the TimeZone objects
            stores_info = [{"store_id": store.store_id, "timezone_str": store.timezone_str} for store in stores]

            log.info("Generating report....!")
            # Generate a report for each store asynchronously
            generate_reports_task.apply_async(args=(report_id, current_timestamp, stores_info))

            # Store the status as "Running" in the database
            report_task = ReportTask(report_id=report_id, status="Running")
            db.session.add(report_task)
            db.session.commit()

            return {"report_id": report_id}
        except Exception as e:
            log.error("An error occurred: %s", str(e))
            return {"error": "An error occurred"}, 500
