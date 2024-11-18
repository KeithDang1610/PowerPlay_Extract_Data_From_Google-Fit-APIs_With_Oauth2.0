import pandas as pd
from authenticate import get_fit_service


def get_fit_data(service, data_source_id):
    response = service.users().dataSources().datasets().get(
        userId="me",
        dataSourceId=data_source_id,
     #   datasetId=data_set_id
    ).execute()
    return response


def process_fit_data(response):
    data = []
    for point in response.get("point", []):
        start_time = point.get("startTimeNanos")
        end_time = point.get("endTimeNanos")
        for value in point.get("value", []):
            data.append({
                "start_time": start_time,
                "end_time": end_time,
                "value": value.get("fpVal", 0)  # Adjust if necessary
            })
    return pd.DataFrame(data)


def main():
    # Step 3: Authenticate and create the service
    fit_service = get_fit_service()

    # Example data source and dataset IDs; replace with real values
    data_source_id = ["derived:com.google.step_count.delta:com.google.android.gms:estimated_steps",
                      "derived:com.google.sleep.segment:com.google.android.gms:merged",
                      "derived:com.google.heart_minutes:com.google.android.gms:merge_heart_minutes",
                      "derived:com.google.calories.expended:com.google.android.gms:merge_calories_expended"]
    # data_set_id = "your_data_set_id"

    # Step 4: Get data from Google Fit
    fit_data_response = get_fit_data(fit_service, data_source_id, data_set_id)

    # Step 5: Process and convert data to DataFrame
    fit_data_df = process_fit_data(fit_data_response)

    print(fit_data_df)

if __name__ == "__main__":
    main()