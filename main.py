from app import ReportResource
from app import TriggerReportResource
from app import app, api, db

api.add_resource(ReportResource.ReportResource, '/get_report/<string:report_id>')
api.add_resource(TriggerReportResource.TriggerReportResource, '/trigger_report')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
