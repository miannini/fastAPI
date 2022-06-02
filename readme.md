### FastAPI development used for Herd-management App

- api_folder / Contains all python required files to run the API;
- Requirements: List of all required libraries to run the API in Python;


# API developed using fastAPI for Python
to Run it locally, execute:
- uvicorn api_folder.main:app --reload
- Don't try to debug or run with pycharm buttons, only use Pycharm terminal


to explore locally the content, open the browser and got to:
- http://127.0.0.1:8000/docs

to deploy in GCP:
- push the changes to GitHub
- Pull the changes in GCP, fastAPI folder
- gcloud app deploy app.yaml
  - when prompted, authorize and then type "y" to deploy the service

* To deploy Prod and Test Versions use: \
  ***gcloud app deploy app.yaml test.yaml***