import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import datetime
import dash_table

from Dash_App.app import app
import pandas as pd

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.user import User
from facebook_business.adobjects.adaccount import AdAccount

row1 = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Input(id="ad_account_id",
                      type="text",
                      placeholder="Account ID",
                      style={'width': '300px'}, persistence=True,
                      persistence_type='memory'),
        ], style={'margin-top': 20, 'margin-left': -250, 'display': 'table-cell', 'verticalAlign': 'middle'})])])

row2 = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Input(id="app_id",
                      type="text",
                      placeholder="App ID",
                      style={'width': '300px'}, persistence=True,
                      persistence_type='memory', ),
        ], style={'margin-top': 20, 'margin-left': -250, 'display': 'table-cell', 'verticalAlign': 'middle'})])])

row3 = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Input(id="access_token",
                      type="text",
                      placeholder="Access Token",
                      style={'width': '300px'}, persistence=True,
                      persistence_type='memory', ),
        ], style={'margin-top': 20, 'margin-left': -250, 'display': 'table-cell', 'verticalAlign': 'middle'})])])

row4 = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Input(id="app_secret",
                      type="text",
                      placeholder="App Secret",
                      style={'width': '300px'}, persistence=True,
                      persistence_type='memory', ),
        ], style={'margin-top': 20, 'margin-left': -250, 'display': 'table-cell', 'verticalAlign': 'middle'})])])

row5 = html.Div([
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='metrics',
                options=[{'label': i, 'value': i} for i in ['account_currency',
                                                            'account_id',
                                                            'account_name',
                                                            'actions',
                                                            'ad_id',
                                                            'ad_name',
                                                            'adset_id',
                                                            'adset_name',
                                                            'buying_type',
                                                            'campaign_id',
                                                            'campaign_name',
                                                            'date_start',
                                                            'date_stop',
                                                            'objective',
                                                            'action_values',
                                                            'canvas_avg_view_percent',
                                                            'canvas_avg_view_time',
                                                            'clicks',
                                                            'conversion_rate_ranking',
                                                            'conversion_values',
                                                            'conversions',
                                                            'cost_per_action_type',
                                                            'cost_per_conversion',
                                                            'cost_per_estimated_ad_recallers',
                                                            'cost_per_inline_link_click',
                                                            'cost_per_inline_post_engagement',
                                                            'cost_per_outbound_click',
                                                            'cost_per_thruplay',
                                                            'cost_per_unique_action_type',
                                                            'cost_per_unique_click',
                                                            'cost_per_unique_inline_link_click',
                                                            'cost_per_unique_outbound_click',
                                                            'cpc', 'cpm', 'cpp', 'ctr',
                                                            'engagement_rate_ranking',
                                                            'estimated_ad_recall_rate',
                                                            'estimated_ad_recallers',
                                                            'frequency',
                                                            'full_view_impressions',
                                                            'full_view_reach', 'impressions',
                                                            'inline_link_click_ctr',
                                                            'inline_link_clicks',
                                                            'inline_post_engagement',
                                                            'instant_experience_clicks_to_open',
                                                            'instant_experience_clicks_to_start',
                                                            'instant_experience_outbound_clicks',
                                                            'mobile_app_purchase_roas',
                                                            'outbound_clicks',
                                                            'outbound_clicks_ctr',
                                                            'purchase_roas',
                                                            'quality_ranking',
                                                            'reach', 'social_spend',
                                                            'spend', 'unique_actions',
                                                            'unique_clicks', 'unique_ctr',
                                                            'unique_inline_link_click_ctr',
                                                            'unique_inline_link_clicks',
                                                            'unique_link_clicks_ctr',
                                                            'unique_outbound_clicks',
                                                            'unique_outbound_clicks_ctr',
                                                            'video_30_sec_watched_actions',
                                                            'video_avg_time_watched_actions',
                                                            'video_p100_watched_actions',
                                                            'video_p25_watched_actions',
                                                            'video_p50_watched_actions',
                                                            'video_p75_watched_actions',
                                                            'video_p95_watched_actions',
                                                            'video_play_actions',
                                                            'video_play_curve_actions',
                                                            'website_ctr',
                                                            'website_purchase_roas']], persistence=True,
                persistence_type='memory',
                multi=True,
                style={'width': '300px'},
                placeholder='Dimensions & Metrics')
        ], style={'margin-top': 20, 'margin-left': -250, 'display': 'table-cell', 'verticalAlign': 'middle'})])])

row6 = html.Div([
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='breakdown',
                options=[{'label': i, 'value': i} for i in ['ad_format_asset', 'age', 'body_asset',
                                                            'call_to_action_asset', 'country',
                                                            'description_asset',
                                                            'gender', 'image_asset',
                                                            'impression_device',
                                                            'link_url_asset',
                                                            'product_id',
                                                            'region',
                                                            'title_asset',
                                                            'video_asset',
                                                            'dma',
                                                            'frequency_value',
                                                            'hourly_stats_aggregated_by_advertiser_time_zone',
                                                            'hourly_stats_aggregated_by_audience_time_zone',
                                                            'place_page_id',
                                                            'publisher_platform',
                                                            'platform_position',
                                                            'device_platform']], persistence=True,
                persistence_type='memory',
                multi=True,
                style={'width': '300px'},
                placeholder='Breakdown')
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
            html.Button(id='submit-button', type='submit', children='Submit', style={'width': '300px'}),

        ], width={"order": "first"}, style={'margin-top': 20, 'margin-left': -235, 'display': 'table-cell',
                                            'verticalAlign': 'middle'}),
        dbc.Col([
            html.Div(id='output_div-fb'),
        ])
    ])
])

row10 = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Input(id="save-report",
                      type="text",
                      placeholder="Save Report as",
                      style={'width': '300px'}, persistence=True,
                      persistence_type='memory'),
        ], style={'margin-top': 20, 'margin-left': -250, 'display': 'table-cell', 'verticalAlign': 'middle'})])])

row11 = html.Div([
    dbc.Row([
        dbc.Col([
            html.Button(id='submit-button-save', type='submit', children='Submit', style={'width': '300px'}),
        ], width={"order": "first"}, style={'margin-top': 20, 'margin-left': -235, 'display': 'table-cell',
                                            'verticalAlign': 'middle'}),
        dbc.Col([
            html.Div(id='output_div-save'),
        ])
    ])
])

row12 = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Input(id="get-report",
                      type="text",
                      placeholder="Get Report",
                      style={'width': '300px'}, persistence=True,
                      persistence_type='memory'),
        ], style={'margin-top': 20, 'margin-left': -250, 'display': 'table-cell', 'verticalAlign': 'middle'})])])

row13 = html.Div([
    dbc.Row([
        dbc.Col([
            html.Button(id='submit-button-get', type='submit', children='Submit', style={'width': '300px'}),

        ], width={"order": "first"}, style={'margin-top': 20, 'margin-left': -235, 'display': 'table-cell',
                                            'verticalAlign': 'middle'}),
        dbc.Col([
            html.Div(id='output_div-get'),
        ])
    ])
])

# row1 = html.Div([
#      dbc.Row([
#          dbc.Col([
#              dbc.Input(id="ad_account_id",
#                        type="text",
#                        placeholder="Account ID",
#                        style={'width': '150px'}, persistence=True,
#                        persistence_type='memory'),
#          ]),
#
#          dbc.Col([
#              dbc.Input(id="app_id",
#                        type="text",
#                        placeholder="App ID",
#                        style={'width': '150px'}, persistence=True,
#                        persistence_type='memory', ),
#          ]),
#          dbc.Col([
#              dbc.Input(id="access_token",
#                        type="text",
#                        style={'width': '150px'},
#                        placeholder="Access Token", persistence=True,
#                        persistence_type='memory', )
#          ]),
#          dbc.Col([
#              dbc.Input(id="app_secret",
#                        type="text",
#                        style={'width': '150px'},
#                        placeholder="App Secret", persistence=True,
#                        persistence_type='memory', )
#          ]),
#
# dbc.Col([
#     dcc.Dropdown(
#         id='metrics',
#         options=[{'label': i, 'value': i} for i in ['account_currency',
#                                                     'account_id',
#                                                     'account_name',
#                                                     'actions',
#                                                     'ad_id',
#                                                     'ad_name',
#                                                     'adset_id',
#                                                     'adset_name',
#                                                     'buying_type',
#                                                     'campaign_id',
#                                                     'campaign_name',
#                                                     'date_start',
#                                                     'date_stop',
#                                                     'objective',
#                                                     'action_values',
#                                                     'canvas_avg_view_percent',
#                                                     'canvas_avg_view_time',
#                                                     'clicks',
#                                                     'conversion_rate_ranking',
#                                                     'conversion_values',
#                                                     'conversions',
#                                                     'cost_per_action_type',
#                                                     'cost_per_conversion',
#                                                     'cost_per_estimated_ad_recallers',
#                                                     'cost_per_inline_link_click',
#                                                     'cost_per_inline_post_engagement',
#                                                     'cost_per_outbound_click',
#                                                     'cost_per_thruplay',
#                                                     'cost_per_unique_action_type',
#                                                     'cost_per_unique_click',
#                                                     'cost_per_unique_inline_link_click',
#                                                     'cost_per_unique_outbound_click',
#                                                     'cpc', 'cpm', 'cpp', 'ctr',
#                                                     'engagement_rate_ranking',
#                                                     'estimated_ad_recall_rate',
#                                                     'estimated_ad_recallers',
#                                                     'frequency',
#                                                     'full_view_impressions',
#                                                     'full_view_reach', 'impressions',
#                                                     'inline_link_click_ctr',
#                                                     'inline_link_clicks',
#                                                     'inline_post_engagement',
#                                                     'instant_experience_clicks_to_open',
#                                                     'instant_experience_clicks_to_start',
#                                                     'instant_experience_outbound_clicks',
#                                                     'mobile_app_purchase_roas',
#                                                     'outbound_clicks',
#                                                     'outbound_clicks_ctr',
#                                                     'purchase_roas',
#                                                     'quality_ranking',
#                                                     'reach', 'social_spend',
#                                                     'spend', 'unique_actions',
#                                                     'unique_clicks', 'unique_ctr',
#                                                     'unique_inline_link_click_ctr',
#                                                     'unique_inline_link_clicks',
#                                                     'unique_link_clicks_ctr',
#                                                     'unique_outbound_clicks',
#                                                     'unique_outbound_clicks_ctr',
#                                                     'video_30_sec_watched_actions',
#                                                     'video_avg_time_watched_actions',
#                                                     'video_p100_watched_actions',
#                                                     'video_p25_watched_actions',
#                                                     'video_p50_watched_actions',
#                                                     'video_p75_watched_actions',
#                                                     'video_p95_watched_actions',
#                                                     'video_play_actions',
#                                                     'video_play_curve_actions',
#                                                     'website_ctr',
#                                                     'website_purchase_roas']], persistence=True,
#         persistence_type='memory',
#         multi=True,
#         style={'width': '300px'},
#         placeholder='Dimensions & Metrics')
# ]),
#      ], align="center"),
#      ], style={'margin-top': 20, 'margin-left': -90}
# )
#
# row2 = html.Div([
#     dbc.Row([
#         dbc.Col([
#             dcc.Dropdown(
#                 id='breakdown',
#                 options=[{'label': i, 'value': i} for i in ['ad_format_asset', 'age', 'body_asset',
#                                                             'call_to_action_asset', 'country',
#                                                             'description_asset',
#                                                             'gender', 'image_asset',
#                                                             'impression_device',
#                                                             'link_url_asset',
#                                                             'product_id',
#                                                             'region',
#                                                             'title_asset',
#                                                             'video_asset',
#                                                             'dma',
#                                                             'frequency_value',
#                                                             'hourly_stats_aggregated_by_advertiser_time_zone',
#                                                             'hourly_stats_aggregated_by_audience_time_zone',
#                                                             'place_page_id',
#                                                             'publisher_platform',
#                                                             'platform_position',
#                                                             'device_platform']], persistence=True,
#                 persistence_type='memory',
#                 multi=True,
#                 style={'width': '250px'},
#                 placeholder='Breakdown')
#         ]),
#         html.Br(),
#         dbc.Col([
#             dcc.DatePickerSingle(
#                 id='start-date',
#                 placeholder="Start Date",
#                 min_date_allowed=datetime.datetime.now().strftime('2018-01-01'),
#                 max_date_allowed=datetime.datetime.today().date(),
#                 display_format='YYYY-MM-DD',
#                 style={'width': '150px', 'margin-left': 30}, persistence=True,
#                 persistence_type='memory',
#             ),
#         ]),
#         dbc.Col([
#             dcc.DatePickerSingle(
#                 id='end-date',
#                 placeholder="End Date",
#                 min_date_allowed=datetime.datetime.now().strftime('2018-01-01'),
#                 max_date_allowed=datetime.datetime.today().date(),
#                 display_format='YYYY-MM-DD',
#                 style={'width': '150px', 'margin-left': 40}, persistence=True,
#                 persistence_type='memory',
#             )]),
#     ])
# ])
#
# row3 = html.Div([
#     dbc.Row([
#         dbc.Col([
#             html.Button(id='submit-button', type='submit', children='Submit', style={'width': '150px', 'margin-top': 5,
#                                                                                      'margin-left': 370}),
#
#         ], width={"order": "first"}),
#         dbc.Col([
#             html.Div(id='output_div-fb'),
#         ])
#     ])
# ])

# row4 = html.Div([
#     dbc.Row([
#         dbc.Col([
#             html.Button(id='submit-button-save', type='submit', children='Submit', style={'width': '150px',
#                                                                                           'margin-top': 10,
#                                                                                           'margin-left': 10}),
#
#         ], width={"order": "first"}),
#         dbc.Col([
#             html.Div(id='output_div-save'),
#         ])
#     ])
# ])
#
# row5 = html.Div([
#     dbc.Row([
#         dbc.Col([
#             dbc.Input(id="save-report",
#                       type="text",
#                       placeholder="Save Report as",
#                       style={'width': '150px', 'margin-top': -60, 'margin-left': 0}, persistence=True,
#                       persistence_type='memory'),
#         ])])])
#
# row6 = html.Div([
#     dbc.Row([
#         dbc.Col([
#             dbc.Input(id="get-report",
#                       type="text",
#                       placeholder="Get Report",
#                       style={'width': '150px', 'margin-top': -160, 'margin-left': 700}, persistence=True,
#                       persistence_type='memory'),
#         ])])])
#
# row7 = html.Div([
#     dbc.Row([
#         dbc.Col([
#             html.Button(id='submit-button-get', type='submit', children='Submit', style={'width': '150px',
#                                                                                          'margin-top': -1000,
#                                                                                          'margin-left': 720}),
#
#         ], width={"order": "first"}),
#         dbc.Col([
#             html.Div(id='output_div-get'),
#         ])
#     ])
# ])

tab_1_layout = dbc.Container(children=[
    row1, row2, row3, row4,
    row5, row6,
    row7, row8,
    row9, row10,
    row11, row12,
    row13
]
)


@app.callback(Output('output_div-fb', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('ad_account_id', 'value'),
               State('app_id', 'value'),
               State('access_token', 'value'),
               State('app_secret', 'value'),
               State('metrics', 'value'),
               State('breakdown', 'value'),
               State('start-date', 'date'),
               State('end-date', 'date'),
               ],
              )
def facebook_output(clicks, ad_account_id, app_id, access_token, app_secret, metrics, breakdown,
                    start_date, end_date):
    if clicks is not None:
        my_ad_account = ad_account_id
        my_app_id = app_id
        my_access_token = access_token
        my_app_secret = app_secret
        my_metrics = metrics
        my_breakdown = breakdown
        my_start_date = start_date
        my_end_date = end_date
        my_action_type = 'action_type'
        my_level = 'ad'
        my_time_increment = 1
        FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token,
                            api_version='v5.0')
        me = User(fbid="me")
        new_col_list = my_metrics
        # print(new_col_list)
        act = AdAccount(my_ad_account)
        async_job = act.get_insights(params={'time_range': {'since': my_start_date, 'until': my_end_date},
                                             'breakdowns': list(my_breakdown),
                                             'action_breakdowns': my_action_type, 'level': my_level,
                                             'time_increment': my_time_increment},
                                     fields=list(new_col_list))
        df = pd.DataFrame(async_job)
        dff = df[new_col_list]
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
                            'width': '{}%'.format(len(dff.columns)), 'textOverflow': 'ellipsis',
                            'overflow': 'hidden'},

                style_table={'maxHeight': '200px', 'overflowY': 'scroll', 'maxWidth': '1000px',
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
                tooltip_duration=None, persistence=True, persistence_type='memory'
            ),
        ], style={'margin-top': 20, 'margin-left': 300, 'display': 'table-cell', 'verticalAlign': 'middle',
                  'width': '100%'})


# Save the Query Parameters
@app.callback(Output('output_div-save', 'children'),
              [Input('submit-button-save', 'n_clicks')],
              [State('ad_account_id', 'value'),
               State('app_id', 'value'),
               State('access_token', 'value'),
               State('app_secret', 'value'),
               State('metrics', 'value'),
               State('breakdown', 'value'),
               State('start-date', 'date'),
               State('end-date', 'date'),
               State('save-report', 'value'),
               ],
              )
def facebook_output(clicks, ad_account_id, app_id, access_token, app_secret, metrics, breakdown,
                    start_date, end_date, save_report):
    if clicks is not None:
        dff = pd.read_csv('query.csv')
        my_ad_account = ad_account_id
        my_app_id = app_id
        my_access_token = access_token
        my_app_secret = app_secret
        my_metrics = metrics
        my_breakdown = breakdown
        my_start_date = start_date
        my_end_date = end_date
        my_save_report = save_report
        data = [my_save_report, my_ad_account, my_app_id, my_access_token, my_app_secret, my_metrics,
                my_breakdown, my_start_date, my_end_date]
        df = pd.DataFrame([data], columns=['Report Name', 'Ad Account id', 'App id', 'Access token', 'App secret',
                                           'Metrics and dimensions', 'Breakdown', 'Start date', 'End date'])
        df_new = df.append(dff)
        df_new.to_csv('query.csv', index=False)
        html.Br()
        return "Your report has been saved as {}".format(df['Report Name'].to_string(index=False))


# Fill the reports
@app.callback([Output('ad_account_id', 'value'),
               Output('app_id', 'value'),
               Output('access_token', 'value'),
               Output('app_secret', 'value'),
               Output('metrics', 'value'),
               Output('breakdown', 'value'),
               Output('start-date', 'date'),
               Output('end-date', 'date')],
              [Input('submit-button-get', 'n_clicks')],
              [State('get-report', 'value')], )
def facebook_output(clicks, get_report):
    if clicks is not None:
        print(get_report)
        df = pd.read_csv('query.csv')
        df = df.loc[df['Report Name'].isin(['{}'.format(get_report)])]
        print(df)
        df['Start date'] = pd.to_datetime(df['Start date'])
        df['End date'] = pd.to_datetime(df['End date'])
        ad_account_id = list(df.iloc[:, 1])
        app_id = list(df.iloc[:, 2])
        access_token = list(df.iloc[:, 3])
        app_secret = list(df.iloc[:, 4])
        metrics = df.iloc[:, 5].to_string(index=False)
        metrics_new = metrics.replace("'", "")
        metrics_n = metrics_new.replace("[", "")
        metrics_nn = metrics_n.replace("]", "")
        metrics_list = [x.strip() for x in metrics_nn.split(',')]
        # metrics_list_new = [x.encode('utf-8') for x in metrics_list]

        breakdown = df.iloc[:, 6].to_string(index=False)
        breakdown_new = breakdown.replace("'", "")
        breakdown_n = breakdown_new.replace("[", "")
        breakdown_nn = breakdown_n.replace("]", "")
        breakdown_list = [x.strip() for x in breakdown_nn.split(',')]
        # breakdown_list_new = [x.encode('utf-8') for x in breakdown_list]

        start_date = df.iloc[:, 7].to_string(index=False)
        end_date = df.iloc[:, 8].to_string(index=False)

        return ad_account_id, app_id, access_token, app_secret, [i for i in metrics_list], \
               [i for i in breakdown_list], start_date, end_date
