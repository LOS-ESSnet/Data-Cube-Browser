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
app.css.append_css({
    "external_url": "https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"
    })

app.layout = html.Div(
    className="container",
    children = [

    html.H1("T E S S E R A C T"),

    html.H2("Exploring DataCubes"),

    dcc.Dropdown(
        id = "domain-list",
        options = query_datasets(),
        value = "tourism"
    ),

    html.Div(id = "target"),

    html.H2("I want to take a look at :"), 

    dcc.RadioItems(
        id = "select-dim-or-meas",
        options=[
            {'label': 'Dimensions', 'value': 'dimensions'},
            {'label': 'Measures', 'value': 'measures'}
        ],
        value=''
        ),
    
    html.Div(id = "table")
    
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
    [Input(component_id = "select-dim-or-meas", component_property = "value")]
)
def get_dimensions_or_measures(input_value):
    if (input_value == "dimensions"):
        # TODO use Salim code for multiple selection
        df = query_dimensions()
        print(df)
        return html.Div(    
            className = "row", 
            children = [
                html.Div(
                    className = "col s6", 
                    children = [
                        html.Label('Dimensions'),
                        dcc.Checklist(
                            options=[
                                {'label': 'Dimension 1', 'value': 'd1'},
                                {'label': 'Dimension 2', 'value': 'd2'},
                                {'label': 'Dimension 3', 'value': 'd3'}
                            ],
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
                            options=[
                                {'label': 'Measures 1', 'value': 'm1'},
                                {'label': 'Measures 2', 'value': 'm2'},
                                {'label': 'Measures 3', 'value': 'm3'}
                            ],
                            id="measures",
                            values=[],
                            labelStyle={'display': 'block'}
                        )
                    ]
                )
            ]
        )
    elif (input_value == "measures"):
        return html.Table([html.Tr([html.Td("test")]) for row in range(10)])
    else:
        return html.Div("No dimensions or measures chosen")


if __name__ == '__main__':
    app.run_server()