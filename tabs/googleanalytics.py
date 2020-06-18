import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import datetime
import dash_table
import httplib2
import pandas as pd

from Dash_App.app import app
from dash.dependencies import Input, Output, State
from oauth2client import GOOGLE_REVOKE_URI
from oauth2client import client, GOOGLE_TOKEN_URI

from apiclient import discovery

row1 = html.Div(
    [
        dbc.Row([
            dbc.Col([
                dbc.Input(id="client_id",
                          type="text",
                          placeholder="Client ID",
                          style={'width': '150px'}, persistence=True,
                          persistence_type='memory'),
            ]),

            dbc.Col([
                dbc.Input(id="profile_id",
                          type="text",
                          placeholder="Profile ID",
                          style={'width': '150px'}, persistence=True,
                          persistence_type='memory'),
            ]),
            dbc.Col([
                dbc.Input(id="refresh_token",
                          type="text",
                          style={'width': '150px'},
                          placeholder="Refresh Token", persistence=True,
                          persistence_type='memory')
            ]),
            dbc.Col([
                dbc.Input(id="client_secret",
                          type="text",
                          style={'width': '150px'},
                          placeholder="Client Secret", persistence=True,
                          persistence_type='memory')
            ]),

            dbc.Col([
                dcc.Dropdown(
                    id='dimensions',
                    options=[{'label': i, 'value': i} for i in ['deviceCategory', 'segment']],
                    multi=True,
                    style={'width': '150px'},
                    placeholder='Dimensions', persistence=True,
                    persistence_type='memory')
            ]),

            dbc.Col([
                dcc.Dropdown(
                    id='metrics',
                    options=[{'label': i, 'value': i} for i in ['sessions', 'users']],
                    multi=True,
                    style={'width': '150px'},
                    placeholder='Metrics', persistence=True,
                    persistence_type='memory', )
            ]),
        ], align="center"),
    ], style={'margin-top': 20, 'margin-left': -90}
)

row2 = html.Div([
    dbc.Row([
        dbc.Col([
            dcc.DatePickerSingle(
                id='start-date',
                placeholder="Start Date",
                min_date_allowed=datetime.datetime.now().strftime('2018-01-01'),
                max_date_allowed=datetime.datetime.today().date(),
                display_format='YYYY-MM-DD',
                style={'width': '150px', 'margin-left': 180}, persistence=True,
                persistence_type='memory',
            ),
        ]),
        dbc.Col([
            dcc.DatePickerSingle(
                id='end-date',
                placeholder="End Date",
                min_date_allowed=datetime.datetime.now().strftime('2018-01-01'),
                max_date_allowed=datetime.datetime.today().date(),
                display_format='YYYY-MM-DD',
                style={'width': '150px', 'margin-left': 50}, persistence=True,
                persistence_type='memory',
            )]),
    ])
])

row3 = html.Div([
    dbc.Row([
        dbc.Col([
            html.Button(id='submit-button', type='submit', children='Submit',
                        style={'width': '150px', 'margin-top': 5,
                               'margin-left': 370}),

        ], width={"order": "first"}),
        dbc.Col([
            html.Div(id='output_div-ga'),
        ])
    ])
])

row5 = html.Div([
    dbc.Row([
        dbc.Col([
            html.Button(id='submit-button_segment', type='submit', children='Submit',
                        style={'width': '150px', 'margin-top': 10,
                               'margin-left': 370}),

        ], width={"order": "first"}),
        dbc.Col([
            html.Div(id='output_div-ga_segment'),
        ])
    ])
])

tab_2_layout = dbc.Container(children=[
    row1, row5,
    html.Br(),
    row2,
    html.Br(),
    row3,
    html.Br(),
]
)


@app.callback(Output('output_div-ga_segment', 'children'),
              [Input('submit-button_segment', 'n_clicks')],
              [State('client_id', 'value'),
               State('refresh_token', 'value'),
               State('client_secret', 'value'),
               ],
              )
def ga_output(clicks, client_id, refresh_token, client_secret):
    if clicks is not None:
        my_client_id = client_id
        my_refresh_token = refresh_token
        my_client_secret = client_secret

        credentials = client.OAuth2Credentials(
            access_token=None,  # set access_token to None since we use a refresh token
            client_id=my_client_id,
            client_secret=my_client_secret,
            refresh_token=my_refresh_token,
            token_expiry=None,
            token_uri=GOOGLE_TOKEN_URI,
            user_agent=None,
            revoke_uri=GOOGLE_REVOKE_URI)

        credentials.refresh(httplib2.Http())  # refresh the access token (optional)

        http = credentials.authorize(httplib2.Http())  # apply the credentials
        service_v3 = discovery.build('analytics', 'v3', http=http)
        segments = service_v3.management().segments().list().execute()
        df = pd.DataFrame(segments['items'])

        df = df[['name', 'id']]
        df['name_id'] = df.name.astype(str).str.cat(df.id.astype(str), sep=':')
        return html.Div([
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        id='segment',
                        options=[{'label': i, 'value': i} for i in df['name_id'].unique()],
                        persistence=True, persistence_type='memory',
                        multi=True,
                        style={'width': '250px', 'margin-left': -250, 'margin-top': 10},
                        placeholder='Segment'),
                ]), ]), ])


@app.callback(Output('output_div-ga', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('client_id', 'value'),
               State('profile_id', 'value'),
               State('refresh_token', 'value'),
               State('client_secret', 'value'),
               State('dimensions', 'value'),
               State('metrics', 'value'),
               State('segment', 'value'),
               State('start-date', 'date'),
               State('end-date', 'date'),
               ],
              )
def ga_output(clicks, client_id, profile_id, refresh_token, client_secret, dimensions, metrics, segments,
              start_date, end_date):
    if clicks is not None:
        my_client_id = client_id
        my_profile_id = profile_id
        my_refresh_token = refresh_token
        my_client_secret = client_secret
        my_dimensions = dimensions
        my_metrics = metrics
        my_segment = segments
        my_start_date = start_date
        my_end_date = end_date

        credentials = client.OAuth2Credentials(
            access_token=None,  # set access_token to None since we use a refresh token
            client_id=my_client_id,
            client_secret=my_client_secret,
            refresh_token=my_refresh_token,
            token_expiry=None,
            token_uri=GOOGLE_TOKEN_URI,
            user_agent=None,
            revoke_uri=GOOGLE_REVOKE_URI)

        credentials.refresh(httplib2.Http())  # refresh the access token (optional)

        http = credentials.authorize(httplib2.Http())  # apply the credentials

        service = discovery.build('analyticsreporting', 'v4', http=http)

        list_dim = my_dimensions
        list_metrics = my_metrics
        list_segment = my_segment

        dimensions_ = []
        for i in list_dim:
            list_item_dim = {'name': 'ga:{}'.format(i)}
            dimensions_.append(list_item_dim)

        metrics_ = []
        for j in list_metrics:
            list_item_metrics = {'expression': 'ga:{}'.format(j)}
            metrics_.append(list_item_metrics)

        segment_id = []
        for k in list_segment:
            j = k.split(':')[-1]
            list_item_segment = {'segmentId': 'gaid::{}'.format(j)}
            segment_id.append(list_item_segment)
        print(segment_id)
        sample_request = {
            'viewId': my_profile_id,
            'dateRanges': {
                'startDate': my_start_date,
                'endDate': my_end_date
            },
            'dimensions': dimensions_,
            'metrics': metrics_,
            'segments': segment_id,
            "samplingLevel": "LARGE",
        }

        response = service.reports().batchGet(
            body={
                'reportRequests': sample_request
            }).execute()

        data_tuples = []
        lst1 = response['reports'][0]['columnHeader']['dimensions']
        lst2 = response['reports'][0]['columnHeader']['metricHeader']['metricHeaderEntries']

        for i in range(len(lst2)):
            lst1.append(lst2[i]['name'])

        lst3 = response['reports'][0]['data']['rows']
        for i in range(len(lst3)):
            data_tuples.append(lst3[i]['dimensions'] + lst3[i]['metrics'][0]['values'])

        df = pd.DataFrame(data_tuples, columns=lst1)
        dff = df
        html.Br()
        return html.Div([dcc.Store('memory'),
                         dash_table.DataTable(
                             css=[{'selector': '.row',
                                   'rule': 'margin: 0; white-space: inherit; overflow: inherit; text-overflow: inherit;'}],
                             id='table',
                             columns=[{"name": i, "id": i} for i in dff.columns],
                             data=dff.to_dict("rows"), persistence=True, persistence_type='memory',
                             export_format="csv",
                             style_cell={"fontFamily": "Arial", "size": 10, 'textAlign': 'left',
                                         'width': '{}%'.format(len(dff.columns)), 'textOverflow': 'ellipsis',
                                         'overflow': 'hidden'},

                             style_table={'maxHeight': '200px', 'overflowY': 'scroll', 'maxWidth': '1500px',
                                          'overflowX': 'scroll'},
                             style_header={'backgroundColor': '#ffd480', 'color': 'white', 'height': '10',
                                           'width': '10',
                                           'fontWeight': 'bold'},
                             style_data={'whiteSpace': 'auto', 'height': 'auto', 'width': 'auto'},
                             tooltip_data=[
                                 {
                                     column: {'value': str(value), 'type': 'markdown'}
                                     for column, value in row.items()
                                 } for row in dff.to_dict('rows')
                             ],
                             tooltip_duration=None,
                         ),
                         ], style={'margin-top': 60, 'display': 'inline-block', 'margin-left': -250, 'width': '100%'})
