# import dataiku


import warnings

warnings.filterwarnings('ignore')

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Initialise the app
app = dash.Dash(__name__)


app.layout = html.Div(
    style={}, 
    children=[
        dcc.Interval(id='interval', interval=2000),
        html.H1('Whatsapp Cleaner'),
        html.Div(
            id = 'main',
            children = ''
        ),
    ]
)

@app.callback(Output('main', 'children'), Input('interval', 'n_intervals'),)
def interval_update(n_intervals):
    return str(n_intervals)

# Run the app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port = 8050)

