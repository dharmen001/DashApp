import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import datetime
import ast
import dash_table
import httplib2
import pandas as pd

from dash_extensions import Download
from dash_extensions.snippets import send_data_frame, send_bytes
from Dash_App.app import app
from dash.dependencies import Input, Output, State
from oauth2client import GOOGLE_REVOKE_URI
from oauth2client import client, GOOGLE_TOKEN_URI

from apiclient import discovery

row1 = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Input(id="client_id",
                      type="text",
                      placeholder="Client ID",
                      style={'width': '300px'}, persistence=True,
                      persistence_type='memory'),
        ], style={'margin-top': 20, 'margin-left': -250, 'display': 'table-cell', 'verticalAlign': 'middle'})])])

row2 = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Input(id="profile_id",
                      type="text",
                      placeholder="Profile ID",
                      style={'width': '300px'}, persistence=True,
                      persistence_type='memory', ),
        ], style={'margin-top': 20, 'margin-left': -250, 'display': 'table-cell', 'verticalAlign': 'middle'})])])

row3 = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Input(id="refresh_token",
                      type="text",
                      placeholder="Refresh Token",
                      style={'width': '300px'}, persistence=True,
                      persistence_type='memory', ),
        ], style={'margin-top': 20, 'margin-left': -250, 'display': 'table-cell', 'verticalAlign': 'middle'})])])

row4 = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Input(id="client_secret",
                      type="text",
                      placeholder="Client Secret",
                      style={'width': '300px'}, persistence=True,
                      persistence_type='memory', ),
        ], style={'margin-top': 20, 'margin-left': -250, 'display': 'table-cell', 'verticalAlign': 'middle'})])])

row5 = html.Div([
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='dimensions',
                options=[{'label': i, 'value': i} for i in ['deviceCategory', 'segment', 'userType'
                                                            ]], persistence=True,
                persistence_type='memory',
                multi=True,
                style={'width': '300px'},
                placeholder='Dimensions')
        ], style={'margin-top': 20, 'margin-left': -250, 'display': 'table-cell', 'verticalAlign': 'middle'})])])

row6 = html.Div([
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='metrics',
                options=[{'label': i, 'value': i} for i in ['users', 'sessions', 'bounces']], persistence=True,
                persistence_type='memory',
                multi=True,
                style={'width': '300px'},
                placeholder='Metrics')
        ], style={'margin-top': 20, 'margin-left': -250, 'display': 'table-cell', 'verticalAlign': 'middle'})])])

row7 = html.Div([
    dbc.Row([dbc.Col([
        dcc.DatePickerSingle(
            id='start-date',
            placeholder="Start Date",
            min_date_allowed=datetime.datetime.now().strftime('2018-01-01'),
            max_date_allowed=datetime.datetime.today().date(),
            display_format='YYYY-MM-DD',
            style={'width': '300px'},
            persistence=True,
            persistence_type='memory',
        ),
    ], style={'margin-top': 20, 'margin-left': -250, 'display': 'table-cell', 'verticalAlign': 'middle'})])])

row8 = html.Div([
    dbc.Row([dbc.Col([
        dcc.DatePickerSingle(
            id='end-date',
            placeholder="End Date",
            min_date_allowed=datetime.datetime.now().strftime('2018-01-01'),
            max_date_allowed=datetime.datetime.today().date(),
            display_format='YYYY-MM-DD',
            persistence=True,
            persistence_type='memory',
        ),
    ], style={'margin-top': 20, 'margin-left': -250, 'display': 'table-cell', 'verticalAlign': 'middle'})])])

row9 = html.Div([
    dbc.Row([
        dbc.Col([
            html.Button(id='submit-button_segment', type='submit', children='Submit', style={'width': '300px'}),

        ], width={"order": "first"},
            style={'margin-top': 10, 'margin-left': -235}),
        dbc.Col([
            html.Div(id='output_div-ga_segment'),
        ])
    ])
])

row10 = html.Div([
    dbc.Row([
        dbc.Col([
            html.Button(id='submit-button', type='submit', children='Submit', style={'width': '300px'}),
        ], width={"order": "first"}, style={'margin-top': 20, 'margin-left': -235}),
        # dbc.Col([
        #     html.Div(id='output_div-ga'),
        # ])

        dbc.Col([
            html.Div(Download(id="download_ga"))
        ])
    ])
])

row11 = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Input(id="save-report",
                      type="text",
                      placeholder="Save Report as",
                      style={'width': '300px'}, persistence=True,
                      persistence_type='memory'),
        ], style={'margin-top': 20, 'margin-left': -250, 'display': 'table-cell', 'verticalAlign': 'middle'})])])

row12 = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Input(id="email-save-report",
                      type="text",
                      placeholder="Email ID",
                      style={'width': '300px'}, persistence=True,
                      persistence_type='memory'),
        ], style={'margin-top': 20, 'margin-left': -250, 'display': 'table-cell', 'verticalAlign': 'middle'})])])

row13 = html.Div([
    dbc.Row([
        dbc.Col([
            html.Button(id='submit-button-save', type='submit', children='Submit', style={'width': '300px'}),
        ], width={"order": "first"}, style={'margin-top': 20, 'margin-left': -235, 'display': 'table-cell',
                                            'verticalAlign': 'middle'}),
        dbc.Col([
            html.Div(id='output_div-save-ga'),
        ])
    ])
])

row14 = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Input(id="get-report",
                      type="text",
                      placeholder="Email ID Get Report",
                      style={'width': '300px'}, persistence=True,
                      persistence_type='memory'),
        ], style={'margin-top': 20, 'margin-left': -250, 'display': 'table-cell', 'verticalAlign': 'middle'})])])

row15 = html.Div([
    dbc.Row([
        dbc.Col([
            html.Button(id='submit-button-get', type='submit', children='Submit', style={'width': '300px'}),

        ], width={"order": "first"}, style={'margin-top': 20, 'margin-left': -235, 'display': 'table-cell',
                                            'verticalAlign': 'middle'}),
        dbc.Col([
            html.Div(id='output_div-get-ga'),
        ]),
    ])
])

row16 = html.Div([
    dbc.Row([dbc.Col([
        dcc.DatePickerSingle(
            id='start-date-email',
            placeholder="Start Date",
            min_date_allowed=datetime.datetime.now().strftime('2018-01-01'),
            max_date_allowed=datetime.datetime.today().date(),
            display_format='YYYY-MM-DD',
            style={'width': '300px'},
            persistence=True,
            persistence_type='memory',
        ),
    ], style={'margin-top': 20, 'margin-left': -235, 'display': 'table-cell', 'verticalAlign': 'middle'})
    ])])

row17 = html.Div([dbc.Row([dbc.Col([
    dcc.DatePickerSingle(
        id='end-date-email',
        placeholder="End Date",
        min_date_allowed=datetime.datetime.now().strftime('2018-01-01'),
        max_date_allowed=datetime.datetime.today().date(),
        display_format='YYYY-MM-DD',
        persistence=True,
        persistence_type='memory',
    ),
], style={'margin-top': 20, 'margin-left': -235, 'display': 'table-cell', 'verticalAlign': 'middle'})])])

row18 = html.Div([
    dbc.Row([
        dbc.Col([
            html.Button(id='submit-button-get-email', type='submit', children='Submit', style={'width': '300px'}),

        ], width={"order": "first"},
            style={'margin-top': 20, 'margin-left': -235, 'display': 'table-cell', 'verticalAlign': 'middle'}),
        dbc.Col([
            html.Div(Download(id='output_div-get-ga-email')),
        ]),
    ])
])

tab_2_layout = dbc.Container(children=[
    row1, row2, row3, row4, row9,
    row5, row6,
    row7, row8,
    row10, row11, row12, row13, row14, row15,
    # row16, row17,
    row18
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
                        style={'width': '300px'},
                        placeholder='Segment'),
                ], style={'margin-top': 80, 'margin-left': -315, 'display': 'table-cell', 'verticalAlign': 'middle'})
            ])])


@app.callback(Output('download_ga', 'data'),
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
        print(my_segment)
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

        dimensions_name = []
        for i in list_dim:
            list_item_dim = {'name': 'ga:{}'.format(i)}
            dimensions_name.append(list_item_dim)
        print(dimensions_name)
        metrics_name = []
        for j in list_metrics:
            list_item_metrics = {'expression': 'ga:{}'.format(j)}
            metrics_name.append(list_item_metrics)
        print(metrics_name)
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
            'dimensions': dimensions_name,
            'metrics': metrics_name,
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
        report_name = 'ga_{}.csv'.format(datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S"))
        return send_data_frame(dff.to_csv, report_name, index=False)


@app.callback(Output('output_div-save-ga', 'children'),
              [Input('submit-button-save', 'n_clicks')],
              [State('client_id', 'value'),
               State('profile_id', 'value'),
               State('refresh_token', 'value'),
               State('client_secret', 'value'),
               State('dimensions', 'value'),
               State('metrics', 'value'),
               State('segment', 'value'),
               State('start-date', 'date'),
               State('end-date', 'date'),
               State('save-report', 'value'),
               State('email-save-report', 'value')
               ],
              )
def ga_output(clicks, client_id, profile_id, refresh_token, client_secret, dimensions, metrics, segment,
              start_date, end_date, save_report, email_id):
    if clicks is not None:
        dff = pd.read_csv('query_ga.csv')
        my_ad_account = client_id
        my_app_id = profile_id
        my_access_token = refresh_token
        my_app_secret = client_secret
        my_dimensions = dimensions
        my_metrics = metrics
        my_segment = segment
        my_start_date = start_date
        my_end_date = end_date
        my_save_report = save_report
        my_email_report = email_id
        data = [my_save_report, my_email_report, my_ad_account, my_app_id, my_access_token, my_app_secret,
                my_dimensions, my_metrics, my_segment, my_start_date, my_end_date]
        df = pd.DataFrame([data], columns=['Report Name', 'Email ID', 'Ad Account id', 'App id', 'Access token',
                                           'App secret', 'Dimensions', 'Metrics', 'Segment',
                                           'Start date', 'End date'])
        df_new = df.append(dff)
        df_new.to_csv('query_ga.csv', index=False)
        html.Br()
        return "Your report has been saved as {} report and {} email ID".format(
            df['Report Name'].to_string(index=False),
            df['Email ID'].to_string(index=False))


@app.callback(Output('output_div-get-ga', 'children'),
              [Input('submit-button-get', 'n_clicks')],
              [State('get-report', 'value')
               ],
              )
def ga_output(clicks, email_id):
    if clicks is not None:
        df = pd.read_csv('query_ga.csv')
        my_email_id = email_id
        dff = df.loc[df['Email ID'].isin(['{}'.format(my_email_id)])]
        dff_new = dff[['Report Name', 'Email ID', 'Dimensions', 'Metrics', 'Segment', 'Start date', 'End date']]
        return html.Div([
            dbc.Row([
                dbc.Col([
                    dash_table.DataTable(
                        css=[{'selector': '.row',
                              'rule': 'margin: 0; white-space: inherit; overflow: inherit; text-overflow: inherit;'}],
                        id='table',
                        columns=[{"name": i, "id": i} for i in dff_new.columns],
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
                ], style={'margin-top': -900, 'display': 'inline-block', 'margin-left': 100, 'width': '100%'}),
            ]),
        ]), html.Div([
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        id='report_name',
                        options=[{'label': i, 'value': i} for i in dff['Report Name'].unique()],
                        persistence=True, persistence_type='memory',
                        multi=True,
                        style={'width': '300px'},
                        placeholder='Report Names'),
                ], style={'margin-top': 20, 'margin-left': -250, 'display': 'table-cell', 'verticalAlign': 'middle'})
            ]), ])


def make_report(i, my_start_date, my_end_date, my_email):
    df = pd.read_csv('query_ga.csv')
    df_new = df.loc[df['Report Name'].isin(['{}'.format(i)]) & df['Email ID'].isin(['{}'.format(my_email)])]
    my_client_id = df_new['Ad Account id'].iat[0]
    my_client_secret = df_new['App secret'].iat[0]
    my_refresh_token = df_new['Access token'].iat[0]
    my_dim = df_new['Dimensions'].iat[0]
    my_dimensions = ast.literal_eval(my_dim)
    my_met = df_new['Metrics'].iat[0]
    my_metrics = ast.literal_eval(my_met)
    my_seg = df_new['Segment'].iat[0]
    my_segment = ast.literal_eval(my_seg)
    my_profile_id = df_new['App id'].iat[0]
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

    dimensions_name = []
    for m in list_dim:
        list_item_dim = {'name': 'ga:{}'.format(m)}
        dimensions_name.append(list_item_dim)

    metrics_name = []
    for j in list_metrics:
        list_item_metrics = {'expression': 'ga:{}'.format(j)}
        metrics_name.append(list_item_metrics)

    segment_id = []
    for k in list_segment:
        p = k.split(':')[-1]
        list_item_segment = {'segmentId': 'gaid::{}'.format(p)}
        segment_id.append(list_item_segment)

    sample_request = {
        'viewId': my_profile_id,
        'dateRanges': {
            'startDate': my_start_date,
            'endDate': my_end_date
        },
        'dimensions': dimensions_name,
        'metrics': metrics_name,
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

    for q in range(len(lst2)):
        lst1.append(lst2[q]['name'])

    lst3 = response['reports'][0]['data']['rows']
    for r in range(len(lst3)):
        data_tuples.append(lst3[r]['dimensions'] + lst3[r]['metrics'][0]['values'])

    df = pd.DataFrame(data_tuples, columns=lst1)
    df['Report Name'] = i
    return df


@app.callback(Output('output_div-get-ga-email', 'data'),
              [Input('submit-button-get-email', 'n_clicks')],
              [State('start-date', 'date'),
               State('end-date', 'date'),
               State('report_name', 'value'),
               State('get-report', 'value')])
def ga_output(clicks, start_date, end_date, report_name, email):
    if clicks is not None:
        file_name = 'ga_{}.xlsx'.format(datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S"))
        my_report_name = report_name
        my_start_date = start_date
        my_end_date = end_date
        my_email = email

        def to_xlsx(bytes_io):
            xlsx_writer = pd.ExcelWriter(bytes_io, engine="xlsxwriter")
            for i in my_report_name:
                df = make_report(i, my_start_date, my_end_date, my_email)
                df.to_excel(xlsx_writer, index=False, sheet_name=i)
            xlsx_writer.save()

        return send_bytes(to_xlsx, file_name)
