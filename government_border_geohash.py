from zipfile import ZipFile
import os
from lxml import html
from shapely import geometry
import pandas as pd
import re
from polygon_geohasher.polygon_geohasher import polygon_to_geohashes, geohashes_to_polygon, geohash_to_polygon
from shapely.ops import cascaded_union
from matplotlib import pyplot as plt
from shapely.ops import transform
import pyproj
from shapely.validation import make_valid
from tqdm import tqdm
# import multiprocessing as mp
import multiprocess as mp

## custom for paralel processing not working ##

# def geohash_intersect_custom(geoh, polygon=polygon, area_size=area_size, k=k):
    
#     from polygon_geohasher.polygon_geohasher import geohash_to_polygon
#     from shapely.ops import transform
#     from shapely.validation import make_valid
#     import pyproj

#     wgs84 = pyproj.CRS('EPSG:4326')
#     utm = pyproj.CRS('EPSG:32618')
#     project = pyproj.Transformer.from_crs(wgs84, utm, always_xy=True).transform

#     if k == 1: 
#         testgeopol = geohash_to_polygon(geoh)
#         testgeopol_compile = testgeopol
#         try:
#             testgeopol_intersect = testgeopol.intersection(make_valid(polygon))
#         except:
#             pass
#     else :
#         testgeopol = geohash_to_polygon(geoh)
#         try:
#             testgeopol_intersect = testgeopol.intersection(make_valid(polygon))
#         except:
#             pass
#     area_size.append(transform(project, testgeopol_intersect).area)
#     k=k+1
#     return area_size

# pool = mp.Pool(mp.cpu_count())

# from customf import *


### take the filelist ###

path_base = os.getcwd()
# path_base = 'D:/rhyando/work/project/tmp_government_border_geohash/'
foldername = os.path.join(path_base, 'kmz')
listfiles = [s for s in os.listdir(foldername) if s.endswith('.kmz')]
# listfiles = ['id_sulsel.kmz','id_bangkabelitung.kmz', 'id_banten.kmz', 'id_bengkulu.kmz', 'id_diy.kmz', 'id_gorontalo.kmz', 'id_jakarta.kmz', 'id_jambi.kmz', 'id_jawabarat.kmz', 'id_jawatengah.kmz', 'id_jawatimur.kmz', 'id_kalbar.kmz', 'id_kalsel.kmz', 'id_kalteng.kmz', 'id_kaltim.kmz', 'id_kalut.kmz', 'id_kepulauanriau.kmz', 'id_lampung.kmz', 'id_maluku.kmz', 'id_malukuutara.kmz', 'id_ntb.kmz', 'id_riau.kmz', 'id_sulbar.kmz', 'id_sulteng.kmz', 'id_sultenggara.kmz', 'id_sulut.kmz', 'id_sumbar.kmz', 'id_sumsel.kmz', 'id_sumut.kmz']
listfiles = [eachfile.split(sep = '.')[0] for eachfile in listfiles]
print(listfiles)
# listfiles = ['id_aceh']
# listfiles = ['id_bali']

### start to loop per file ###

for eachfile in listfiles:
    print(eachfile)
    filename = os.path.join(path_base, 'kmz', eachfile+".kmz")
    kmz = ZipFile(filename, 'r')
    kml = kmz.open('doc.kml', 'r').read()
    doc = html.fromstring(kml)

    ### for government kml ###

    wgs84 = pyproj.CRS('EPSG:4326')
    utm = pyproj.CRS('EPSG:32618')
    project = pyproj.Transformer.from_crs(wgs84, utm, always_xy=True).transform

    j=1
    compol = []

    for place in tqdm(doc.cssselect('Folder Placemark')):
        test_name = place[1][0][3].text_content()
        # print (test_name)
        test = place[2].text_content()
        test = re.sub('\s+',' ',test)
        test = test.split(sep=',0 ')
        test = [x.replace(" ","") for x in test]
        test = [x for x in test if len(x)>0]
        test_list = []
        for itertest in test:
            splited = itertest.split(sep=',')
            x0 = splited[0]
            y0 = splited[1]
            test_list.append([float(x0),float(y0)])
        test_list = [test_list]

        i=1

        for x in test_list:

            list_c=[]
            for y in x:
                #print(y)
                #print("\n")  
                combine = (y[0], y[1])
                list_c.append(combine)
            #print(list_c)
            #print("\n")
            polygon = geometry.Polygon(list_c)
            compiled = polygon_to_geohashes(polygon, 7, False) #outer
            #compiled = polygon_to_geohashes(polygon, 8)
            compiled = pd.DataFrame(list(compiled),columns=["geohash"])[0:]
            compiled["remark"] = test_name

            # part derived area #
            
            k=1
            area_size = []
            # area_size = pool.map(geohash_intersect_custom, [geoh for geoh in compiled['geohash']])
            for a,b in zip(compiled['geohash'],compiled['remark']):
                if k == 1: 
                    testgeopol = geohash_to_polygon(a)
                    testgeopol_compile = testgeopol
                    try:
                        testgeopol_intersect = testgeopol.intersection(make_valid(polygon))
                    except:
                        pass
                else :
                    testgeopol = geohash_to_polygon(a)
                    try:
                        testgeopol_intersect = testgeopol.intersection(make_valid(polygon))
                    except:
                        pass
                # plt.plot(*testgeopol_intersect.exterior.xy)
                # print(y)
                area_size.append(transform(project, testgeopol_intersect).area)
                k=k+1
                # print(k)
            compiled['area_size'] = area_size
            
            if i == 1:
                compiled_df = compiled
            else:
                compiled_df = pd.concat([compiled_df,compiled], ignore_index=True)
            i=i+1
            #print(compiled)
        if j == 1:
            compol = compiled_df
        else:
            compol = pd.concat([compiled_df,compol], ignore_index=True)
        # print(j)
        j=j+1
        # break

    df = compol

    path = os.path.join(path_base, 'shp', 'adm4_info.csv')
    pol = pd.read_csv(path, index_col=False)
    pol = pol.loc[:,["ADM4_PCODE","Shape_Area"]]
    pol.columns = ["remark","poly_size"]
    df = pd.merge(df,pol,on="remark")

    # df = df.sort_values(by=['geohash','poly_size','area_size'], ascending=[True,True,False]).drop_duplicates('geohash', keep='first')
    df = df.sort_values(by=['geohash','area_size'], ascending=[True,False]).drop_duplicates('geohash', keep='first')
    df["remark"] = df.remark.apply(str)
    df = df.loc[:,['geohash','remark','area_size']]

    fileresult = os.path.join(path_base, 'results',eachfile+ ".csv")
    df.to_csv(fileresult, index=False)
    # plt.plot(*polygon.exterior.xy)
