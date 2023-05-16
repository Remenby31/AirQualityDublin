# Background
Air quality is a major public health and urban ecological issue. In Dublin, the capital of Ireland, the
situation is of concern due to the constant increase in population and road traffic. This innovative
project aims to collect data on air quality in Dublin using DPD delivery vehicles as a means of
measurement. Sensors installed on these vehicles record air quality data as they travel around the city
each day, making it possible to track changes in air quality in different neighborhoods and at different
times of the day.
# Project Overview
The project will proceed in several key stages: Data Collection, Analysis and Mapping and finally
Handling missing values.
### Data Collection
The sensors in question are responsible for collecting the following information, which we will need to
process:
• Air quality indicators (pm2.5 and pm10)
• GPS coordinates
• Date and time of data collection
### Analysis and Mapping
By focusing on the air quality indicators (pm2.5 and pm10) and combining this information with GPS
coordinates, dates and times, we have the opportunity to create a dynamic picture of the environmental
situation in Dublin. Our first step is to develop a map that illustrates this data, providing a clear view
of air quality at different times of the day.
### Handling missing values
However, there will be missing values in our dataset, and this is the heart of our project. We will
implement various techniques and models to predict these missing values, exploring the correlation
between air quality and other sources of information, such as meteorological data. By estimating these
values, we will build a more complete and reliable dataset for analysis, revealing the unknowns and
correlations behind air quality variations.
# Long-Term Goals
Our quest to understand the factors influencing these variations will lead us to a better understanding
of the Dublin environment and to the discovery of valuable tools for environmental policy and urban
planning decisions. Ultimately, beyond simply collecting data, this project will allow us to contribute
to building a healthier future for Ireland’s capital city and its residents.

# How to use it

1. Copy the data in the foder *DataDublin*/*name_data*
2. Run XAMPP and start Apache
3. Open the file *siteJavaScript.html* in a web browser