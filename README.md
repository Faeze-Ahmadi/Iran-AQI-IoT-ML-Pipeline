# Iran AQI IoT ML Pipeline

This project builds an end-to-end, IoT-style data pipeline for **air quality (AQI)** in major Iranian cities (e.g., Tehran, Isfahan, Mashhad, Ahvaz).  
The goal is to use **real air quality data** to:

- Collect and preprocess sensor-like AQI and weather data
- Perform exploratory data analysis and visualizations
- Prepare time-series data for machine learning–based AQI forecasting
- Export models to **ONNX** for deployment
- Organize the code in a **modular, object-oriented (OOP)** structure with proper error handling

The project is designed as a realistic, production-inspired pipeline that connects **IoT concepts**, **time-series ML**, and **data visualization**.

## Project Overview

The pipeline fetches live AQI data from a public API, stores historical records in a SQLite database, and generates visual insights such as city-level AQI comparisons.

## Project Structure

- `src/` : Main source code
  - `config/` : Environment-based configuration management
  - `data_loader/` : API clients and data fetching logic
  - `pipeline/` : Data collection orchestration
  - `storage/` : SQLite persistence layer
  - `visualization/` : Plotting and visual analysis
- `data/` : Generated datasets, database, and plots
- `notebooks/` : (Future) exploratory analysis
- `main.py` : Application entry point

## Next Steps

- Collect and accumulate historical AQI data over time
- Perform time-series analysis and advanced visualizations
- Prepare features for machine learning models
- Train and evaluate AQI forecasting models
- Export trained models to ONNX for deployment

## Data Source

This project uses real-time air quality data provided by the World Air Quality Index (AQICN) project.

Data is fetched programmatically via the official AQICN API:
https://aqicn.org/data-platform/

All AQI values are based on real monitoring stations and are updated continuously.

