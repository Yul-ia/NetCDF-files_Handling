
# Analysis of CMAP and NCEP/DOE Reanalysis II

- **Global and East Asia `Precipitation` Analysis using CMAP and NCEP_R2**
- **Global and East Asia `Air Temperature`, `Surface Pressure`, and `Wind Speed` Analysis using NCEP_R2**

---

### Data source

**CMAP** | https://www.psl.noaa.gov/data/gridded/data.cmap.html

- Average Monthly Rate of Precipitation

**NCEP_R2** | [https://psl.noaa.gov/data/gridded/data.ncep.reanalysis2.html](https://psl.noaa.gov/data/gridded/data.ncep.reanalysis2.html)

- Precipitation Rate at Surface
- Forecast of Surface Pressure
- Forecast of U-wind and V-wind at 10 m
- Forecast of Air Temperature at 2 m

For this dataset, the following were analyzed for the global, East Asia ( East Sea, Yellow Sea, and East China Sea ) regions:

**Time series**

- Monthly average
    - Trend (over 10 years, 30years) , p-value
    Trend model : scipy.stats.linregress
- Climatic average
    - Standard deviation
- Anomaly

**Map projection**

- Monthly average
- Climatic average
- Anomaly

—

**Acknowledgements**

This data analysis was conducted as part of an internship at the [Ocean Climate Prediction Center(OCPC)](https://www.ocpc.kr/) of the [Korea Institute of Ocean Science and Technology](https://www.kiost.ac.kr/eng.do).

I’m deeply grateful to the entire team at the OCPC for their invaluable guidance and unwavering support throughout this process.
