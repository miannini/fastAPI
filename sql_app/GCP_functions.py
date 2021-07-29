# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 21:38:29 2021

@author: Marcelo
"""
#import os
import re
import numpy as np
#from google.cloud import storage
#from google.resumable_media.requests import Download, ChunkedDownload
#from pathlib import Path



#option GLOB
#import glob
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="secrets/data-science-proj-280908-e7130591b0d5.json" #D:/M4A/git_folder/Satellite_analysis_v2/

#option JSON - import directly storage_client in functions


#storage_client = storage.Client(project=project_id, credentials=storage_credentials)


# FUNCTIONS #

'''
### crear un bucket
def create_bucket(bucket_name):
    """Creates a new bucket."""
    # bucket_name = "your-new-bucket-name"
    #storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name)
    print("Bucket {} created".format(bucket.name))

#usar funcion
#bucket_name = 'satellite_storage'
#create_bucket(bucket_name)

'''

### subir archivos a un bucket
def upload_blob(storage_client, bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"
    #storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

#usar la funcion
#folder = 'Satellite/Data/Data/Database/-MAa0O5PMyE81I_AFC6E/'
#file = 'D:/M4A/git_folder/Data/cloud_masks_valid.png'
#destination_blob_name = folder + "new_folder/" + file.split('/')[-1]
#upload_blob('data-science-proj-280908',file,destination_blob_name)
    
'''

#subir folder y archivos

def upload_local_directory_to_gcs(local_path, bucket_name, gcs_path):
    assert os.path.isdir(local_path)
    for local_file in glob.glob(local_path + '/**'):
        print(local_file)        
        if not os.path.isfile(local_file):
            upload_local_directory_to_gcs(local_file, bucket_name, gcs_path + os.path.basename(local_file) +"/")
        else:
            remote_path = os.path.join(gcs_path, local_file[1 + len(local_path):]) #local_file[1 + len(local_path):]
            #storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(remote_path)
            blob.upload_from_filename(local_file)

#upload list of files
#folder = 'D:/M4A/git_folder/Data/Output_Images/boye_output/'
#gcs_path = 'new_folder/'
#bucket_name = 'satellite_storage'
#upload_local_directory_to_gcs(folder, bucket_name, 'new_folder2/')



### listar buckets
def list_buckets():
    """Lists all buckets."""
    #storage_client = storage.Client()
    buckets = storage_client.list_buckets()
    lista = []
    for bucket in buckets:
        print(bucket.name)
        lista.append(bucket.name)
    return lista
#usar funcion
#list_buckets()
'''

### list prefixes
'''def list_prefixes(self, prefix=None):
    iterator = self.list_blobs(delimiter='/', prefix=prefix)
    list(iterator)  # Necessary to populate iterator.prefixes
    for p in iterator.prefixes:
        yield p
'''
'''
### extract prefixes
def list_gcs_directories(bucket, prefix):
    # from https://github.com/GoogleCloudPlatform/google-cloud-python/issues/920
    #storage_client = storage.Client()
    iterator = storage_client.list_blobs(bucket, prefix=prefix, delimiter='/')
    prefixes = set()
    for page in iterator.pages:
        #print (page, page.prefixes)
        prefixes.update(page.prefixes)
    return prefixes

'''
### listar objetos de un bucket
def list_all_blobs(storage_client, bucket_name, prefix=None, delimiter=None, lote=None, prop=None, mindate=0, maxdate=np.inf): #prefix is initial route, delimiter is '/', lote, prop
    #cred
    """Lists all the blobs in the bucket."""
    # bucket_name = "your-bucket-name"
    lista = []
    #storage_client = storage.Client()
    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name, prefix=prefix,delimiter=delimiter)
    for blob in blobs:
        if int(blob.name.split('/')[-1][0:8]) >= mindate and int(blob.name.split('/')[-1][0:8]) <= maxdate:
            if lote is not None: #si ha restriccion de lote
                if prop is not None: #tambien hay restriccion de propiedad
                    if re.search(r'_'+re.escape(lote)+r'_'+re.escape(prop),blob.name):
                        lista.append(blob.name)
                else:               #no hay restriccion de propiedad
                    if re.search(r'_'+re.escape(lote)+r'_',blob.name):
                        lista.append(blob.name)
            else:                   #no hay restriccion de lote
                if prop is not None:    #si hay restriccion de propiedad
                    if re.search(r'_'+re.escape(prop),blob.name):
                        lista.append(blob.name)
                else:               #no hay restriccion de lote ni de propiedad
                    lista.append(blob.name)   
    return lista

#usar la funcion
#folder = 'Data/PNG_Images/ID_CLIENTE-'
#list_all_blobs('data-science-proj-280908',prefix=folder,delimiter='/')





### abrir objeto:
def open_blob(storage_client, bucket_name, source_blob_name): #destination_file_name
    """open a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # source_blob_name = "storage-object-name"
    #storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    with blob.open('rb') as f:
        return f.read()

### abrir objetos:
def open_multi_blob(storage_client, bucket_name, source_blob_folder): #destination_file_name
    """open a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # source_blob_name = "storage-object-name"
    #storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    for source_blob_name in source_blob_folder:
        blob = bucket.blob(source_blob_name)
        with blob.open('rb') as f:
            return f.read()


#def stream_blob(storage_client, url, bucket_name, source_blob_name):
    

#GCP_functions.download_blob(buck, datos[0], os.path.basename(datos[0].split('/')[-1]))
#usar funcion
#folder = 'Colombia/mpos/'
#objetos = list(list_all_blobs('shapefiles-storage',prefix=folder,delimiter='/'))
#destination = shape_folder + folder #shapefolder from sat_processing.py
#Path(destination).mkdir(parents=True, exist_ok=True)
#for n in objetos:
#    download_blob('shapefiles-storage', n, destination + n.split('/')[-1])


'''
### Copiar Objetos 
def copy_blob(bucket_name, blob_name, destination_bucket_name, destination_blob_name):
    """Copies a blob from one bucket to another with a new name."""
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"
    # destination_bucket_name = "destination-bucket-name"
    # destination_blob_name = "destination-object-name"

    #storage_client = storage.Client()
    source_bucket = storage_client.bucket(bucket_name)
    source_blob = source_bucket.blob(blob_name)
    destination_bucket = storage_client.bucket(destination_bucket_name)

    blob_copy = source_bucket.copy_blob(
        source_blob, destination_bucket, destination_blob_name
    )

    print(
        "Blob {} in bucket {} copied to blob {} in bucket {}.".format(
            source_blob.name,
            source_bucket.name,
            blob_copy.name,
            destination_bucket.name,
        )
    )


### Eliminar Objetos
def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"

    #storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()

    print("Blob {} deleted.".format(blob_name))

### listar labels de un bucket
def get_bucket_labels(bucket_name):
    """Prints out a bucket's labels."""
    # bucket_name = 'your-bucket-name'
    #storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    labels = bucket.labels
    print(labels)
    return labels
'''
#usar funcion
#get_bucket_labels(bucket_name)
    
#posible run gsutil gunctions from python
'''
import subprocess
subprocess.run(["ls", "-l"],capture_output=True)

subprocess.run(["gsutil", "cp", "-r", "gs://data-science-proj-280908/Satellite/Data/Data/Database/-MAa0O5PMyE81I_AFC6E test"])
'''
#to try later