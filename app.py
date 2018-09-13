import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd

from queries import  query_datasets, query_dimensions, query_measures, get_endpoints_list
from uiutilities import custom_checklists
from queries2 import query_endpoint, load_queries, pretty_results

# ----- Main layout
#load queries with queries2
queries={}
queries_dir="sparql/"
for queries in load_queries(queries_dir):
    queries
	
app = dash.Dash()
server = app.server

# ----- sTYLING
""" app.css.append_css({
    "external_url": "https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"
    }) """

app.layout = html.Div(
    className="container",
    children = [

    html.H1("T E S S E R A C T"),

    html.H2("Exploring DataCubes"),

    html.Div(
        children = [
            html.H3("Select an endpoint"),
            dcc.Dropdown(
                id = "endpoints-list",
                options = get_endpoints_list(),
                value = ""
            ),
        ]
    ),

    html.Span(),

    html.Div(
        children = [
            html.H3("DataCube selection"),
            html.Div(id = "blip",
            children = [dcc.Dropdown(
                id = "datasets-list",
                options = [],
                value = ""
            )]),
            html.Div(id = "target")
        ]
    ),


    html.Div(
        id = "table",
        children = [
            html.H3("Dimensions and measures selection"),
            html.Div(
                className = "col s6", 
                children = [
                    html.Label('Dimensions'),
                    dcc.Checklist(
                        options=[],
                        id='dimensions',
                        values=[],
                        labelStyle={'display': 'block'}
                    )
                ]
            ),
            html.Div(
                className = "col s6", 
                children = [
                    html.Label('Measures'),
                    dcc.Checklist(
                        options=[],
                        id='measures',
                        values=[],
                        labelStyle={'display': 'block'}
                    )
                ]
            ),
        ]
    ),

    html.H4(id = "selection-info"),

    html.Button(
        "Run query",
        id = "run",
        style = {"display" : "none"}
    )
    
])

# ----- Callbacks
@app.callback(
    Output(component_id = "datasets-list", component_property = "options"),
    [ Input(component_id = "endpoints-list", component_property = "value") ]
)
def test(input_value):
    return query_datasets(input_value)

@app.callback(
    Output(component_id = "dimensions", component_property = "options"),
    [Input(component_id = "datasets-list", component_property = "value")],
    [State("endpoints-list", "value")]
)
def get_dimensions(dataset_uri, endpoint):
    dim_data = query_dimensions(endpoint, dataset_uri)
    dim_rows = dim_data[1]

    if dataset_uri == "":
        return []
    else:
        return dim_rows

@app.callback(
    Output(component_id = "measures", component_property = "options"),
    [Input(component_id = "datasets-list", component_property = "value")],
    [State("endpoints-list", "value")]
)
def get_measures(dataset_uri, endpoint):
    measures_data = query_measures(endpoint, dataset_uri)
    measures_rows = measures_data[1]

    if dataset_uri == "":
        return []
    else:
        return measures_rows

@app.callback(
    Output(component_id = "selection-info", component_property = "children"),
    [ 
        Input(component_id = "dimensions", component_property = "values"),
        Input(component_id = "measures", component_property = "values") 
    ]
)
def selection_info(dim_info, measures_info):
    if len(dim_info) == 2 and len(measures_info) == 1:
        return html.P("You can execute your query")
    else:
        return html.P("You must select 2 dimensions and 1 measure")

@app.callback(
    Output(component_id = "run", component_property = "style"),
    [ 
        Input(component_id = "dimensions", component_property = "values"), 
        Input(component_id = "measures", component_property = "values") 
    ]
)
def button_display(dim_info, measures_info):
    if len(dim_info) == 2 and len(measures_info) == 1:
        return {"display" : "block"}
    else:
        return {"display": "none"}


if __name__ == '__main__':
    app.run_server()