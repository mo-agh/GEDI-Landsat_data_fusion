import numpy as np
import matplotlib.pyplot as plt
import rasterio

path = r'D:\university\UMD\courses\Fall 2023\geog 642, biogeoraphy\project\new data/'

with rasterio.open(path + '20210130.tif', driver='GTiff') as src:
    mask = src.read()[:7]
    mask = np.prod(~np.isnan(mask), axis=0).astype('bool')
    
with rasterio.open(path + '20210130_enhanced_uint16.tif', driver='GTiff') as src:
    profile = src.profile
    Landsat = src.read()[:7].astype('float')/(2**16-1)
    Landsat[:, ~mask] = np.nan
    
    

Landsat_NDVI = (Landsat[5-1] - Landsat[4-1]) / (Landsat[5-1] + Landsat[4-1] + 1e-5)
# Landsat_EVI = 2.5* ((Landsat[5-1] - Landsat[4-1]) / (Landsat[5-1] + 6*Landsat[4-1] -7.5*Landsat[2-1]+1 + 1e-5))
Landsat_NBR = (Landsat[5-1] - Landsat[7-1]) / (Landsat[5-1] + Landsat[7-1] + 1e-5)
Landsat_NBR2 = (Landsat[6-1] - Landsat[7-1]) / (Landsat[6-1] + Landsat[7-1] + 1e-5)
Landsat_NDMI = (Landsat[5-1] - Landsat[6-1]) / (Landsat[5-1] + Landsat[6-1] + 1e-5)
TCT_Wet = (Landsat[1-1]*0.1511+Landsat[2-1]*0.1973+Landsat[3-1]*0.3283+Landsat[4-1]*0.3407+Landsat[5-1]*(-0.7117)+Landsat[6-1]*(-0.4559))
TCT_Green = (Landsat[1-1]*(-0.2941)+Landsat[2-1]*(-0.243)+Landsat[3-1]*(-0.5424)+Landsat[4-1]*0.7276+Landsat[5-1]*0.0713+Landsat[6-1]*(-0.1608))
TCT_Bright = (Landsat[1-1]*0.3029+Landsat[2-1]*0.2786+Landsat[3-1]*0.4733+Landsat[4-1]*0.5599+Landsat[5-1]*0.508+Landsat[6-1]*0.1872)

# plt.imshow(Landsat.transpose(1, 2, 0)[:, :, 3:0:-1], cmap='gray')
# plt.imshow(TCT_Bright, cmap='gray')
# print(np.min(TCT_Bright[mask]), np.max(TCT_Bright[mask]))

final = np.concatenate([Landsat, 
                       np.expand_dims(Landsat_NDVI, axis=0), 
                       np.expand_dims(Landsat_NBR, axis=0), 
                       np.expand_dims(Landsat_NBR2, axis=0), 
                       np.expand_dims(Landsat_NDMI, axis=0), 
                       np.expand_dims(TCT_Wet, axis=0), 
                       np.expand_dims(TCT_Green, axis=0), 
                       np.expand_dims(TCT_Bright, axis=0)], 
                       axis=0)

# plt.imshow(final.transpose(1, 2, 0)[:, :, 3:0:-1])
# plt.imshow(final[11], cmap='gray')

profile1 = profile.copy()
profile1.update(dtype=np.float32, 
                count=len(final), 
                compress='lzw')
    
with rasterio.open(path + '20210130_processed.tif', 'w', **profile1) as dst:
        dst.write(final)