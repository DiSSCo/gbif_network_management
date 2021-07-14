#!/usr/bin/env python
# coding: utf-8


import pandas as pd
#import json
import requests
#from change_registry_using_API import *


def dataset_with_specimen_for_publishing_org(publishing_org_uuid,
                                                       step=1000):
    """
    Returns dataset containing specimens published by a given organization
    """
    offset = 0
    end_of_records = False
    nb_facet = 0
    datasetList = []
    base_request = "http://api.gbif.org/v1/occurrence/search?"
    base_request += "limit=0&facet=dataset_key"
    base_request += "&basis_of_record=basis_of_record=PRESERVED_SPECIMEN&basis_of_record=FOSSIL_SPECIMEN&basis_of_record=LIVING_SPECIMEN&basis_of_record=MATERIAL_SAMPLE"
    base_request += "&facetLimit=" + str(step)
    base_request += "&publishing_org=" + publishing_org_uuid
    
    while not end_of_records:
        response = requests.get(base_request + "&facetOffset=" + str(offset))
        if response.ok:
            response = response.json()
            
            nb_facet_in_page = 0
            if len(response["facets"]) > 0 :
                nb_facet_in_page = len(response["facets"][0]["counts"])
                datasetList += response["facets"][0]["counts"]
                
            # Increment page
            offset += step
            end_of_records = (nb_facet_in_page < step)
        else:
            print("ERROR", base_request + "&facetOffset=" + str(offset))
            end_of_records = True
    return [d['name'] for d in datasetList]


# Put here your GBIF credentials
login = "bla"
password = "bla"

api = "http://api.gbif.org/v1"
headers = {'Content-Type': 'application/json'}
# I used this excel sheet I got from Tim but here you could also use a list of org UUIDs
publisher_in_network = pd.read_excel("CETAF+DiSSCO institutions with GBIF Publisher ID.xlsx", sheet_name="Sheet1")
publisher_in_network = publisher_in_network[publisher_in_network.gbifPublisherID.notna()]
publisher_in_network = publisher_in_network.set_index("gbifPublisherID")


network_id = "17abcf75-2f1e-46dd-bf75-a5b21dd02655" # Network UUID

for uuid in publisher_in_network.index.tolist():
    # You might want to modify that condition if you are using a different spreasheet format
    if publisher_in_network.at[uuid, "disscoMember"] == "y":
        datasets_with_specimens = dataset_with_specimen_for_publishing_org(uuid)
        
        for ds in datasets_with_specimens:
            
            
            add_dataset = requests.post(api+"/network/"+network_id+"/constituents/"+ds,
                                        auth=(login, password),
                                        headers=headers)
            if add_dataset.ok:
                print(ds, "-> added")
            else:
                print(add_dataset)
           



