# Local Food Wastage Management System 🍎♻️

This project is a web-based application built with **Streamlit** and **SQLite** to combat food waste and food insecurity. It provides a platform for food providers to list surplus food and for receivers to find available donations, creating a digital bridge for efficient food redistribution.

## Key Features

-   **Interactive Dashboard:** Provides a quick, at-a-glance overview of key metrics such as total available food, the number of providers, and the number of receivers, presented in a clean, card-based format.
-   **Detailed Analysis:** A dedicated page with a comprehensive collection of dataframes providing in-depth insights into providers, claims, and distribution patterns.
-   **Food Listings:** Browse, filter, and search through available food listings using a user-friendly, card-based interface with collapsible details.
-   **Provider Actions:** A secure section for providers to easily **C**reate, **R**ead, **U**pdate, and **D**elete their food listings.
-   **SQL Query Runner:** An advanced feature that allows users to run custom SQL queries directly against the database for powerful, on-demand data exploration.

---

## Tech Stack

-   **Framework:** Streamlit
-   **Database:** SQLite3
-   **Data Manipulation:** Pandas

---

## Getting Started

Follow these steps to get a copy of the project up and running on your local machine.

### Prerequisites

-   Python 3.8 or newer
-   Git

### Installation

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/shiv915141/Local-Food-Wastage-Management-System.git](https://github.com/shiv915141/Local-Food-Wastage-Management-System.git)
    cd Local-Food-Wastage-Management-System
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    # On Windows:
    # venv\Scripts\activate
    # On macOS/Linux:
    # source venv/bin/activate
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

Once the dependencies are installed, you can run the Streamlit application from your terminal:
This will automatically open the application in your default web browser.

File Structure
app.py: The main Streamlit application file containing the user interface and page navigation.

database_manager.py: Contains functions to handle database connections, table creation, and data loading/retrieval.

data_analysis.py: Houses the functions that perform the various SQL queries and data analysis for the dashboard.

requirements.txt: Lists all Python package dependencies required to run the project.

README.md: This file, providing project information and setup instructions.

LICENSE.md: The license file for the project.

License
This project is licensed under the MIT License. See the LICENSE.md file for more details.

Contact
If you have any questions, feel free to open an issue on GitHub or contact at shivkumardubey997@gmail.com


```bash
streamlit run app.py
