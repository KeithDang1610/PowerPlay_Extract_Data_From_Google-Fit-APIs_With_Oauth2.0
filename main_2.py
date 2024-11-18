import pandas as pd
import json
from authenticate import get_fit_service
from datetime import datetime

def get_fit_data(service, data_source_ids, start_time, end_time):
    url = 'https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate'
        # Prepare the aggregate data request body
    aggregate_request = {
        "aggregateBy": [{"dataSourceId": source_id} for source_id in data_source_ids],
        "bucketByTime": {"durationMillis": 86400000},  # 1 day in milliseconds
        "startTimeMillis": start_time,
        "endTimeMillis": end_time
    }

    # Convert the aggregate request body to JSON string and encode it to bytes
    body = json.dumps(aggregate_request).encode('utf-8')
    print(body)
    # Send the POST request to the aggregate endpoint
    response, content = service._http.request(
        url,
        method="POST",
        body=body
    )

        # Check if response is successful
    if response.status == 200:
        print("success")
        print(json.loads(content))
        return json.loads(content)
        
    else:
        print(f"Error: {response.status}")
        return None



def process_fit_data(content):
    # data = []
    # # Loop through the buckets in the response
    # for bucket in content.get("bucket", []):
    #     for point in bucket.get("point", []):
    #         start_time = point.get("startTimeNanos")
    #         end_time = point.get("endTimeNanos")
    #         for value in point.get("value", []):
    #             # Extracting the value for each data point
    #             data.append({
    #                 "start_time": start_time,
    #                 "end_time": end_time,
    #                 "value": value.get("intVal", 0)  # Adjust if necessary
    #             })
    # print(data)
    # return pd.DataFrame(data)
    daily_steps = {}

# Iterate through each day's data
    for day in content['bucket']:
        start_time = int(day['startTimeMillis'])
        date = datetime.utcfromtimestamp(start_time // 1000).strftime('%Y-%m-%d')
        steps = sum(point['value'][0]['intVal'] for dataset in day['dataset'] for point in dataset['point'])
        daily_steps[date] = steps

    # Print summary
    for date, steps in daily_steps.items():
        print(f"{date}: {steps} steps")

def main():
    # Step 3: Authenticate and create the service
    fit_service = get_fit_service()

    # Example data source IDs; replace with real values
    data_source_ids = [
        "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"
        #,"derived:com.google.sleep.segment:com.google.android.gms:merged",
        #"derived:com.google.heart_minutes:com.google.android.gms:merge_heart_minutes",
        #"derived:com.google.calories.expended:com.google.android.gms:merge_calories_expended"
    ]

    # Specify the time range (startTimeMillis and endTimeMillis are in milliseconds)
    start_time = 1729875600000  # Example start time (Oct 26, 2024, 00:00:00)
    end_time = 1731776400000    # Example end time (Nov 17, 2024, 00:00:00)

    # Step 4: Get aggregated data from Google Fit
    fit_data_response = get_fit_data(fit_service, data_source_ids, start_time, end_time)

    # Step 5: Process and convert data to DataFrame
    fit_data_df = process_fit_data(fit_data_response)

    print(fit_data_df)


if __name__ == "__main__":
    main()
