import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

from queries import  query_datasets, query_dimensions, query_measures



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
            html.H3("DataCube selection"),
            dcc.Dropdown(
                id = "domain-list",
                options = query_datasets(),
                value = ""
            ),

            html.Div(id = "target")
        ]
    ),
    
    html.Div(
        id = "table")
    
])

# ----- Callbacks
@app.callback(
    Output(component_id='target', component_property='children'),
    [Input(component_id='domain-list', component_property='value')]
)
def update_output_div(input_value):
    return f"You selected the {input_value} domain"

@app.callback(
    Output(component_id = "table", component_property = "children"),
    [Input(component_id = "domain-list", component_property = "value")]
)
def get_dimensions_or_measures(input_value):
    # TODO use Salim code for multiple selection
    dim_data = query_dimensions()
    dim_rows = dim_data[1]
    measures_data = query_measures()
    measures_row = measures_data[1]

    if input_value == "":
        html.Div("")
    else:
        return html.Div(
            className = "row", 
            children = [
                html.H3("Dimensions and measures selection"),
                html.Div(
                    className = "col s6", 
                    children = [
                        html.Label('Dimensions'),
                        dcc.Checklist(
                            options=dim_rows,
                            id="dimensions",
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
                            options=measures_row,
                            id="measures",
                            values=[],
                            labelStyle={'display': 'block'}
                        )
                    ]
                )
            ]
        )

if __name__ == '__main__':
    app.run_server()