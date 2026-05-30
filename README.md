# 🏎️ McLaren Telemetry Analysis: Lando Norris vs Oscar Piastri

This project features an End-to-End Data Engineering pipeline designed to process and analyze raw McLaren telemetry data, comparing the track performance of drivers Lando Norris and Oscar Piastri. The ultimate goal is to decode, through data, who gains the upper hand in critical metrics such as top speed, braking efficiency, and lap time consistency.

The entire processing pipeline was developed using **PySpark** within the **Databricks** environment, applying the practical concepts of the **Medallion Architecture**.

## 🏗️ Pipeline Architecture (Medallion Model)

The project is structured into three logical layers to ensure the organization, scalability, and quality of the IoT telemetry data:

* **🥉 Bronze Layer (Ingestion):** Consumes raw sensor data directly from the source (`mclaren_raw_telemetry.csv`), maintaining an immutable, append-only historical record of the track data.
* **🥈 Silver Layer (Cleaning & Standardization):** Handles missing values, performs data type casting (such as timestamps and velocity metrics), eliminates duplicates, and splits the data into distinct, clean streams for each driver (Norris vs. Piastri).
* **🥇 Gold Layer (Business Aggregation):** Generates analytical tables optimized for visualization and race strategy. In this stage, data is aggregated to extract direct track insights: who achieved the highest top speed on the straights, who braked later into corners, and who maintained the highest cornering consistency.

## 🔥 Case Study: Thermal Anomaly & Race Strategy Impact
During the analysis in the Gold layer, the pipeline detected a critical thermal event in Piastri's car. A sudden spike in brake disc temperatures forced an automated response: the driver had to manage the temperatures by lifting and coasting and braking earlier. This operational shift opened a telemetry window of vulnerability, which mathematically enabled Lando Norris to close the gap and execute the overtake.

## 🛠️ Tech Stack & Tools

* **Databricks:** Cloud data platform used for developing, orchestrating, and executing the pipeline.
* **PySpark (Apache Spark):** Distributed computing engine utilized for scalable manipulation of high-frequency telemetry data.
* **Python:** Core programming language used to build the Formula 1 business logic.
* **Git & GitHub:** Tools implemented for version control and portfolio publication.

## 📁 Repository Structure

The repository is organized into the following components:

* `mclaren_raw_telemetry.csv`: The raw dataset used as the starting point (Bronze Layer).
* `Telemetria McLaren.py`: The comprehensive script containing the complete Spark pipeline code (from Bronze to Gold).
