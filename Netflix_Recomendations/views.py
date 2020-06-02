
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from Netflix_Recomendations.Netflix_Recommend_code import recommendations
import json


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__,
                    external_stylesheets=external_stylesheets)


app.layout = html.Div([
    html.H1("Welcome to Netflix Recommendations!",
            style={"textalign": "center"}),

    html.Hr(),

    html.Div([

        dcc.Input(id="request", placeholder="Enter Movie Name",value='',
                  style={"width": "60%"}),


        html.Button(id="submit", children="Recommend",n_clicks=0),
        # dcc.Textarea(
        #     id='textarea-output',
        #     value='Textarea content initialized\nwith multiple lines of text',
        #     style={'width': '100%', 'height': 300},
        # )
        html.H4(id="textarea-output")

    ], style={"textalign": 'center', "width": "80%"})

])
# ******* callbacks*****************


@app.callback(Output("textarea-output", "children"), [Input("submit", "n_clicks")], [State("request", "value")])
def action(n_clicks,val):
    return json.dumps(recommendations(val))
