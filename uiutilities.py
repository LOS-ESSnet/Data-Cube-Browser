import dash_core_components as dcc
import dash_html_components as html

def custom_checklists(label, rows):
    return html.Div(
                    className = "col s6", 
                    children = [
                        html.Label(label),
                        dcc.Checklist(
                            options=rows,
                            id=label.lower(),
                            values=[],
                            labelStyle={'display': 'block'}
                        )
                    ]
                )