## **git file**
https://github.com/kurangdoa/indonesia_government_border_geohash.git

## **Description**
Create geohash from government border to make the process of spatial join easier and faster. Initial work was done for Kelurahan level where it was broken down to geohash7. Geohash7 is used because the size will fit most of kelurahan. For more reference on geohash refer to this link https://www.movable-type.co.uk/scripts/geohash.html

## **Algorithm**
For converting polygon to geohashit will rely heavily on **polygon-geohasher** package which could be seen in this link https://pypi.org/project/polygon-geohasher/. After the conversion, the duplication of geohashes that belong to two polygon will be removed by comparing its size from one another.

## **Code**
The code is divided into two, **government_border_geohash.py** where the coverter from government border file to geohashes is conducted and **geohash_remove_duplicate.py** where the duplicate removal is conducted.

## **How To**
After downloading the data to the same folder as this readme.md simply run the code in your local computer. To download the data, follow this link https://drive.google.com/drive/folders/1kBfdHcif8sfdWz3NoHhQSaOw62LlOw7t?usp=sharing
- **kmz** folder that contains the government border data that were already converted into kmz.
- **shp** folder that contains the governmnet border as shape file (taken from https://data.humdata.org/dataset/84a1d98a-790b-4d66-9d14-bbfa48500802/resource/53625e84-203d-4331-b3eb-01e6e8344413/download/idn_adm_bps_20200401_shp.zip)
- **results** folder that contains all the result. 

Note: Open to be used for all