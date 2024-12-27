import requests

# Replace with your Freepik API key
# API_KEY = "FPSXaa11b9ac63744a619f3ab20df2157ea9"
API_KEY = "<my_api_key>"
BOT_TOKEN = "7642750809:AAGia4vhE-SE_024OcrbVBi6EKPA4yvcFU8"
API_KEY = "FPSXaa11b9ac63744a619f3ab20df2157ea9"
# Example resource ID and desired format
resource_id = "5326262"  # Replace with the actual resource ID
resource_format = "png"  # Format (e.g., 'png', 'jpg', 'psd', etc.)

# API endpoint
url = f"https://api.freepik.com/v1/icons/{resource_id}/download"

# Headers for authentication
headers = {
    "x-freepik-api-key": API_KEY
}

# Make the API request
response = requests.get(url, headers=headers)

# Check response status
if response.status_code == 200:
    # Extract download URL
    data = response.json()
    download_url = data['data'][0]['url']
    print(f"Download URL: {download_url}")

    # Optional: Download the file
    file_response = requests.get(download_url)
    with open(f"resource.{resource_format}", "wb") as file:
        file.write(file_response.content)
    print("File downloaded successfully.")
else:
    print(f"Failed to fetch resource: {response.status_code} - {response.text}")
