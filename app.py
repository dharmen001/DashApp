import dash
import dash_bootstrap_components as dbc
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = dbc.themes.BOOTSTRAP
app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                external_stylesheets=[external_stylesheets], serve_locally=False, prevent_initial_callbacks=True)
app.title = "Data"
server = app.server
app.config['suppress_callback_exceptions'] = True
