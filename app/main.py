


import dash
import dash_table
from dash.dependencies import Input, Output,  State
import dash_core_components as dcc
import dash_html_components as html

import sys
import pandas as pd
import plotly.graph_objs as go


import plotly.express as px


from reduction import make_pca, morgan_finger,loc_value,make_tsne, make_umap


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv(sys.argv[1])
print(df.head())




with open(("demo_intro.md"), "r") as file:
    demo_intro_md = file.read()



def Card(children, **kwargs):
    return html.Section(children, className="card-style")

def create_layout(app):
    return html.Div(
        className="row",
        style={"max-width": "100%", "font-size": "1.5rem", "padding": "0px 0px"},
        children=[
            # Header
            html.Div(
                className="row header",
                id="app-header",
                style={"background-color": "#f9f9f9"},
                children=[
                    html.Div(
                        [
                            html.H3(
                                "Hugo reduction",
                                className="header_title",
                                id="app-title",
                            )
                        ],
                        className="nine columns header_title_container",
                    ),
                ],
            ),
            # Demo Description
            html.Div(
                className="row background",
                id="demo-explanation",
                style={"padding": "50px 45px"},
                children=[
                    html.Div(
                        id="description-text", children=dcc.Markdown(demo_intro_md)
                    ),      
                ],
            ),

            
            # Body
            html.Div(
                className="row background",
                style={"padding": "10px"},
                children=[
                    html.Div(
                        className="three columns",
                        children=[
                            Card(
                                [
                                    dcc.Dropdown(
                                        id="dropdown-reduction",
                                        searchable=False,
                                        clearable=False,
                                        options=[
                                            {
                                                "label": "PCA",
                                                "value": "df_pca",
                                            },
                                            {
                                                "label": "T-sne",
                                                "value": "df_tsne",
                                            },
                                            {
                                                "label": "UMAP",
                                                "value": "df_umap",
                                            },
                                        ],
                                        placeholder="Select a reduction",
                                        value="df_pca",
                                    ),
                                    html.Div(id='dd-output-container')

                                ]
                            )
                        ],
                    ),
                    html.Div(
                        className="six columns",
                        children=[
                            dcc.Graph(id='graph-with-slider'),
                            dcc.RangeSlider(
                                id='value-slider',
                                min=1,
                                max=10,
                                step=0.5,
                                value=[1,8],
                                marks={str(x): str(x) for x in range(0,10,1)},

                                ),
                            ],
                        ),




                ],
            ),
        ],
    )

df_morg =morgan_finger(df)
df_pca = make_pca(df_morg)
df_tsne = make_tsne(df_morg)
df_umap = make_umap(df_morg)

df_tsne= df_tsne.merge(df[['label','value','smiles']],left_on=df.smiles, right_on=df_tsne.index)
df_pca= df_pca.merge(df[['label','value','smiles']],left_on=df.smiles, right_on=df_pca.index)
df_umap= df_umap.merge(df[['label','value','smiles']],left_on=df.smiles, right_on=df_umap.index)


def callbacks(app):
    print('callback est appelé')

    @app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('dropdown-reduction', 'value')])
    def update_output_reduction(value):
        return 'You have selected "{}"'.format(value)


    
    @app.callback( 
        Output('graph-with-slider', 'figure'),
            [
            Input('dropdown-reduction', 'value'),
            Input('value-slider', 'value'),
            ]
        )
        
    def update_figure(value,value_df):

        print("value reduction", value)
        print("value df", value_df)
    
        if value == "df_pca":
            print("blocle pca")


            filtered_df = loc_value(df_pca,value_df[0],value_df[1])
            print(filtered_df.head())

            figure = px.scatter(filtered_df, x=filtered_df['PC1'], y=filtered_df['PC2'])

            figure.update_layout(transition_duration=500)
            return figure

        if value == "df_tsne":
            print("blocle df_tsne")

            filtered_df = loc_value(df_tsne,value_df[0],value_df[1])
            print(filtered_df.head())

            figure = px.scatter(filtered_df, x=filtered_df['PC1'], y=filtered_df['PC2'])

            figure.update_layout(transition_duration=500)
            return figure
            
        if value == "df_umap":

            filtered_df = loc_value(df_umap,value_df[0],value_df[1])
 

            figure = px.scatter(filtered_df, x=filtered_df['PC1'], y=filtered_df['PC2'])

            figure.update_layout(transition_duration=500)
            return figure

    


app.layout = create_layout(app)
callbacks(app)


if __name__ == '__main__':
    app.run_server(debug=True)
