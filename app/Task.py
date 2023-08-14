from app.ReportUtils import ReportUtils
from app import app
from app import celery
from app import db
from app.log import log
from app.models import TimeZone, ReportTask


@celery.task()
def generate_reports_task(report_id, current_timestamp, stores_info):
    """
    Celery task for generating and storing reports asynchronously.

    Args:
        report_id (str): The ID of the report.
        current_timestamp (datetime.datetime): The current timestamp.
        stores_info (list of dict): List of store information dictionaries.

    Returns:
        None
    """
    log.debug("C-task")
    with app.app_context():
        # Create TimeZone objects from store information
        stores = [TimeZone(store_id=int(info["store_id"]), timezone_str=info["timezone_str"]) for info in
                  stores_info]

        # Generate and store report data for each store
        for store_info in stores:
            log.debug("Processing store info: %s", store_info)
            ReportUtils.generate_and_store_report_data(report_id, store_info, current_timestamp)

        # Update the status of the ReportTask to "Complete"
        log.debug("Updating report task status to Complete: %s", report_id)
        report_task = ReportTask.query.filter_by(report_id=report_id).first()
        if report_task:
            report_task.status = "Complete"
            db.session.commit()
