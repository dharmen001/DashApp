import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import datetime
import dash_table

from Dash_App.app import app
import pandas as pd

row1 = html.Div(
    [
        dbc.Row([
            dbc.Col([
                dbc.Input(id="client_id",
                          type="text",
                          placeholder="Client ID",
                          style={'width': '150px'}),
            ]),

            dbc.Col([
                dbc.Input(id="profile_id",
                          type="text",
                          placeholder="Profile ID",
                          style={'width': '150px'}),
            ]),
            dbc.Col([
                dbc.Input(id="refresh_token",
                          type="text",
                          style={'width': '150px'},
                          placeholder="Refresh Token")
            ]),
            dbc.Col([
                dbc.Input(id="client_secret",
                          type="text",
                          style={'width': '150px'},
                          placeholder="Client Secret")
            ]),

            dbc.Col([
                dcc.Dropdown(
                    id='dimensions',
                    options=[{'label': i, 'value': i} for i in ['Campaign', 'Placement', 'Creative']],
                    multi=True,
                    style={'width': '150px'},
                    placeholder='Dimensions')
            ]),

            dbc.Col([
                dcc.Dropdown(
                    id='metrics',
                    options=[{'label': i, 'value': i} for i in ['account_currency',
                                                                'account_id',
                                                                'account_name',
                                                                ]],
                    multi=True,
                    style={'width': '150px'},
                    placeholder='Metrics')
            ]),
        ], align="center"),
    ], style={'margin-top': 20, 'margin-left': -90}
)

row2 = html.Div([
    dbc.Row([
        # dbc.Col([
        #     dcc.Dropdown(
        #         id='breakdown',
        #         options=[{'label': i, 'value': i} for i in ['ad_format_asset', 'age', 'body_asset',
        #                                                     'call_to_action_asset', 'country',
        #                                                     ]], disabled=True,
        #         multi=True,
        #         style={'width': '250px'},
        #         placeholder='Breakdown'),
        # ]),

        dbc.Col([
            dcc.DatePickerSingle(
                id='start-date',
                placeholder="Start Date",
                min_date_allowed=datetime.datetime.now().strftime('2018-01-01'),
                max_date_allowed=datetime.datetime.today().date(),
                display_format='YYYY-MM-DD',
                style={'width': '150px', 'margin-left': 180}
            ),
        ]),
        dbc.Col([
            dcc.DatePickerSingle(
                id='end-date',
                placeholder="End Date",
                min_date_allowed=datetime.datetime.now().strftime('2018-01-01'),
                max_date_allowed=datetime.datetime.today().date(),
                display_format='YYYY-MM-DD',
                style={'width': '150px', 'margin-left': 50}
            )]),
    ])
])

row3 = html.Div([
    dbc.Row([
        dbc.Col([
            html.Button(id='submit-button', type='submit', children='Submit', style={'width': '150px', 'margin-top': 5,
                                                                                     'margin-left': 370}),

        ], width={"order": "first"}),
        dbc.Col([
            html.Div(id='output_div-dcm'),
        ])
    ])
])

tab_3_layout = dbc.Container(children=[
    row1,
    html.Br(),
    row2,
    html.Br(),
    row3,
    html.Br(),

]
)


@app.callback(Output('output_div-dcm', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('client_id', 'value'),
               State('profile_id', 'value'),
               State('refresh_token', 'value'),
               State('client_secret', 'value'),
               State('dimensions', 'value'),
               State('metrics', 'value'),
               State('start-date', 'date'),
               State('end-date', 'date'),
               ],
              )
def dcm_output(clicks, client_id, profile_id, refresh_token, client_secret, dimensions, metrics, start_date, end_date):
    if clicks is not None:
        my_client_id = client_id
        my_profile_id = profile_id
        my_refresh_token = refresh_token
        my_client_secret = client_secret
        my_dimensions = dimensions
        my_metrics = metrics
        my_start_date = start_date
        my_end_date = end_date

        async_job = ''
        df = pd.DataFrame(async_job)
        dff = df['']
        html.Br()
        return html.Div([
            dash_table.DataTable(
                css=[{'selector': '.row',
                      'rule': 'margin: 0; white-space: inherit; overflow: inherit; text-overflow: inherit;'}],
                id='table',
                columns=[{"name": i, "id": i} for i in dff.columns],
                data=dff.to_dict("rows"),
                export_format="csv",
                style_cell={"fontFamily": "Arial", "size": 10, 'textAlign': 'left',
                            'width': '{}%'.format(len(dff.columns)), 'textOverflow': 'ellipsis', 'overflow': 'hidden'},

                style_table={'maxHeight': '200px', 'overflowY': 'scroll', 'maxWidth': '1500px', 'overflowX': 'scroll'},
                style_header={'backgroundColor': '#ffd480', 'color': 'white', 'height': '10', 'width': '10',
                              'fontWeight': 'bold'},
                style_data={'whiteSpace': 'auto', 'height': 'auto', 'width': 'auto'},
                tooltip_data=[
                    {
                        column: {'value': str(value), 'type': 'markdown'}
                        for column, value in row.items()
                    } for row in dff.to_dict('rows')
                ],
                tooltip_duration=None
            ),
        ], style={'margin-top': 30, 'display': 'inline-block', 'margin-left': 20, 'width': '100%'})
