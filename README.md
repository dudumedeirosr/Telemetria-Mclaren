McLaren Telemetry Analysis: Lando Norris vs Oscar Piastri

This project consists of a Data Engineering pipeline developed to process and analyze raw telemetry data from McLaren, comparing the performance of drivers Lando Norris and Oscar Piastri. The goal is to decipher, through data, who has the edge in metrics such as top speed, braking efficiency, and lap time consistency.

All processing was developed using PySpark within the Databricks environment, applying the practical concepts of the Medallion Architecture.

Pipeline Architecture (Medallion Model)

The project was structured into three logical layers to ensure the organization and quality of the telemetry data:

Bronze Layer (Ingestion): Consumption of raw data directly from the sensor file (mclaren_raw_telemetry.csv), maintaining the faithful history of the track without any alterations.

Silver Layer (Cleaning and Standardization): Treatment of null values, data type conversion (such as time and speed formats), elimination of duplicates, and clear separation of each driver's records (Norris vs. Piastri).

Gold Layer (Business Aggregation): Creation of analytical tables ready for visualization. In this stage, data was aggregated to extract insights straight from the track: who had the highest top speed on the straights, who braked later, and who was more consistent in the corners.

Technologies and Tools Used

Databricks: Cloud data platform used for developing and running the pipeline.

PySpark (Apache Spark): Distributed processing engine for scalable manipulation of telemetry data.

Python: Base language for building the business rules of the Formula 1 ecosystem.

Git & GitHub: Version control and portfolio project publishing tools.

Repository Structure

The repository is organized in a simple and straightforward way:

mclaren_raw_telemetry.csv: The raw database used as the starting point (Bronze Layer).

Telemetria McLaren.py: The complete script containing all the Spark code for the pipeline (from Bronze to Gold).
