import os
from flask import Flask, request, render_template_string
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)

# Get connection string from environment variable
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Name of your container (create it in Azure Storage first)
CONTAINER_NAME = "uploads"

# Simple HTML upload form
UPLOAD_FORM = """
<!DOCTYPE html>
<html>
<body>
    <h2>Upload Excel File</h2>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept=".xlsx,.xls" required>
        <button type="submit">Upload</button>
    </form>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(UPLOAD_FORM)

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")

    if not file:
        return "No file uploaded", 400

    try:
        # Upload to Azure Blob Storage
        blob_client = blob_service_client.get_blob_client(
            container=CONTAINER_NAME,
            blob=file.filename
        )

        blob_client.upload_blob(file, overwrite=True)

        return f"File '{file.filename}' uploaded successfully!"
    except Exception as e:
        return f"Error uploading file: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
