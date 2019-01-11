# Data Cube Browser

Python application built during hackathon to browse RDF Data cube

# Specifications

First:
* easy to use
* graphical interface
* webapp, browser (not something that you should download)

Thematic search?

Index of Dataset / Catalog

Compare some datasets, are there interesting to compare?

Information needed:
* measures
* dimensions
* code lists

Access by:
* measure or dimension
* item of a codelist
* linked datasets?

Main purpose of the user:
* See how the datasets look like to be able to define the usefull comparaisons he can make without knowing sparql

# Usage

Install Dash (https://plot.ly/products/dash/)and required components
pip install dash dash_core_components dash_html_components

Install SPARQLWrapper for queries and pandas for displaying results
pip install SPARQLWrapper pandas

Run application:
python app.py

Navigate to http://127.0.0.1:8050/