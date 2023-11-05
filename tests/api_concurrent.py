import concurrent.futures

import requests


# Define the function to make an API request
def make_api_request():
    url = "http://127.0.0.1:4003/server/applications"
    payload = {}
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4YTVmN2FhYmIwZTk0Nzg0OWEwZDE2YzgyNTYwYjUwZSIsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIiwicm9sZXMiOlsic3VwcG9ydF9hZG1pbiJdLCJleHAiOjE2OTU1MjI3MDl9.wYpHLQdbzRoBM9q-5G9p1fYDsVBWzJKx453QIEAVxwQ"
    }
    response = requests.get(
        url=url, headers=headers
    )  # Replace with your API endpoint
    return response.status_code


# Number of concurrent requests
num_requests = 100

# Create a ThreadPoolExecutor with the desired number of threads
with concurrent.futures.ThreadPoolExecutor(
    max_workers=num_requests
) as executor:
    # Submit the API request function for concurrent execution
    future_to_request = {
        executor.submit(make_api_request): i for i in range(num_requests)
    }

    # Wait for all requests to complete
    for future in concurrent.futures.as_completed(future_to_request):
        request_number = future_to_request[future]
        try:
            status_code = future.result()
            print(f"Request {request_number}: Status Code {status_code}")
        except Exception as e:
            print(f"Request {request_number} generated an exception: {e}")
