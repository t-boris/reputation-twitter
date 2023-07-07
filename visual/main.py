import base64
import pickle
from dash import Dash, html, dcc
import os
from data.provider import DataProvider
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from dash import callback_context


# Read list of json files in local folder
areas = [pos_json.replace('.json', '') for pos_json in os.listdir('.') if pos_json.endswith('.json')]

current_state = None
prev_states = []

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Social Network Review', style={'textAlign':'center'}),
    dcc.Dropdown(areas, areas[0], id='dropdown-selection'),
    dcc.Graph(id='graph', figure=go.Figure()),
    html.Div(id='json-data', style={'display': 'none'}),  # Store JSON data here
    html.Button('Back', id='back-button')  # Add a back button
])

@app.callback(Output('json-data', 'children'), [Input('dropdown-selection', 'value')])
def update_data_provider(selected_file):
    dp = DataProvider(selected_file)
    prev_states.clear()
    pickled_dp = pickle.dumps(dp)
    base64_dp = base64.b64encode(pickled_dp).decode()
    return base64_dp

@app.callback([Output('graph', 'figure'), Output('back-button', 'disabled')],
              [Input('graph', 'clickData'), Input('json-data', 'children'), Input('back-button', 'n_clicks')])
def update_graph(clickData, jsonData, back_clicks):
    global current_state
    j_data = base64.b64decode(jsonData)
    dp = pickle.loads(j_data)
    if current_state is not None:
        dp.select_node(current_state)

    ctx = callback_context
    if ctx.triggered and 'back-button' in ctx.triggered[0]['prop_id']:
        # If the back button triggered the callback
        if back_clicks and back_clicks > 0 and prev_states:
            # Pop the last state from the stack and restore it
            node_id = prev_states.pop()
            dp.select_node(node_id)
            current_state = node_id
    else:
        # If the graph click triggered the callback
        if clickData is not None:
            # Push the current state onto the stack before updating it
            prev_states.append(dp.get_selected_node_id())
            node_id = clickData['points'][0]['id']
            dp.select_node(node_id)
            current_state = node_id

    children = dp.get_sub_topics()

    # Update figure with new data
    fig = go.Figure([go.Bar(
        x=[node['name'] for node in children],
        y=[node['total'] for node in children],
        ids = [node['id'] for node in children]
    )])

    return [fig, len(prev_states) == 0]


if __name__ == '__main__':
    app.run(debug=True)

