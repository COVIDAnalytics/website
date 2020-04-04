import dash_bootstrap_components as dbc
import dash_html_components as html

def Navbar():
    links = dbc.Row(
        [
                # dbc.NavLink("Projections", href="/projections"),
                dbc.DropdownMenu(
                   nav=True,
                   in_navbar=True,
                   label="Projections",
                   children=[
                      dbc.DropdownMenuItem("Graphs", href="/projections"),
                      dbc.DropdownMenuItem(divider=True),
                      dbc.DropdownMenuItem("Documentation", href="/projections_documentation"),
                    ],
                    style={"margin-bottom":20}
                ),
                dbc.NavLink("Interactive Graphs", href="/interactive-graph"),
                dbc.DropdownMenu(
                   nav=True,
                   in_navbar=True,
                   label="Dataset",
                   children=[
                      dbc.DropdownMenuItem("Data Access", href="/dataset"),
                      dbc.DropdownMenuItem(divider=True),
                      dbc.DropdownMenuItem("Documentation", href="/dataset_documentation"),
                    ],
                    style={"margin-bottom":20}
                ),
                dbc.DropdownMenu(
                   nav=True,
                   in_navbar=True,
                   label="About Us",
                   children=[
                      dbc.DropdownMenuItem("The Team", href="/team"),
                      dbc.DropdownMenuItem(divider=True),
                      dbc.DropdownMenuItem("Contact Us", href="/contact"),
                    ],
                    style={"margin-bottom":20}
                ),
            ],
            id="navbar-links",
            no_gutters=True,
            className="ml-auto flex-nowrap mt-3 mt-md-0",
            align="center",
        )

    navbar = dbc.Navbar(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="assets/logo_black.png", height="60px")),
                    ],
                    align="center",
                ),
                href="/home",
            ),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(links, id="navbar-collapse", navbar=True),
        ],
        color="black",
        dark=True,
    )

    return navbar
