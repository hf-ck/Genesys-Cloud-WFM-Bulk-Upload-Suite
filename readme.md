# Genesys Cloud WFM Bulk Upload Suite

## Overview

This repository is part of a suite of tools designed for Workforce Management (WFM) in Genesys Cloud. The suite provides utilities for bulk uploading various configurations, including agent utilization settings. The web interface has been updated to use a different framework (replacing Flask) and includes enhanced navigation, making it easily extendable to include additional utilities.

## Features

- **Batch Agent Utilization Updates:** Upload and process Excel files to update agent utilization settings in bulk.
- **Dynamic Navigation:** Easily navigate between different tools within the web application.
- **Extensible Framework:** Simple integration of additional WFM tools.

## Table of Contents

- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)
- [Running the Application](#running-the-application)
- [Adding New Utilities](#adding-new-utilities)
- [Project Structure](#project-structure)
- [Update Logs](#update-logs)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Clone the Repository:**
    ```sh
    git clone https://github.com/hf-ck/Genesys-Cloud-Agent-Utilization-Update-Utility.git
    cd Genesys-Cloud-Agent-Utilization-Update-Utility
    ```

2. **Create and Activate a Virtual Environment:**
    ```sh
    python -m venv env
    source env/bin/activate   # On Windows, use `env\Scripts\activate`
    ```

3. **Install Dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Create a `.env` File:**
    ```
    GENESYS_CLIENT_ID=your_client_id
    GENESYS_CLIENT_SECRET=your_client_secret
    GENESYS_OAUTH_URL=https://login.mypurecloud.com/oauth/token
    GENESYS_API_BASE_URL=https://api.mypurecloud.com
    ```

## Setup

1. **Initialize the Application:**
    ```sh
    python run.py
    ```

2. **Access the Application:**
    Open your browser and navigate to `http://127.0.0.1:5000`.

## Usage

1. **Upload Utilization File:**
    - Navigate to the `Utilization` section from the main navigation bar.
    - Upload your Excel file containing agent utilization data.
    - Preview the uploaded data and ensure it is correct.
    - Click "Process File" to update the agent utilization settings in Genesys Cloud.

2. **Navigation:**
    - Use the navigation bar at the top to switch between different utilities and return to the home page.

## Running the Application

### Using Waitress for Production on Windows

For a production environment on Windows, it's recommended to use a production-ready server like `waitress`:

1. **Install `waitress`**:
    ```sh
    pip install waitress
    ```

2. **Run the application with `waitress`**:
    ```sh
    waitress-serve --host=0.0.0.0 --port=5000 run:app
    ```

This will make the application accessible from any network interface on your host machine, using `http://<your-machine-ip>:5000`.

## Adding New Utilities

To add a new utility:

1. **Create a New Module:**
    ```python
    from some_framework import Blueprint, render_template

    new_utility_bp = Blueprint('new_utility', __name__)

    @new_utility_bp.route('/')
    def index():
        return render_template('new_utility.html')
    ```

2. **Register the Module:**
    Add the new module to the main application file:
    ```python
    from app.routes.new_utility import new_utility_bp

    def create_app():
        app = SomeFrameworkApp()
        # Register modules
        app.register_blueprint(utilization_bp, url_prefix='/utilization')
        app.register_blueprint(new_utility_bp, url_prefix='/new_utility')
        # Other setup code
        return app
    ```

3. **Create the Template:**
    Create a corresponding template `new_utility.html` in the `templates` directory.

4. **Update Navigation Links:**
    Update the navigation links in the main application file:
    ```python
    app.config['NAVIGATION_LINKS'] = {
        'Utilization': '/utilization',
        'New Utility': '/new_utility',
        # Add more links here
    }
    ```

## Project Structure

Genesys-Cloud-WFM-Bulk-Upload-Suite/
├── app/
│ ├── init.py
│ ├── routes/
│ │ ├── init.py
│ │ ├── utilization.py
│ │ ├── new_utility.py # Example new utility
│ ├── templates/
│ │ ├── base.html
│ │ ├── index.html
│ │ ├── preview.html
│ │ ├── utilization.html
│ │ ├── new_utility.html # Example new utility template
│ ├── static/
├── uploads/
├── .env
├── config.py
├── requirements.txt
├── run.py

markdown
Copy code

## Update Logs

### Version 1.1.0

- Updated the framework from Flask to a new framework.
- Enhanced navigation and layout for better user experience.
- Added support for the `waitress` server for Windows environments.
- Improved the extensibility to easily integrate additional WFM tools.

### Version 1.0.0

- Initial release with batch agent utilization updates.
- Basic navigation and layout using Flask.
- Simple file upload and processing for agent utilization settings.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for review.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
