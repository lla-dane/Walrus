# Example of uploading and downloading a file to / from the Walrus service
# Using the walrus client web API facilities.
#
# Prerequisites:
#
# - Run the Walrus client in daemon mode:
#   $ ../CONFIG/bin/walrus --config ../CONFIG/config_dir/client_config.yaml daemon -b 127.0.0.1:8899
#

# Std lib imports
import os
import time
import base64

# External requests HTTP library
import requests

AGG_ADDRESS = "walrus-testnet-aggregator.stakin-nodes.com"
PUB_ADDRESS = "walrus-testnet-publisher.bartestnet.com"
EPOCHS = "5"

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode('utf-8')  


# Helper functions to upload a blob
def upload_blob(ADDRESS, EPOCHS, data):
    print("UPLOADING...")
    # Upload the data to the Walrus service  using a PUT request
    store_url = f"https://{ADDRESS}/v1/store?epochs={EPOCHS}"
    response = requests.put(store_url, data=data)

    # Assert the response status code
    assert response.status_code == 200
    blob_id = response.json()["newlyCreated"]["blobObject"]["blobId"]
    return blob_id


# Helper functions to download a blob
def download_blob(ADDRESS, blob_id):
    print("DOWNLOADING")
    # Now read the same resource using the blob-id
    read_url = f"https://{ADDRESS}/v1/{blob_id}"
    response = requests.get(read_url)

    # Assert the response status code
    assert response.status_code == 200
    return response.content


# Upload a random 1MB string then download it, and check it matches
if __name__ == "__main__":
    # Generate a 1MB blob of random data
    real_string = "Abhinav AGarwalla."
    byte_data = real_string.encode('utf-8')
    
    # Upload the blob to the Walrus service
    start_time = time.time()
    
    image_bytes = image_to_base64("./nillion.png")
    print(image_bytes)
    
    blob_id = upload_blob(PUB_ADDRESS, EPOCHS, image_bytes)
    upload_time = time.time()
    print(blob_id)

    # Now download the same blob using the blob-id
    data = download_blob(AGG_ADDRESS, blob_id)
    print(data)
    # assert data == image_bytes
    download_time = time.time()

    # Print some information about the blob
    print(f"Blob ID: {blob_id}")
    # print(f"DOWNLOADED: {data} ")
    print(f"Upload time: {upload_time - start_time:.2f}s")
    print(f"Download time: {download_time - upload_time:.2f}s")
