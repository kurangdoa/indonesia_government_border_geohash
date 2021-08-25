import pandas as pd
import os

path_base = os.getcwd()
path = os.path.join(path_base, 'results')
filesnames = os.listdir(path)
filesnames = [os.path.join(path,f) for f in filesnames if (f.lower().endswith(".csv"))]
# print(filesnames)

dfs = list()
for filename in filesnames:
     df = pd.read_csv(filename)
     df = df.loc[:,["geohash","remark","area_size"]]
     # df.to_csv(filename, index=False)
     dfs.append(df)

dfs = pd.concat(dfs)
dfs = dfs.sort_values(by=['geohash','area_size'], ascending=[True,False]).drop_duplicates('geohash', keep='first')
dfs["remark"] = dfs.remark.apply(str)

fname = "id_combine.csv"
fileresult = os.path.join(os.getcwd(), 'results', fname)
dfs = dfs.loc[:,["geohash","remark","area_size"]]
dfs.to_csv(fileresult, index=False)