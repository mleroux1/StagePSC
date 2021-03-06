#!/usr/bin/env python

## Calcul des volumes de PSC (STS, NAT, ICE) à partir des volumes d'ai froid (TSTS, TNAT, TICE) calculés par la fonction VolT_IPSL_2015_2100.py

# Importation des modules
import xarray as xr
import numpy as np

# Ouverture du fichiers netcdf contenant les volumes de températures froides.
ds = xr.open_mfdataset('/home/mleroux/qsub/IPSL-CM6/VolT_IPSL_2015_2100.nc')  

time=np.arange(0, 1032, 1)

latbin=[-79.85915 , -78.59155 , -77.323944, -76.056335, -74.788734, -73.521126,
       -72.253525, -70.985916, -69.71831 , -68.45071 , -67.1831  , -65.91549 ,
       -64.64789 , -63.380283, -62.112675, -60.84507 , -59.577465, -58.30986 ,
       -57.042255, -55.774647, -54.507042, -53.239437, -51.971832, -50.704224]

longbin=[  0. ,   2.5,   5. ,   7.5,  10. ,  12.5,  15. ,  17.5,  20. ,  22.5,
        25. ,  27.5,  30. ,  32.5,  35. ,  37.5,  40. ,  42.5,  45. ,  47.5,
        50. ,  52.5,  55. ,  57.5,  60. ,  62.5,  65. ,  67.5,  70. ,  72.5,
        75. ,  77.5,  80. ,  82.5,  85. ,  87.5,  90. ,  92.5,  95. ,  97.5,
       100. , 102.5, 105. , 107.5, 110. , 112.5, 115. , 117.5, 120. , 122.5,
       125. , 127.5, 130. , 132.5, 135. , 137.5, 140. , 142.5, 145. , 147.5,
       150. , 152.5, 155. , 157.5, 160. , 162.5, 165. , 167.5, 170. , 172.5,
       175. , 177.5, 180. , 182.5, 185. , 187.5, 190. , 192.5, 195. , 197.5,
       200. , 202.5, 205. , 207.5, 210. , 212.5, 215. , 217.5, 220. , 222.5,
       225. , 227.5, 230. , 232.5, 235. , 237.5, 240. , 242.5, 245. , 247.5,
       250. , 252.5, 255. , 257.5, 260. , 262.5, 265. , 267.5, 270. , 272.5,
       275. , 277.5, 280. , 282.5, 285. , 287.5, 290. , 292.5, 295. , 297.5,
       300. , 302.5, 305. , 307.5, 310. , 312.5, 315. , 317.5, 320. , 322.5,
       325. , 327.5, 330. , 332.5, 335. , 337.5, 340. , 342.5, 345. , 347.5,
       350. , 352.5, 355. , 357.5]

VpscSTS= np.zeros([1032, 24, 144])
VpscNAT= np.zeros([1032, 24, 144])
VpscICE= np.zeros([1032, 24, 144])

for k in range(1032):
    print(k)
    for i in range(24):
        for j in range(144):
            
            VTsts=ds.VTsts[k,i,j].values                # VTsts, VTnat, VTice, volumes d'air froid seuils.
            VpscSTS[k,i,j]= 0.0478*VTsts                # Formules (VpscSTS, VpscNAT, VpscICE) obtenues par régression polynomiale sur un scatterplot reliant volumes d'air froid et volumes de PSC issus des observations CALIPSO.
                                                                                               
            VTnat=ds.VTnat[k,i,j].values
            VpscNAT[k,i,j]= 8.239e-19*(VTnat**4) - 5.383e-13*(VTnat**3) + 1.072e-07*(VTnat**2) + 0.1808*VTnat
            
            VTice=ds.VTice[k,i,j].values
            VpscICE[k,i,j]= 3.855e-08*(VTice**2) + 0.1082*(VTice)
       
# Création des fichiers netcdf contenant les volumes de PSC           
STS = xr.DataArray(VpscSTS, dims=('time', 'lat', 'long'), coords={'time':time, 'lat':latbin, 'long':longbin})
NAT = xr.DataArray(VpscNAT, dims=('time', 'lat', 'long'), coords={'time':time, 'lat':latbin, 'long':longbin})
ICE = xr.DataArray(VpscICE, dims=('time', 'lat', 'long'), coords={'time':time, 'lat':latbin, 'long':longbin})

data = xr.Dataset({'vol_STS':STS,'vol_NAT':NAT,'vol_ICE':ICE})
data.to_netcdf('VolPSC_modele_IPSL_2015_2100.nc')
