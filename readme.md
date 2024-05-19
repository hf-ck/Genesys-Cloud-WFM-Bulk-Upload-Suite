# Agent Utilization Update Script

## Overview

This script automates the process of updating agent utilization settings in Genesys Cloud using data from an Excel file. It reads agent utilization settings from an Excel file, searches for users by their email addresses, and updates their utilization settings via the Genesys Cloud API.

## Features

- Automated user search by email.
- Utilization update based on Excel data.
- Detailed logging of requests and responses.
- Ensures custom utilization settings are applied.
- Web interface for file upload and preview.
- Reset functionality to return to the initial state.

## Requirements

- Python 3.6+
- `pandas` library
- `requests` library
- `Flask` library

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   ```
2. **Navigate to the project directory:**
   ```bash
   cd <repository-directory>
   ```
3. **Install the required Python packages:**
   ```bash
   pip install pandas requests Flask
   ```
4. **Create a `config.json` file in the project directory with the following structure:**
   ```json
   {
       "client_id": "your_client_id",
       "client_secret": "your_client_secret"
   }
   ```

## Usage

1. **Ensure the `config.json` file and `agent_utilization.xlsx` are in the project directory.**
2. **Run the Flask app:**
   ```bash
   python app.py
   ```
3. **Open your web browser and go to:**
   ```
   http://127.0.0.1:5000
   ```
4. **Upload the Excel file using the web interface and preview the data.**
5. **Click "Process" to update the agent utilization settings.**
6. **Use the "Reset" button to clear the form and start over if needed.

## Excel File Format

The Excel file (`agent_utilization.xlsx`) should have the following columns:

- `Email Address`
- `Email Maximum Capacity`
- `Email Interruptable Media Types`
- `Chat Maximum Capacity`
- `Chat Interruptable Media Types`
- `Message Maximum Capacity`
- `Message Interruptable Media Types`
- `Callback Maximum Capacity`
- `Callback Interruptable Media Types`
- `Call Maximum Capacity`
- `Call Interruptable Media Types`
- `Workitem Maximum Capacity`
- `Workitem Interruptable Media Types`

### Example Excel File

| Email Address                 | Email Maximum Capacity | Email Interruptable Media Types | Chat Maximum Capacity | Chat Interruptable Media Types | Message Maximum Capacity | Message Interruptable Media Types | Callback Maximum Capacity | Callback Interruptable Media Types | Call Maximum Capacity | Call Interruptable Media Types | Workitem Maximum Capacity | Workitem Interruptable Media Types |
|-------------------------------|------------------------|---------------------------------|-----------------------|-------------------------------|--------------------------|----------------------------------|---------------------------|-----------------------------------|------------------------|-------------------------------|---------------------------|----------------------------------|
| charles.kim@hellofresh.com    | 3                      | call,chat                       | 3                     | callback,message              | 3                        | call,chat                         | 3                         | call,chat                          | 3                      | chat                          | 3                         | call,chat                         |
| nicholas.koch@hellofresh.com  | 3                      | call,chat                       | 3                     | callback,message              | 3                        | callback                          | 3                         | message                           | 3                      | callback,message              | 3                         | callback,message                   |

## Web Interface

### Pages

1. **Index Page (`index.html`):**
    - Upload an Excel file.
    - Preview the file content.

2. **Preview Page (`preview.html`):**
    - Display the content of the uploaded file.
    - Confirm and process the data to update agent utilization.

3. **Results Page (`results.html`):**
    - Display the results of the update process.
    - Options to go back to the main page or reset the form.

### How to Use

1. **Upload File:**
    - Select the Excel file and click "Preview".

2. **Preview File:**
    - Review the data in the uploaded file.
    - Click "Process" to update the utilization settings.

3. **Process Data:**
    - The results page will show the success or failure of each update.
    - Use the "Back" button to return to the main page.
    - Use the "Reset" button to clear the form and start over.

## Changes/Updates

### Version 1

- Automated user search by email.
- Utilization update based on Excel data.
- Detailed logging of requests and responses.

### Version 2

- **Web Interface**:
  - Added a web interface using Flask.
  - Allows users to upload Excel files and preview data before processing.
- **Reset Functionality**:
  - Added a reset button to clear the form and return to the initial state.
- **Correct User ID Usage**:
  - Fixed issues with using email instead of user ID for updating utilization.
- **Improved Data Handling**:
  - Fixed issues with extra characters in the preview and results.
  
### Code Version Differences

**Version 1**: Initial Code

**Version 2**: Updated Code with Web Interface

## License

This project is licensed under the MIT License.
