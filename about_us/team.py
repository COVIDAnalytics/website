import yaml
import dash_html_components as html
import dash_bootstrap_components as dbc

from navbar import Navbar
from footer import Footer

def Team():
    nav = Navbar()
    footer = Footer()

    # Load team members
    with open("assets/team_members/core_team.yml") as f:
        core_members = yaml.load(f, Loader=yaml.FullLoader)
    num_core_members = len(core_members)

    with open("assets/team_members/associated_team.yml") as f:
        associated_members = yaml.load(f, Loader=yaml.FullLoader)
    num_associated_members = len(associated_members)

    with open("assets/team_members/faculty.yml") as f:
        faculty = yaml.load(f, Loader=yaml.FullLoader)
    num_faculty = len(faculty)

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
                        className="team-card-body",
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

    # Table rows
    core_member_rows = \
        [
            dbc.Row(
                [
                    member_pic(core_members[0])
                ],
                justify="around"
            )
        ] + \
        [
            dbc.Row(
                [
                    member_pic(core_members[i]) for i in range(1,num_core_members)
                ],
                justify="around",
            )
        ]

    faculty_rows = \
        [
            dbc.Row(
                [
                    member_pic(faculty[i]) for i in range(num_faculty)
                ],
                justify="around",
            )
        ]

    associated_member_rows = \
        [
            dbc.Row(
                [
                    member_pic(associated_members[i]) for i in range(num_associated_members)
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
            ] + \
            [dbc.Row([dbc.Col([html.H3("Core Team Members")])],style={'marginBottom': 20})] + \
            core_member_rows + \
            [dbc.Row([dbc.Col([html.H3("Collaborating Faculty")])],style={'marginBottom': 20,'marginTop': 40})] + \
            faculty_rows + \
            [dbc.Row([dbc.Col([html.H3("Associated Team Members")])],style={'marginBottom': 20,'marginTop': 40})] + \
            associated_member_rows,
            className="page-body"
        )


    layout = html.Div([nav, body, footer],className="site")
    return layout
