import base64

from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from Dash_App.app import app
from Dash_App.tabs import facebook, googleanalytics, DCM, DV360

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

image_filename = 'C:/sapientrepo/Dash_App/assets/Screenshot_3.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = html.Div([html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                                style={'height': '10%', 'width': '10%'}, ),
                       html.H6('Marketing Funnel Reports', style={'color': '#ffd480', 'font-weight': 'bold',
                                                                  'text-align': 'right', 'margin-top': -40}),
                       dcc.Tabs(id="tabs-example", value='tab-1-example',
                                children=[dcc.Tab(label='Facebook', value='tab-1-example',
                                                  style=tab_style, selected_style=tab_selected_style),
                                          dcc.Tab(label='GoogleAnalytics', value='tab-2-example',
                                                  style=tab_style, selected_style=tab_selected_style),
                                          dcc.Tab(label='DCM', value='tab-3-example', style=tab_style,
                                                  selected_style=tab_selected_style),
                                          dcc.Tab(label='DV360', value='tab-4-example', style=tab_style,
                                                  selected_style=tab_selected_style),
                                          ],
                                style=tabs_styles),
                       html.Div(id='tabs-content-example')])


@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1-example':
        return facebook.tab_1_layout
    elif tab == 'tab-2-example':
        return googleanalytics.tab_2_layout
    elif tab == 'tab-3-example':
        return DCM.tab_3_layout
    elif tab == 'tab-4-example':
        return DV360.tab_4_layout
    else:
        return '404'


external_css = ["https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "https://codepen.io/bcd/pen/KQrXdb.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
                "https://codepen.io/dmcomfort/pen/JzdzEZ.css"]

for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ["https://code.jquery.com/jquery-3.2.1.min.js",
               "https://codepen.io/bcd/pen/YaXojL.js"]

if __name__ == '__main__':
    app.run_server(debug=True)
