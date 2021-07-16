# import dataiku

import time
import warnings

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from clear_massages import clear, is_clear
from landing import is_landing_main, landing_get_image
from taken import is_taken, log_out, refresh

warnings.filterwarnings('ignore')


import platform
from pathlib import Path

main_style = {
    'background': '#FFFFFF',
    'font-family': "Arial"
}

title_style = {
    'background': '#5473FF',
    'text': '#FFFFFF'
}

desc_style = {
    'background': '#FFFFFF',
    'text': '5473FF'
}
dropdown_style = {
    'background': '#DDE5ED',
    'text': '#221C35'
}


def init_driver():
    # try:
    #     driver
    #     return driver
    # except:
    #     pass
    url = 'https://web.whatsapp.com/'

    # chrome_driver_path = 'chromedriver_win32/chromedriver.exe'
    # op = webdriver.ChromeOptions()
    # # op.add_argument('headless')

    # driver = webdriver.Chrome(chrome_driver_path)


    # driver.get(url)
    
    options = FirefoxOptions()
    options.add_argument("--headless")
    print(platform.platform())
    if 'indow' in platform.system():
            driver = webdriver.Firefox(executable_path = str(Path('drivers') / 'geckodriver-v0.29.1-win64' / 'geckodriver.exe'), options=options)#, chrome_options=op)
    else:
        try:
            driver = webdriver.Firefox(executable_path = str(Path('drivers') / 'geckodriver-v0.29.1-linux32' / 'geckodriver'), options=options)#, chrome_options=op)
        except:
            driver = webdriver.Firefox(executable_path = str(Path('drivers') / 'geckodriver-v0.29.1-linux64' / 'geckodriver'), options=options)#, chrome_options=op)
    
    driver.get(url)

    time.sleep(5)

    # url = driver.command_executor._url
    # session_id = driver.session_id 

    return driver


# Initialise the app
app = dash.Dash(__name__)
driver = init_driver()


app.layout = html.Div(
    style={}, 
    children=[
        html.Div(id='dummy-output', style={'display':'none'}),
        dcc.Interval(id='interval', interval=2000),
        dcc.Interval(id='clear-interval', interval=30000),
        html.H1('Whatsapp Cleaner'),
        html.Div(
            id = 'main',
            children = ''
        ),
    ]
)

@app.callback(Output('main', 'children'), Input('interval', 'n_intervals'),)
def interval_update(n_intervals):
    if is_landing_main(driver):
        # return html.Img(src=app.get_asset_url(landing_get_image(driver)), style={'height':'50%', 'width':'50%'})
        return html.Img(src='data:image/png;base64{}'.format(landing_get_image(driver)))
    elif is_taken(driver):
        return [
            html.Button('Refresh', id='refresh-button'),
            html.Button('Sign out', id='signout-button')
        ]
    else:
        return html.Button('Clean', id='clean-button')

@app.callback(Output('dummy-output', 'children'), Input('clear-interval', 'n_intervals'))
def interval_update(n_intervals):
    if not is_landing_main(driver) and not is_taken(driver) and not is_clear():
        clear(driver)
    return ''

@app.callback(Output('refresh-button', 'style'), Input('refresh-button', 'n_clicks'), prevent_initial_call=True)
def refresh_button(n_clicks):
    refresh(driver)
    dash.exceptions.PreventUpdate("")
    return {}

@app.callback(Output('signout-button', 'style'), Input('signout-button', 'n_clicks'), prevent_initial_call=True)
def signout_button(n_clicks):
    log_out(driver)
    dash.exceptions.PreventUpdate("")
    return {}

@app.callback(Output('clean-button', 'style'), Input('clean-button', 'n_clicks'), prevent_initial_call=True)
def clean_button(n_clicks):
    if(not is_clear()):
        clear(driver)
    dash.exceptions.PreventUpdate("")
    return {}



# app.layout = html.Div(
#     ## Step 1: Define App Style
#     style={
#         'backgroundColor': main_style['background'],
#         'font-family': main_style['font-family']
#     },
#     children=[
#         html.H1(
#             children='Total Sales by Country',
#             style={
#                 'backgroundColor': title_style['background'],
#                 'color': title_style['text'],
#                 'textAlign': 'center'}
#         ),
#         html.Div(
#             children='This graph allows you to compare the total sales amount and campaign influence by country.',
#             style={
#                 'backgroundColor': desc_style['background'],
#                 'color': desc_style['text'],
#                 'textAlign': 'center'}
#         ),
#         html.Div(
#             id = 'main'
#         ),
#         html.Label(
#             children='Select countries:'
#         ),
#         dcc.Dropdown(
#             id='country-dropdown',
#             style={'color': dropdown_style['text']},
#             options=[{'label': i, 'value': i} for i in sorted(df.country.unique())],
#             # value=[i for i in sorted(df.country.unique())],
#             multi=True
#         )
#     ]
# )


# @app.callback(Output(component_id='main', component_property='children'),
#             [Input(component_id='country-dropdown', component_property='value')],
#             prevent_initial_call=False
#             )
# def update_graph(input_value):
#     if not input_value:
#         input_value = []
#     if len(input_value) > 0:
#         updated_df = df[df['country'].isin(input_value)]
#         fig = px.histogram(updated_df,
#                         x="value",
#                         color="country",
#                         title="Sales by Country",
#                         )
#         return dcc.Graph(
#             id='graph-output',
#             figure = fig
#         )
#     elif len(input_value) == 0:
#         return html.H2('הכנס!')
#         # raise dash.exceptions.PreventUpdate

# # Define the app
# # app.layout = html.Div()
# app.layout = html.Div(children=[
#                       html.Div(className='row',  # Define the row element
#                                children=[
#                                   html.Div(className='four columns div-user-controls'),  # Define the left element
#                                   html.Div(className='eight columns div-for-charts bg-grey')  # Define the right element
#                                   ])
#                                 ])

# Run the app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port = 8050)

