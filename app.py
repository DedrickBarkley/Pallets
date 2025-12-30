import os
from flask import Flask, request, render_template_string
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)

# Get connection string from environment variable
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# HTML upload form with container selection
UPLOAD_FORM = """
<!DOCTYPE html>
<html>
<body>
    <h2>Upload CSV File</h2>
    <form action="/upload" method="post" enctype="multipart/form-data">

        <label>Select document type:</label><br>
        <select name="container" required>
            <option value="vendor-uploads">vendor-uploads</option>
            <option value="customer-uploads">customer-uploads</option>
        </select>
        <br><br>

        <input type="file" name="file" accept=".csv" required>
        <br><br>

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
    container_name = request.form.get("container")

    if not file:
        return "No file uploaded", 400

    # Validate CSV file
    if not file.filename.lower().endswith(".csv"):
        return "Invalid file type. Only CSV files are allowed.", 400

    try:
        # Create blob client for selected container
        blob_client = blob_service_client.get_blob_client(
            container=container_name,
            blob=file.filename
        )

        blob_client.upload_blob(file, overwrite=True)

        return f"File '{file.filename}' uploaded successfully to container '{container_name}'!"
    except Exception as e:
        return f"Error uploading file: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
