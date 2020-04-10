### Data
import yaml
### Dash
import dash_html_components as html
import dash_bootstrap_components as dbc

from navbar import Navbar
from footer import Footer

nav = Navbar()
footer = Footer()

# Load team members
with open("assets/team_members/team.yml") as f:
    members = yaml.load(f, Loader=yaml.FullLoader)
num_members = len(members)

with open("assets/collaborators/organizations.yml") as f:
    collaborators = yaml.load(f, Loader=yaml.FullLoader)
num_collaborators = len(collaborators)

# Single member pic
def member_pic(member):
    return dbc.Col(
        [
            dbc.Card(
            [
                dbc.CardImg(src='assets/team_members/photos/%s' % member['photo']),
                dbc.CardBody(
                    html.A(member['name'],
                           href=member['website'],
                           className="stretched-link team-name"),
                ),
             ],
             className="team-card h-100 w-100"
            )
        ],
        xs=12,
        sm=6,
        md=3,
        lg=3,
        xl=2,
        style={'marginBottom': 7}
    )

# Single collaborator pic
def collab_pic(collaborator):
    return dbc.Col(
        [   
        html.A([
            html.Div(
            [
                html.Img(
                    src='assets/collaborators/photos/%s' % collaborator['photo'],
                    className="collabs"
                ),
             ],
             style={'display': 'inline-block'}
            )
            ], href=collaborator['website'])
        ],
        width='auto',
    )

# Table rows
member_rows = \
    [
        dbc.Row(
            [
                member_pic(members[0])
            ],
            justify="around"
        )
    ] + \
    [
        dbc.Row(
            [
                member_pic(members[i]) for i in range(1,num_members)
            ],
            justify="around",
        )
    ]

collab_rows = \
    [
        dbc.Row(
            [
                collab_pic(collaborators[i]) for i in range(num_collaborators)
            ],
            justify="around",
        )
    ]

body = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                    [
                        html.H2("Our Team"),
                        html.P('Our team comprises passionate researchers in Operations Research \
                        and Analytics. We are eager to use our collective skills and create new \
                        tools that can help the scientific community fight against the pandemic.')
                    ]
                    )
                ],
                style={'marginBottom': 20}
            )
        ] + member_rows +
        [dbc.Row(
            [
                dbc.Col(
                [
                    html.H2("Our Collaborators"),
                ]
                )
            ],
            style={'margin-bottom': 20,'margin-top': 40}
        )
        ] + collab_rows,
        className="page-body"
    )

def Team():
    layout = html.Div([nav, body, footer],className="site")
    return layout
