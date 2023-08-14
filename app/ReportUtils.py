import datetime

from app import db
from app.log import log
from app.models import MenuHours, StoreStatusEnum, ReportTask, ReportEntry


class ReportUtils:
    """
     Utility class for generating, storing, and retrieving report data.

     Attributes:
         None
     """
    @staticmethod
    def generate_and_store_report_data(report_id, store, current_timestamp):
        """
        Generates and stores report data for a store.

        Args:
            report_id (str): The ID of the report.
            store (MenuHours): The store's business hours.
            current_timestamp (datetime.datetime): The current timestamp.

        Returns:
            None
        """
        try:
            log.info("Generating and storing report data for store: %s", store.store_id)

            # Retrieve store's business hours
            business_hours = MenuHours.query.filter_by(store_id=store.store_id).all()

            # Calculate report data for uptime and downtime
            uptime_last_hour, downtime_last_hour = ReportUtils.calculate_uptime_downtime(
                store.store_id, current_timestamp - datetime.timedelta(hours=1), current_timestamp
            )
            uptime_last_day, downtime_last_day = ReportUtils.calculate_uptime_downtime(
                store.store_id, current_timestamp - datetime.timedelta(days=1), current_timestamp
            )
            update_last_week, downtime_last_week = ReportUtils.calculate_uptime_downtime(
                store.store_id, current_timestamp - datetime.timedelta(weeks=1), current_timestamp
            )

            # Create a new ReportEntry and store it in the database
            report_entry = ReportEntry(
                report_id=report_id,
                store_id=store.store_id,
                uptime_last_hour=uptime_last_hour,
                uptime_last_day=uptime_last_day,
                update_last_week=update_last_week,
                downtime_last_hour=downtime_last_hour,
                downtime_last_day=downtime_last_day,
                downtime_last_week=downtime_last_week
            )
            log.debug("Storing report entry: %s", report_entry)
            db.session.add(report_entry)
            db.session.commit()

            log.info("Report data generation and storage completed for store: %s", store.store_id)
        except Exception as e:
            log.error("An error occurred while generating and storing report data: %s", str(e))

    @staticmethod
    def calculate_uptime_downtime(store_id, start_time, end_time):
        """
        Calculates the uptime and downtime for a store within a specified time range.

        Args:
            store_id (int): The ID of the store.
            start_time (datetime.datetime): The start time of the calculation.
            end_time (datetime.datetime): The end time of the calculation.

        Returns:
            float: Total uptime in hours.
            float: Total downtime in hours.
        """
        try:
            log.debug("Calculating uptime and downtime for store: %s", store_id)

            # Retrieve the store's business hours
            business_hours = MenuHours.query.filter_by(store_id=store_id).all()

            # Initialize variables to track uptime and downtime
            total_business_hours = 0
            total_uptime = 0

            # Calculate uptime and downtime based on business hours and status
            for business_hour in business_hours:
                overlap_start = max(business_hour.start_time_local, start_time.time())
                overlap_end = min(business_hour.end_time_local, end_time.time())

                if overlap_start < overlap_end:
                    # Calculate the duration of overlap in seconds
                    overlap_duration_seconds = (
                                                       overlap_end.hour * 3600 + overlap_end.minute * 60 + overlap_end.second) - (
                                                       overlap_start.hour * 3600 + overlap_start.minute * 60 + overlap_start.second)

                    total_business_hours += overlap_duration_seconds / 3600
                    status = ReportUtils.get_store_status(store_id, overlap_start, overlap_end)
                    if status == StoreStatusEnum.ACTIVE:
                        total_uptime += overlap_duration_seconds / 3600

            total_downtime = total_business_hours - total_uptime

            log.debug("Uptime: %.2f hours, Downtime: %.2f hours", total_uptime, total_downtime)

            return total_uptime, total_downtime
        except Exception as e:
            log.error("An error occurred while calculating uptime and downtime: %s", str(e))

    @staticmethod
    def get_store_status(store_id, start_time, end_time):
        """
        Get the status of a store within a specified time range.

        Args:
            store_id (int): The ID of the store.
            start_time (datetime.time): The start time of the interval.
            end_time (datetime.time): The end time of the interval.

        Returns:
            StoreStatusEnum: The status of the store within the given interval.
        """
        return StoreStatusEnum.ACTIVE

    @staticmethod
    def get_report_status_and_data(report_id):
        """
        Get the status and CSV data of a report.

        Args:
            report_id (str): The ID of the report.

        Returns:
            tuple: A tuple containing the report status and CSV data (if available).
        """
        # Check the status of the report in the database
        report_task = ReportTask.query.filter_by(report_id=report_id).first()

        if report_task is None:
            # Report task not found
            return "Not Found", None

        if report_task.status == "Complete":
            csv_data = ReportUtils.generate_report_csv_data(report_id)
            return report_task.status, csv_data
        else:
            return report_task.status, None

    @staticmethod
    def generate_report_csv_data(report_id):
        """
                Generate CSV data for a report.

                Args:
                    report_id (str): The ID of the report.

                Returns:
                    str: CSV data for the report.
        """
        report_entries = ReportEntry.query.filter_by(report_id=report_id).all()
        csv_data = "store_id,uptime_last_hour,uptime_last_day,update_last_week,downtime_last_hour,downtime_last_day,downtime_last_week\n"
        for entry in report_entries:
            csv_data += f"{entry.store_id},{entry.uptime_last_hour},{entry.uptime_last_day},{entry.update_last_week},{entry.downtime_last_hour},{entry.downtime_last_day},{entry.downtime_last_week}\n"

        return csv_data

    @staticmethod
    def generate_reports(report_id, current_timestamp, stores):
        """
        Generate reports for multiple stores.

        Args:
           report_id (str): The ID of the report.
           current_timestamp (datetime.datetime): The current timestamp.
           stores (list of dict): List of store information dictionaries.

        Returns:
           str: The ID of the generated report.
        """
        try:
            log.info("Generating reports for %d stores", len(stores))

            # Generate and store report data for each store
            for store_info in stores:
                log.info("Generating report for store: %s", store_info)
                ReportUtils.generate_and_store_report_data(report_id, store_info, current_timestamp)

            log.info("Reports generation completed for %d stores", len(stores))

            return report_id
        except Exception as e:
            log.error("An error occurred while generating reports: %s", str(e))
