# COMP90024 - Cluster and Cloud Computing

## University of Melbourne

### Project: Cluster and Cloud Computing (CCC)

This repository contains the project work for COMP90024 at the University of Melbourne. The project involves developing a cloud-based application with the following components:

- **Frontend**: Jupyter Notebook
- **Backend**: Fission functions
- **Orchestration**: Kubernetes (K8s)
- **Database**: Elasticsearch

Description of repo contents:
- **frontend**: Jupyter notebooks of codes for visualization
- **Backend**: YAML specifications, and files and codes used to deploy functions in fission including functions for insertion, analysis and query
- **database**: Codes used to create indexes in elasticsearch
- **docs**: Instructions of APIs of our functions
- **data**: Our used raw data and codes of preprocessing the data
- **test**: Files and codes used for test

Instructions:
To use our frontend client, python packages of 'json', 'requests', 'folium', 'pandas', 'seaborn', 'matplotlib' need to be installed. Then the connection from local computer to the Kubernetes cluster need to be built. After that each cell in the jupyter notebooks need to be run in sequence. 