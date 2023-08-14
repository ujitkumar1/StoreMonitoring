# Store Monitoring API: A Python app for generating and managing store reports

## Description

This RESTful API, built with Python Flask and Celery, enables users to trigger and generate store reports
asynchronously. The reports contain information about various stores, their timezones, and relevant data. Users can also
retrieve the generated reports for analysis.

## Prerequisites

Before using this application, ensure you have the following prerequisites:

1. Python Programming Language
2. MySQL
3. Flask
4. Flask-RESTful
5. JSON
6. Redis
7. Celery

## Installation

To install the required packages and libraries, run the following command in your terminal:

```
pip install -r requirements.txt
```

This command will install all the necessary dependencies listed in the requirements.txt file, allowing you to run the
project without any issues.

### Usage:

1. Start the application by running the following command in the project directory:

```
python main.py
```

This will start the application, and you should be able to use it. (or) Directly run the main.py file by defalt the url
of application would be : http://127.0.0.1:5000

2. To run Celery and Redis, execute the following commands in separate terminal (for windows use WSL)

```
redis-server
celery -A app.celery worker -l info
```

This will start the Redis server and the Celery worker to enable asynchronous task processing.

#### Endpoint Working:

1. **Trigger Report Generation**:

    - Endpoint: /trigger_report
    - Description: Trigger the generation of a store report.
    - Method: POST
    - Example Request:```POST http://127.0.0.1:5000/trigger_report```
    - Example Response:
    - ```{"report_id": "5e379ee1"}```


2. **Get Generated Report**:

    - Endpoint: /get_report/<string:report_id>
    - Description: Retrieve a generated store report.
    - Method: GET
    - Example Request: ```GET http://127.0.0.1:5000/get_report/5e379ee1```
    - Example Response (Report Generation in Progress):
    - ```{"Status": "Running"}```
    - Example Response (Report Generation Completed):
    - ```{"Status": "Completed","Path": "report/5e379ee1.csv"}```

### logic for computing the hours
1. The function calculate_uptime_downtime is responsible for calculating the uptime and downtime of a store within a specific time period.

2. It takes three arguments: store_id (the ID of the store), start_time (the beginning of the time period), and end_time (the end of the time period).

3. Inside the function:

 - It first retrieves the business hours of the store using the MenuHours table from the database.
 - It initializes variables to keep track of the total business hours, total uptime, and total downtime.

4. The function then goes through each business hour for the store and checks if there's an overlap between the business hour and the specified time period.

5. If an overlap exists:

 - It calculates the duration of the overlap in seconds.
 - Adds this overlap duration to the total business hours.
 - It simulates retrieving the store's status during this overlap from the get_store_status function. If the store is active during this time, it adds the overlap duration to the total uptime.

6. Finally, the function calculates the total downtime by subtracting the total uptime from the total business hours.

7. The calculated total uptime and total downtime are returned as a tuple.

8. If any error occurs during this process, it is caught, and an error message is logged.

This function essentially helps determine the time the store was operational (uptime) and the time it was not operational (downtime) within a given time period, considering its business hours and status.

### Contact:

**Name** : Ujit Kumar

**Email** : ujitkumar1@gmail.com

