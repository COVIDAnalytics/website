import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from navbar import Navbar

nav = Navbar()

body = dbc.Container(
    [
      dbc.Row(
        [
          dbc.Col(
            [
            html.H1("COVID-19"),
            html.H2("Insights")
            ]
          ),
        ],
        ),
       dbc.Row(
           [
               dbc.Col(
                  [
                      dcc.Graph(
                          figure={"data":
                                  [
                                      {
                                          "x": [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
                                          "y": [1, 4, 9, 20, 50, 100, 220, 500, 550, 550, 550, 400, 330, 300, 250]
                                      }
                                  ],
                                  "layout": {
                                      "title": "My Graph",
                                      "height": 300,
                                      'paper_bgcolor': 'gray',
                                      'plot_bgcolor': 'gray',
                                      'margin-top': 10
                                  },
                                  }
                             ),
                   ]
                 ),
              dbc.Col(
                 [
                     dcc.Graph(
                           figure={"data":
                                   [
                                       {
                                           "x": [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
                                           "y": [1, 4, 9, 20, 50, 100, 220, 500, 550, 550, 550, 400, 330, 300, 250]
                                       }
                                   ],
                                   "layout": {
                                       "title": "My Graph",
                                       "height": 300,
                                       'paper_bgcolor': 'gray',
                                       'plot_bgcolor': 'gray'
                                   },
                                   }
                            ),
                  ]
                ),
                dbc.Col(
                   [
                       dcc.Graph(
                             figure={"data":
                                     [
                                         {
                                             "x": [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
                                             "y": [1, 4, 9, 20, 50, 100, 220, 500, 550, 550, 550, 400, 330, 300, 250]
                                         }
                                     ],
                                     "layout": {
                                         "title": "My Graph",
                                         "height": 300,
                                         'paper_bgcolor': 'gray',
                                         'plot_bgcolor': 'gray'
                                     },
                                     }
                              ),
                    ]
                  ),
                ]
            ),
           dbc.Row(
               [
                   dbc.Col(
                      [
                          dcc.Graph(
                            figure={"data":
                                    [
                                        {
                                            "x": [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
                                            "y": [1, 4, 9, 20, 50, 100, 220, 500, 550, 550, 550, 400, 330, 300, 250]
                                        }
                                    ],
                                    "layout": {
                                        "title": "My Graph",
                                        "height": 300,
                                        'paper_bgcolor': 'gray',
                                        'plot_bgcolor': 'gray'
                                    },
                                    }
                                 ),
                       ]
                     ),
                  dbc.Col(
                     [
                         dcc.Graph(
                               figure={"data":
                                       [
                                           {
                                               "x": [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
                                               "y": [1, 4, 9, 20, 50, 100, 220, 500, 550, 550, 550, 400, 330, 300, 250]
                                           }
                                       ],
                                       "layout": {
                                           "title": "My Graph",
                                           "height": 300,
                                           'paper_bgcolor': 'gray',
                                           'plot_bgcolor': 'gray'
                                       },
                                       }
                                ),
                      ]
                    ),
                    dbc.Col(
                       [
                           dcc.Graph(
                                 figure={"data":
                                         [
                                             {
                                                 "x": [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
                                                 "y": [1, 4, 9, 20, 50, 100, 220, 500, 550, 550, 550, 400, 330, 300, 250]
                                             }
                                         ],
                                         "layout": {
                                             "title": "My Graph",
                                             "height": 300,
                                             'paper_bgcolor': 'gray',
                                             'plot_bgcolor': 'gray'
                                         },
                                         }
                                  ),
                        ]
                      ),
                    ]
                ),
       ],
className="insight_graphs",
)

def Graphs():
    layout = html.Div([
                    nav,
                    body
                    ])
    return layout

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED])
app.layout = Graphs()
app.title = "MIT_ORC_COVID19"
