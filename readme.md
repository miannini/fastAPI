### FastAPI development used for Herd-management App

- api_folder / Contains all python required files to run the API;
- Requirements: List of all required libraries to run the API in Python;


# API developed using fastAPI for Python
to Run it, execute:
- uvicorn api_folder.main:app --reload

to explore locally the content, open the browser and got to:
- http://127.0.0.1:8000/docs

to deploy in GCP:
- push the changes ti GitHub
- Pull the changes in GCP, fastAPI folder
- gcloud app deploy app.yaml
  - when prompted, authorize and then type "y" to deploy the service
* To deploy Prod and Test Versions use:
  ***gcloud app deploy app.yaml test.yaml***


  **Table of Contents**

[TOCM]

[TOC]

#H1 header
##H2 header
###H3 header
####H4 header
#####H5 header
######H6 header
#Heading 1 link [Heading link](https://github.com/pandao/editor.md "Heading link")
##Heading 2 link [Heading link](https://github.com/pandao/editor.md "Heading link")
###Heading 3 link [Heading link](https://github.com/pandao/editor.md "Heading link")
####Heading 4 link [Heading link](https://github.com/pandao/editor.md "Heading link") Heading link [Heading link](https://github.com/pandao/editor.md "Heading link")
#####Heading 5 link [Heading link](https://github.com/pandao/editor.md "Heading link")
######Heading 6 link [Heading link](https://github.com/pandao/editor.md "Heading link")

##Headers (Underline)

H1 Header (Underline)
=============

H2 Header (Underline)
-------------




###End