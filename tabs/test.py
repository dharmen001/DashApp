import dash
import dash_bootstrap_components as dbc

external_stylesheets = dbc.themes.BOOTSTRAP
app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                external_stylesheets=[external_stylesheets], serve_locally=False, prevent_initial_callbacks=True)
app.title = "Data"
server = app.server
app.config['suppress_callback_exceptions'] = True

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import datetime
import dash_table


import pandas as pd

df = pd.read_csv('C:/sapientrepo/Dash_App/query.csv')

row1 = html.Div(
    [dcc.Store(id='local', storage_type='local'),
     dbc.Row([
         dbc.Col([
             dbc.Input(id="ad_account_id",
                       type="text",
                       placeholder="Account ID",
                       style={'width': '150px'}, persistence=True,
                       persistence_type='memory'),
         ])])])

row6 = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Input(id="get-report",
                      type="text",
                      placeholder="Get Report",
                      style={'width': '150px', 'margin-top': 20, 'margin-left': 10}, persistence=True,
                      persistence_type='memory'),
        ])])])

row7 = html.Div([
    dbc.Row([
        dbc.Col([
            html.Button(id='submit-button-get', type='submit', children='Submit', style={'width': '150px',
                                                                                         'margin-top': 20,
                                                                                         'margin-left': 10}),

        ], width={"order": "first"}),
        dbc.Col([
            html.Div(id='output_div-get'),
        ])
    ])
])

app.layout = dbc.Container(children=[
    row1,
    html.Br(),
    row6,
    html.Br(),
    row7])


@app.callback([Output('output_div-get', 'children'), Output('ad_account_id', 'value')],
              [Input('submit-button-get', 'n_clicks')],
              [State('get-report', 'value')], )
def facebook_output(clicks, get_report):
    if clicks is not None:
        my_report = get_report
        new_df = df.loc[df['Report Name'] == my_report]
        ad_account_id = new_df.iloc[:, 1]
        a_id = list(ad_account_id)
        return '', a_id


if __name__ == '__main__':
    app.run_server(debug=True)
