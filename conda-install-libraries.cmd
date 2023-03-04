ECHO off
call conda create --name ultima python==3.9
call conda activate ultima
call conda install matplotlib==3.5.3  pandas==1.5.2  Shapely==1.8.4 ^
Fiona==1.8.13.post1 pyproj==2.6.1.post1 scipy==1.9.3 netCDF4==1.5.7 ^
xarray==2022.11.0 joblib==1.1.1 geopandas==0.9.0 ttkthemes==3.2.2
call pip install motionless==1.3.3
call pip install salem==0.3.8
PAUSE