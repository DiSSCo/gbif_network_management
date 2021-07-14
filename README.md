# gbif_network_management
repo for code to manage the DiSSCo network in GBIF

The repo contains a Python script to add datasets from dataproviders IDs read from the excel sheet also in the repo, to the DiSSCo network in GBIF. Only datasets are added that contain records with basis_of_record=PRESERVED_SPECIMEN, FOSSIL_SPECIMEN, LIVING_SPECIMEN or MATERIAL_SAMPLE. To run the script you need to set a GBIF username and password in the script with appropriate rights to make the changes.
