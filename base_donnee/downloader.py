""" module which provides tools for automatically download databases"""


import io
import zipfile
import requests
import os, inspect
import pandas

URL={
"ref_lig":"https://data.iledefrance-mobilites.fr/explore/dataset/referentiel-des-lignes/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B",
"gtfs_key":"https://data.iledefrance-mobilites.fr/explore/dataset/offre-horaires-tc-gtfs-idf/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B",
"trace_fer":"https://data.iledefrance-mobilites.fr/explore/dataset/traces-du-reseau-ferre-idf/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B",
"trace_bus":"https://data.iledefrance-mobilites.fr/explore/dataset/bus_lignes/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B",
"reflex_key":"https://data.iledefrance-mobilites.fr/explore/dataset/referentiel-arret-tc-idf/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B",
}

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

FOLDERS = {
"GTFS":currentdir+"/datas/Gtfs",
"REFLEX":currentdir+"/datas/Reflex",
"TRACE":currentdir+"/datas/Trace",
"REFERENCIEL":currentdir+"/datas/Referenciel" }


ADRESS={"agency":FOLDERS["GTFS"]+"/agency.txt",
"calendar_dates":FOLDERS["GTFS"]+"/calendar_dates.txt",
"calendar":FOLDERS["GTFS"]+"/calendar.txt",
"routes":FOLDERS["GTFS"]+"/routes.txt",
"stop_extensions":FOLDERS["GTFS"]+"/stop_extensions.txt",
"stop_times":FOLDERS["GTFS"]+"/stop_times.txt",
"stops":FOLDERS["GTFS"]+"/stops.txt",
"transfers":FOLDERS["GTFS"]+"/transfers.txt",
"trips":FOLDERS["GTFS"]+"/trips.txt",
"reflex":FOLDERS["REFLEX"]+"/reflex.csv",
"trace_fer":FOLDERS["TRACE"]+"/traces-du-reseau-ferre-idf.csv",
"trace_bus":FOLDERS["TRACE"]+"/bus_lignes.csv",
"ref_lig":FOLDERS["REFERENCIEL"]+"/referentiel-des-lignes.csv" }




def download_zip(zip_file_url,path):
    """ download a file at url zip_url_file and unzip it in path"""
    print("Downloading files")
    r = requests.get(zip_file_url, stream=True)
    if r.ok:
        print("Download finished succesfully")
        print("unzipping files in", path)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(path)
        print("Download process finished")
        return True
    print("an unexpected error occured, please check the downloading url",zip_file_url)
    return False

def download_csv(csv_file_url,path):
    """ download a file at url csv_url_file and save it in path"""
    myfile = requests.get(csv_file_url)
    if myfile.ok :
        f = open(path,'wb')
        f.write(myfile.content)
        f.close()
        return True
    print("an unexpected error occured, please check the downloading url",csv_file_url)
    return False

def download_and_display_gtfs_pdf(df):
    try :
        download_csv(df[1][2],currentdir+"/gtfs_notes.pdf")
        os.startfile(currentdir+"/gtfs_notes.pdf")
    except :
        return 0

def get_download_file_from_csv_key(csv_file_url,bool_gtfs,bool_reflex):
    bool = download_csv(csv_file_url,"temp.csv")
    if bool :
        df = pandas.read_csv("temp.csv",sep=";", header=None , engine='python')
        os.remove("temp.csv")
    else :
        return False,""
    if bool_gtfs and bool_reflex :
        print("base_donnee.downloader.get_download_file_from_csv_key : only one of bool_gtfs and bool_reflex must be set equals to True")
    if bool_gtfs:
        download_and_display_gtfs_pdf(df)
        return True,df[1][1] #[col][row]
    if bool_reflex:
        return True,df[2][2]
    print("base_donnee.downloader.get_download_file_from_csv_key : only one of bool_gtfs and bool_reflex must be set equals to True")

def download_file(key):
    if key in ["agency","calendar_dates","calendar","routes","stop_extensions","stop_times","stops","transfers","trips","gtfs"] :
        bool1,url = get_download_file_from_csv_key(csv_file_url = URL["gtfs_key"],bool_gtfs=True,bool_reflex=False)
        if bool1:
            bool2 = download_zip(url,FOLDERS["GTFS"])
    elif key in ["trace_fer","trace_bus","ref_lig"]:
        bool1 = download_csv(URL[key],ADRESS[key])
        bool2 = True
    elif key=="reflex" :
        bool1,url = get_download_file_from_csv_key(csv_file_url = URL["reflex_key"],bool_gtfs=False,bool_reflex=True)
        if bool1:
            bool2 = download_csv(url,ADRESS[key])
    else :
        bool1 = False
        bool2 = False

    return bool1 and bool2

def path_checks ():
    for key in FOLDERS :
        if os.path.exists(FOLDERS[key])==False:
            os.makedirs(FOLDERS[key])



def download_check (bool_force_update):
    global_succes = True
    path_checks()
    for key in bool_force_update :
        if bool_force_update[key]:
            print("DOWNLOADING ",key)
            succes = download_file(key)
            global_succes = succes and global_succes

    for key in ADRESS :
        bool = os.path.exists(ADRESS[key])
        if bool==False :
            print("DOWNLOADING ",key)
            succes = download_file(key)
            global_succes = succes and global_succes

    return global_succes



def force_download(gtfs,ref_lig,trace,reflex):
    return {
    "gtfs" : gtfs,
    "reflex" : reflex,
    "trace_fer" : trace,
    "trace_bus" : trace,
    "ref_lig" : ref_lig}
