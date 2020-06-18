import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from Dash_App.app import app

tab_4_layout = html.Div([
    html.Div([
        html.Div([
            # html.Label('Dimensions', style={'font-weight': 'bold', 'margin-left': 60}),
            dcc.Dropdown(
                id='dimensions',
                options=[{'label': i, 'value': i} for i in ['Campaign', 'Placement', 'Creative']],
                multi=True,
                placeholder='Dimensions',
                style={'width': '200px', 'margin-top': 10, 'height': '40px'}
            ),
            html.Div(id='page-4-dimensions')
        ]),
        html.Div([
            # html.Label('Metrics', style={'font-weight': 'bold', 'margin-left': 60}),
            dcc.Dropdown(
                id='metrics',
                options=[{'label': i, 'value': i} for i in ['Impressions', 'Clicks', 'Conversions']],
                multi=True,
                placeholder='Metrics',
                style={'width': '200px', 'margin-top': 10, 'margin-left': 5, 'height': '40px'}
            ),
            html.Div(id='page-4-metrics')
        ]),
        html.Div([
            dcc.DatePickerRange(
                id='start-date-end-date',
                start_date_placeholder_text='Start Date',
                end_date_placeholder_text='End Date',
                min_date_allowed=datetime.datetime.now().strftime('2018-01-01'),
                max_date_allowed=datetime.datetime.today().date(),
                display_format='YYYY-MM-DD',
                style={'width': '500px', 'margin-top': 10, 'margin-left': 15}
            ),
            html.Div(id='page-4-start-date-end-date')
        ]),
    ], style={'display': 'flex'}),html.A('Download Data', id='download-link', download="rawdata.csv", href="",
                                          target="_blank")
])
