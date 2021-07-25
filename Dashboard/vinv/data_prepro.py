# Importing Libraries
import pandas as pd
import numpy as np

df_rsrp = pd.read_csv("assets/RSRP.csv")
df_tv = pd.read_csv("assets/TrafficVolume.csv")

# Slicing the string as the only used time are Hours and Minutes
df_rsrp['Timestamp'] = df_rsrp.Timestamp.str.slice(0, 16)
df_tv['Timestamp'] = df_tv.Timestamp.str.slice(0, 16)

# Changing from string to date time format for both datasets
df_rsrp['Timestamp'] = pd.to_datetime(df_rsrp['Timestamp'], format='%Y-%m-%d %H:%M')
df_tv['Timestamp'] = pd.to_datetime(df_tv['Timestamp'], format='%Y-%m-%d %H:%M', errors='coerce')

# Replacing the NaNs with Saudi Arabia after the Analysis done
df_rsrp = df_rsrp.replace(np.nan, 'Saudi Arabia', regex=True)

# Dropping the NaNs record as they are only 80
df_tv.dropna(inplace=True)

# Dropping the records of the RSRP dataset of which are larger than -40 as they are outliers
indexNames = df_rsrp[df_rsrp['RSRP'] > -40].index
df_rsrp.drop(indexNames, inplace=True)

# Dataa of 4G only
indexNames = df_tv[df_tv['RadioNetworkGeneration'] == '3G'].index
df_tv.drop(indexNames , inplace=True)

indexNames = df_rsrp[df_rsrp['RadioNetworkGeneration'] == '3G'].index
df_rsrp.drop(indexNames , inplace=True)

# Sorting the Data according to the Timestamp
df_tv.sort_values(by='Timestamp', inplace=True)
df_rsrp.sort_values(by='Timestamp', inplace=True)

# Resetting the index of both Dataset
df_rsrp.reset_index(inplace=True, drop=True)
df_tv.reset_index(inplace=True, drop=True)

# Returning only data with the Downlink
df_down = df_tv[df_tv['TrafficDirection'] == 'Downlink']
df_down.reset_index(inplace=True, drop=True)
da = df_down[df_down["RadioOperatorName"] == 'Operator A']
db = df_down[df_down["RadioOperatorName"] == 'Operator B']
dc = df_down[df_down["RadioOperatorName"] == 'Operator C']

#dz = df_tv.groupby(["LocationLatitude", "LocationLongitude", "RadioOperatorName"]).count()
#print(df_rsrp['RadioOperatorName'].unique())
#print(df_rsrp['RSRP'].max())
#print(df_rsrp['RSRP'].min())

def return_rsrp_unique(operator):
    dz = df_rsrp.groupby(["LocationLatitude", "LocationLongitude", "RadioOperatorName", "RSRP"]).count()
    dz = dz[['Timestamp']]
    dz.rename(columns={'Timestamp': 'Count'}, inplace=True)
    dz.reset_index(inplace=True)
    OP = dz[dz["RadioOperatorName"] == operator]
    return OP

def return_slice(n,agg):
    length = len(df_rsrp)
    n = round(length * (n/100))
    dz = df_rsrp[:n]
    if agg == 'max':
        dz = dz.groupby(["DeviceManufacturer", "RadioOperatorName"]).max()
    elif agg == 'min':
        dz = dz.groupby(["DeviceManufacturer", "RadioOperatorName"]).min()
    elif agg == 'avg':
        dz = dz.groupby(["DeviceManufacturer", "RadioOperatorName"]).mean()
    if agg == '90':
        dz = dz.groupby(["DeviceManufacturer", "RadioOperatorName"]).max()
        dz['RSRP'] = dz['RSRP']*0.9
    else:
        dz = dz.groupby(["DeviceManufacturer", "RadioOperatorName"]).mean()
        dz = dz[['RSRP']]
    dz = dz[['RSRP']]
    dz['RSRP'] = dz['RSRP'] * -1
    dz.reset_index('DeviceManufacturer', inplace=True)
    dz["DeviceManufacturer"] = dz["DeviceManufacturer"].str.upper()
    sams = dz[dz["DeviceManufacturer"] == "SAMSUNG"]
    hmd = dz[dz["DeviceManufacturer"] == "HMD GLOBAL"]
    huwa = dz[dz["DeviceManufacturer"] == "HUAWEI"]
    lge = dz[dz["DeviceManufacturer"] == "LGE"]
    htc = dz[dz["DeviceManufacturer"] == "HTC"]
    vivo = dz[dz["DeviceManufacturer"] == "VIVO"]
    real = dz[dz["DeviceManufacturer"] == "REALME"]
    zte = dz[dz["DeviceManufacturer"] == "ZTE"]
    oppo = dz[dz["DeviceManufacturer"] == "OPPO"]
    xia = dz[dz["DeviceManufacturer"] == "XIAOMI"]
    one = dz[dz["DeviceManufacturer"] == "ONEPLUS"]
    sony = dz[dz["DeviceManufacturer"] == "SONY"]
    moto = dz[dz["DeviceManufacturer"] == "MOTOROLA"]
    pana = dz[dz["DeviceManufacturer"] == "PANASONIC"]
    tcl = dz[dz["DeviceManufacturer"] == "TCL"]
    qmobile = dz[dz["DeviceManufacturer"] == "QMOBILE"]
    obi = dz[dz["DeviceManufacturer"] == "OBI"]
    sharp = dz[dz["DeviceManufacturer"] == "SHARP"]
    leco = dz[dz["DeviceManufacturer"] == "LECO"]
    return sams, hmd, huwa, lge, htc, vivo, real, zte, oppo, xia, one, sony, moto, pana, tcl, qmobile, obi, sharp, leco
