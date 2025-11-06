# Energy Consumption Analysis & Forecast

An end-to-end data analytics project that transforms messy raw energy data into clean, interactive insights — featuring automated preprocessing, exploratory data analysis, and 7-day demand forecasting using **Meta’s Prophet**.

---

## Overview

This project cleans and analyzes energy consumption data from multiple consumers and visualizes **future forecasts** in a Streamlit dashboard.

### Highlights
- Automated ingestion & cleaning of 20+ Excel files  
- No statistical outliers (verified via Z-Score & IQR)  
- Dynamic EDA dashboards built with **Plotly + Streamlit**  
- Per-consumer **Prophet models** for accurate daily forecasts  
- Exportable forecast results and interactive charts  

---

## Tech Stack

**Python**, **Pandas**, **Plotly**, **Streamlit**, **Prophet**, **Matplotlib**

---

## Project Structure
Assignment/

├── dashboard.py # Streamlit dashboard (EDA + Forecast)

├── data_prep.ipynb # Data cleaning & merging

├── eda_power.ipynb # Exploratory analysis

├── prophet_forecast_model.py # Prophet model training

├── requirements.txt

---

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/callmegruz/energy-consumption-analysis
    cd energy-consumption-analysis

    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```
3.  **Install Python packages:**
    ```bash
    pip install -r requirements.txt
    ```


## Usage
1. Run data_prep.ipynn for loading, preparing and cleaning data.
2. Run eda_power.ipynb for Exploratory Data Analysis and Outlier test
3. Run prophet_forecast_model for building the forecast model

4.  **Run the application from the root directory:**
    ```bash
    streamlit run dashboard.py
    ```

