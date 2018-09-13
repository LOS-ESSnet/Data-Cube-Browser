import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd

from queries import  query_datasets, query_dimensions, query_measures, get_endpoints_list
from uiutilities import custom_checklists
from queries2 import query_endpoint, load_queries, pretty_results

# ----- Main layout
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
        id = "table")
    
])

# ----- Callbacks
@app.callback(
    Output(component_id = "datasets-list", component_property = "options"),
    [ Input(component_id = "endpoints-list", component_property = "value") ]
)
def test(input_value):
    return query_datasets(input_value)

@app.callback(
    Output(component_id = "table", component_property = "children"),
    [Input(component_id = "datasets-list", component_property = "value")],
    [State("endpoints-list", "value")]
)
def get_dimensions_or_measures(dataset_uri, endpoint):
    # TODO use Salim code for multiple selection
    dim_data = query_dimensions(endpoint, dataset_uri)
    dim_rows = dim_data[1]
    measures_data = query_measures(endpoint, dataset_uri)
    measures_rows = measures_data[1]

    if dataset_uri == "":
        html.Div("")
    else:
        return html.Div(
            className = "row", 
            children = [
                html.H3("Dimensions and measures selection"),
                custom_checklists("Dimensions", dim_rows),
                custom_checklists("Measures", measures_rows)
            ]
        )

if __name__ == '__main__':
    app.run_server()