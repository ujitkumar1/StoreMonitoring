import csv
from datetime import datetime

from app import db
from app import models


def add_data_from_csv():
    with open('data/Menu-hours.csv', 'r') as csv_file:
        print("Adding data for Menu Hours")
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            menu_hour = models.MenuHours(
                store_id=row['store_id'],
                day=int(row['day']),
                start_time_local=datetime.strptime(row['start_time_local'], '%H:%M:%S').time(),
                end_time_local=datetime.strptime(row['end_time_local'], '%H:%M:%S').time()
            )
            db.session.add(menu_hour)

        db.session.commit()
        print("Committed ...!")

        with open('data/store-status.csv', 'r') as csv_file:
            print("Adding data for store-status")
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                try:
                    store_status = models.StoreStatus(
                        store_id=row['store_id'],
                        status=row['status'],
                        timestamp=datetime.strptime(row['timestamp_utc'], '%Y-%m-%d %H:%M:%S UTC')
                    )
                except:
                    store_status = models.StoreStatus(
                        store_id=row['store_id'],
                        status=row['status'],
                        timestamp=datetime.strptime(row['timestamp_utc'], '%Y-%m-%d %H:%M:%S.%f UTC')
                    )
                db.session.add(store_status)
            db.session.commit()
            print("Committed ...!")

        with open('data/timezone.csv', 'r') as csv_file:
            print("Adding data for timezone")
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                timezone = models.TimeZone(
                    store_id=row['store_id'],
                    timezone_str=row['timezone_str']
                )
                db.session.add(timezone)
            db.session.commit()
            print("Committed ...!")

        print("Data added...!")
