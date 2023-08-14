from datetime import datetime
from enum import Enum

from sqlalchemy import Time

from app import db


class StoreStatusEnum(Enum):
    """
    Enumeration for store status values.

    Attributes:
        ACTIVE (str): Represents an active store status.
        INACTIVE (str): Represents an inactive store status.
    """
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class MenuHours(db.Model):
    """
    Model class to represent store menu hours.

    Attributes:
        id (int): Primary key identifier.
        store_id (int): ID of the store.
        day (int): Day of the week (0-6, where 0 represents Monday).
        start_time_local (Time): Start time of menu hours in local time.
        end_time_local (Time): End time of menu hours in local time.
    """
    __tablename__ = 'MenuHours'
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    start_time_local = db.Column(Time, nullable=False)
    end_time_local = db.Column(Time, nullable=False)


class StoreStatus(db.Model):
    """
    Model class to represent store status history.

    Attributes:
        id (int): Primary key identifier.
        store_id (int): ID of the store.
        status (StoreStatusEnum): Store status (active or inactive).
        timestamp (datetime): Timestamp of the status change.
    """
    __tablename__ = 'StoreStatus'
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum(StoreStatusEnum), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)


class TimeZone(db.Model):
    """
    Model class to represent store time zones.

    Attributes:
        id (int): Primary key identifier.
        store_id (int): ID of the store.
        timezone_str (str): Time zone string (e.g., 'Asia/Kolkata').
    """
    __tablename__ = 'TimeZone'
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, nullable=False)
    timezone_str = db.Column(db.String, nullable=False)


class ReportEntry(db.Model):
    """
    Model class to represent report entries.

    Attributes:
        id (int): Primary key identifier.
        report_id (str): ID of the report.
        store_id (int): ID of the store.
        uptime_last_hour (float): Uptime in hours for the last hour.
        uptime_last_day (float): Uptime in hours for the last day.
        update_last_week (float): Uptime in hours for the last week.
        downtime_last_hour (float): Downtime in hours for the last hour.
        downtime_last_day (float): Downtime in hours for the last day.
        downtime_last_week (float): Downtime in hours for the last week.
    """
    __tablename__ = 'ReportEntry'
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.String, nullable=False)
    store_id = db.Column(db.Integer, nullable=False)
    uptime_last_hour = db.Column(db.Float, nullable=False)
    uptime_last_day = db.Column(db.Float, nullable=False)
    update_last_week = db.Column(db.Float, nullable=False)
    downtime_last_hour = db.Column(db.Float, nullable=False)
    downtime_last_day = db.Column(db.Float, nullable=False)
    downtime_last_week = db.Column(db.Float, nullable=False)


class ReportTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.String, unique=True, nullable=False)
    status = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
