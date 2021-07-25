# Libraries
import data_prepro
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np
import json
import plotly.graph_objects as go
from dash.dependencies import Input, Output

# Initialize app
app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
app.title = "Ericsson Dashboard"
server = app.server

# Load data
df_r = data_prepro.df_rsrp
df_t = data_prepro.df_tv
df_down = data_prepro.df_down
da = data_prepro.da
db = data_prepro.db
dc = data_prepro.dc
#geojson = json.load(open('assets/world.geo.json'))

# Setting Colors
DEFAULT_COLORSCALE = [
    "#f2fffb",
    "#bbffeb",
    "#98ffe0",
    "#79ffd6",
    "#6df0c8",
    "#69e7c0",
    "#59dab2",
    "#45d0a5",
    "#31c194",
    "#2bb489"
]
DEFAULT_OPACITY = 0.8
#BINS = [
#     "-140-130",
#     "-130-120",
#     "-120-110",
#     "-110-100",
#     "-100-90",
#     "-90-80",
#     "-80-70",
#     "-70-60",
#     "-60-50",
#     "-50-40",
# ]

# Configuring mapbox token
mapbox_token = "pk.eyJ1IjoiYWhtZWQtbWVrbGVkIiwiYSI6ImNrcjZnaGdjeTMwMjYydXBsdWdnbGZ2dTkifQ.pD26q64fclcWpbjC9zf0Eg"
mapbox_style = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"


def plot_map(data):
    fig = px.density_mapbox(data, lat=data['LocationLatitude'],
                            lon=data['LocationLongitude'],
                            radius=10,
                            animation_frame=data["Timestamp"].astype(str)
                            )
    fig.update_layout(mapbox_style=mapbox_style, mapbox_accesstoken=mapbox_token, mapbox_zoom=7.5,
                      mapbox_center={"lat": 24.774265, "lon": 46.738586}, )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 600
    fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 600
    fig.layout.coloraxis.showscale = True
    fig.layout.sliders[0].pad.t = 10
    fig.layout.updatemenus[0].pad.t = 10

    #fig.show()
    return fig

# APP
app.layout = html.Div(
    id="root",
    children=[
        html.Div(
            id="header",
            children=[
                html.Img(
                    id="logo",
                    src=app.get_asset_url("ericsson-logo.png"),
                ),
                html.H1("Ericsson Challenge Dashboard"),
            ],
        ),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[
                        html.Div(
                            id="slider-container",
                            children=[
                                html.P(
                                    id='Slider-text',
                                    children="Time Laps Density Map:")
                            ],
                        ),
                        html.Div(
                            children=[dcc.Graph(id="densitymap-container", figure=(plot_map(df_t)))],
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            id="app-container2",
            children=[
                html.Div(
                    id="row-two",
                    children=[
                        html.Div(
                            id="heatmap-container",
                            children=[
                                html.P(id="chart-selector", children="Select Operator:"),
                                dcc.Dropdown(
                                    options=[
                                        {
                                            "label": "Operator A",
                                            "value": "Operator A",
                                        },
                                        {
                                            "label": "Operator B",
                                            "value": "Operator B",
                                        },
                                        {
                                            "label": "Operator C",
                                            "value": "Operator C",
                                        },
                                    ],
                                    value="Operator A",
                                    id="chart-dropdown",
                                ),
                                dcc.Graph(
                                    id="choropleth",
                                    # figure=dict(
                                    #     layout=dict(
                                    #         mapbox=dict(
                                    #             layers=[],
                                    #             accesstoken=mapbox_token,
                                    #             style=mapbox_style,
                                    #             center=dict(
                                    #                 lat=24.774265, lon=46.738586
                                    #             ),
                                    #             pitch=0,
                                    #             zoom=3.5,
                                    #         ),
                                    #         autosize=True,
                                    #     ),
                                    # ),
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            id="app-container3",
            children=[
                html.Div(
                    id="row-three",
                    children=[
                        html.Div(
                            id='hex-slider-container',
                            children=[
                                html.P(
                                    id='hex-slider-text',
                                    children="Choose the size of the Hexagon on the Map:"
                                ),
                                dcc.Slider(
                                    id='hex-slider',
                                    min=1,
                                    max=10,
                                    value=1,
                                    marks={
                                        10: {"label": "1", "style": {"color": "#7fafdf"}},
                                        8: {"label": "2", "style": {"color": "#7fafdf"}},
                                        6: {"label": "4", "style": {"color": "#7fafdf"}},
                                        4: {"label": "6", "style": {"color": "#7fafdf"}},
                                        2: {"label": "8", "style": {"color": "#7fafdf"}},
                                        1: {"label": "10", "style": {"color": "#7fafdf"}},
                                    }

                                )
                            ],
                        ),
                        html.Div(
                            id='hexmap-container',
                            children=[
                                html.P(
                                    'HexMap of the selected size for the Downlink only.',
                                    id='hexmap-title',
                                ),
                                dcc.Graph(id='hex-map')
                            ]
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            id="app-container4",
            children=[
                html.Div(
                    id="row-four",
                    children=[
                        html.Div(
                            id='radio-container',
                            children=[
                                html.P(
                                    id='radio-text',
                                    children='Choose aggregation method and number of users from bellow:'
                                ),
                                dcc.RadioItems(
                                    id='agg-val',
                                    options=[
                                        {'label': 'Average', 'value': 'avg'},
                                        {'label': 'Minimum', 'value': 'min'},
                                        {'label': 'Maximum', 'value': 'max'},
                                        {'label': '90%', 'value': '90'}

                                    ],
                                    value='avg',
                                    labelStyle={'display': 'inline-block'}
                                ),
                                dcc.Slider(
                                    id='pop-slider',
                                    min=10,
                                    max=100,
                                    value=50,
                                    marks={
                                        10: {"label": "10 %", "style": {"color": "#7fafdf"}},
                                        25: {"label": "25 %", "style": {"color": "#7fafdf"}},
                                        50: {"label": "50 %", "style": {"color": "#7fafdf"}},
                                        75: {"label": "75 %", "style": {"color": "#7fafdf"}},
                                        100: {"label": "100 % ", "style": {"color": "#7fafdf"}},
                                    }

                                )
                            ]
                        ),
                        html.Div(
                            id='graph-container',
                            children=[
                                html.P(
                                    'Bar-Chart for every Operator and Device for the selected number of users.',
                                ),
                                dcc.Graph(id='bar-chart')
                            ]
                        )

                    ]
                )
            ],
        ),
    ]
)
@app.callback(
    Output("choropleth", "figure"),
    [Input("chart-dropdown", "value")]
)
# def display_map(chart_dropdown, figure):
#     cm = dict(zip(BINS, DEFAULT_COLORSCALE))
#     data = [
#         dict(
#             lat=df_r['LocationLatitude'],
#             lon=df_r['LocationLongitude'],
#             type="scattermapbox",
#             hoverinfo="text",
#             marker=dict(size=5, color="white", opacity=0),
#         )
#     ]
#     annotations = [
#         dict(
#             showarrow=False,
#             align="right",
#             text="<b>RSRP Value<br>per Operator</b>",
#             font=dict(color="#2cfec1"),
#             bgcolor="#1f2630",
#             x=0.95,
#             y=0.95,
#         )
#     ]
#     for i, bin in enumerate(reversed(BINS)):
#         color = cm[bin]
#         annotations.append(
#             dict(
#                 arrowcolor=color,
#                 text=bin,
#                 x=0.95,
#                 y=0.85 - (i / 20),
#                 ax=-60,
#                 ay=0,
#                 arrowwidth=5,
#                 arrowhead=0,
#                 bgcolor="#1f2630",
#                 font=dict(color="#2cfec1"),
#             )
#         )
#     if "layout" in figure:
#         lat = figure["layout"]["mapbox"]["center"]["lat"]
#         lon = figure["layout"]["mapbox"]["center"]["lon"]
#         zoom = figure["layout"]["mapbox"]["zoom"]
#     else:
#         lat = 24.774265
#         lon = 46.738586
#         zoom = 3.5
#
#     layout = dict(
#         mapbox=dict(
#             layers=[],
#             accesstoken=mapbox_token,
#             style=mapbox_style,
#             center=dict(lat=lat, lon=lon),
#             zoom=zoom,
#         ),
#         hovermode="closest",
#         margin=dict(r=0, l=0, t=0, b=0),
#         dragmode="lasso",
#     )
#     base_url = "https://raw.githubusercontent.com/ahmedmekled/Dash/main/"
#     for bin in BINS:
#         geo_layer = dict(
#             sourcetype="geojson",
#             source=base_url + chart_dropdown + "/" + bin + ".geojson",
#             type="fill",
#             color=cm[bin],
#             opacity=DEFAULT_OPACITY,
#             # CHANGE THIS
#             fill=dict(outlinecolor="#afafaf"),
#         )
#         layout["mapbox"]["layers"].append(geo_layer)
#
#     fig = dict(data=data, layout=layout)
#     return fig
def heat_map_2(chart_dropdown):
    OP = data_prepro.return_rsrp_unique(chart_dropdown)
    fig = px.scatter_mapbox(OP, lat=OP['LocationLatitude'], lon=OP['LocationLongitude'], hover_name="RadioOperatorName",
                            hover_data=["RSRP"],
                            color="RSRP", color_discrete_sequence=["fuchsia"], zoom=5)
    fig.update_layout(mapbox_style=mapbox_style, mapbox_accesstoken=mapbox_token)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig

@app.callback(
    Output("hex-map", "figure"),
    [Input("hex-slider", "value")]
)
def hex_map(size):

    fig = ff.create_hexbin_mapbox(
        data_frame=df_down, lat="LocationLatitude", lon="LocationLongitude",
        nx_hexagon=size, opacity=0.9, labels={"color": "Traffic Volume Value"},
        color="TrafficVolume", color_continuous_scale="aggrnyl", range_color=[1, 20],
        agg_func=np.sum
    )
    fig2 = px.scatter_mapbox(
        da,
        lat=da['LocationLatitude'],
        lon=da['LocationLongitude'],
        hover_name="RadioOperatorName",
        opacity=0.6,
        zoom=5,
        color='RadioOperatorName'
    )
    fig3 = px.scatter_mapbox(
        db,
        lat=db['LocationLatitude'],
        lon=db['LocationLongitude'],
        hover_name="RadioOperatorName",
        color='RadioOperatorName',
        opacity=0.6,
        zoom=5

    )
    fig4 = px.scatter_mapbox(
        dc,
        lat=dc['LocationLatitude'],
        lon=dc['LocationLongitude'],
        hover_name="RadioOperatorName",
        color='RadioOperatorName',
        opacity=0.6,
        zoom=5

    )
    fig.add_trace(fig2.data[0])
    fig.add_trace(fig3.data[0])
    fig.add_trace(fig4.data[0])
    fig.update_layout(mapbox_style=mapbox_style,
                      mapbox_accesstoken=mapbox_token,
                      legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
                      )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

@app.callback(
    Output("bar-chart", "figure"),
    [
        Input("agg-val", "value"),
        Input("pop-slider", "value")
    ]
)
def bar_fig(agg, pop):
    sams, hmd, huwa, lge, htc, vivo, real, zte, oppo, xia, one, sony, moto,\
    pana, tcl, qmobile, obi, sharp, leco = data_prepro.return_slice(pop, agg)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=sams.index,
        y=sams["RSRP"],
        name='Samsung',
        marker_color='indianred'
    ))
    fig.add_trace(go.Bar(
        x=hmd.index,
        y=hmd["RSRP"],
        name='HMD Global',
        marker_color='lightsalmon'
    ))
    fig.add_trace(go.Bar(
        x=sony.index,
        y=sony["RSRP"],
        name='Sony',
        marker_color='crimson'
    ))
    fig.add_trace(go.Bar(
        x=moto.index,
        y=moto["RSRP"],
        name='Motorola',
        marker_color='gold'
    ))
    fig.add_trace(go.Bar(
        x=htc.index,
        y=htc["RSRP"],
        name='HTC',
        marker_color='darksalmon'
    ))
    fig.add_trace(go.Bar(
        x=oppo.index,
        y=oppo["RSRP"],
        name='Oppo',
        marker_color='beige'
    ))
    fig.add_trace(go.Bar(
        x=xia.index,
        y=xia["RSRP"],
        name='Xiaomi',
        marker_color='gray'
    ))
    fig.add_trace(go.Bar(
        x=one.index,
        y=one["RSRP"],
        name='One Plus',
        marker_color='deeppink'
    ))
    fig.add_trace(go.Bar(
        x=lge.index,
        y=lge["RSRP"],
        name='LGE',
        marker_color='chocolate'
    ))
    fig.add_trace(go.Bar(
        x=huwa.index,
        y=huwa["RSRP"],
        name='Huwaui',
        marker_color='burlywood'
    ))
    fig.add_trace(go.Bar(
        x=tcl.index,
        y=tcl["RSRP"],
        name='TCL',
        marker_color='firebrick'
    ))
    fig.add_trace(go.Bar(
        x=real.index,
        y=real["RSRP"],
        name='RealMe',
        marker_color='midnightblue'
    ))
    fig.add_trace(go.Bar(
        x=sharp.index,
        y=sharp["RSRP"],
        name='Sharp',
        marker_color='coral'
    ))
    fig.add_trace(go.Bar(
        x=zte.index,
        y=zte["RSRP"],
        name='ZTE',
        marker_color='khaki'
    ))
    fig.add_trace(go.Bar(
        x=pana.index,
        y=pana["RSRP"],
        name='Panasonic',
        marker_color='darkorange'
    ))
    fig.add_trace(go.Bar(
        x=qmobile.index,
        y=qmobile["RSRP"],
        name='Q Mobile',
        marker_color='rosybrown'
    ))
    fig.add_trace(go.Bar(
        x=vivo.index,
        y=vivo["RSRP"],
        name='Vivo',
        marker_color='deeppink'
    ))
    fig.add_trace(go.Bar(
        x=obi.index,
        y=obi["RSRP"],
        name='OBI',
        marker_color='hotpink'
    ))


    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(barmode='group', xaxis_tickangle=-45)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)