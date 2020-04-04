import dash_bootstrap_components as dbc
import dash_html_components as html

def Navbar():
    links = dbc.Row(
        [
                dbc.DropdownMenu(
                   in_navbar=True,
                   className="projections-nav",
                   color="link",
                   label="Projections",
                   children=[
                      dbc.DropdownMenuItem("Graphs", href="/projections"),
                      dbc.DropdownMenuItem(divider=True),
                      dbc.DropdownMenuItem("Documentation", href="/projections_documentation"),
                    ],
                ),
                dbc.NavLink("Interactive Graphs", href="/interactive-graph"),
                dbc.DropdownMenu(
                   in_navbar=True,
                   color="link",
                   label="Dataset",
                   children=[
                      dbc.DropdownMenuItem("Data Access", href="/dataset"),
                      dbc.DropdownMenuItem(divider=True),
                      dbc.DropdownMenuItem("Documentation", href="/dataset_documentation"),
                    ],
                ),
                dbc.DropdownMenu(
                   in_navbar=True,
                   color="link",
                   label="About Us",
                   children=[
                      dbc.DropdownMenuItem("The Team", href="/team"),
                      dbc.DropdownMenuItem(divider=True),
                      dbc.DropdownMenuItem("Contact Us", href="/contact"),
                    ],
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
        id="navbar",
        color="black",
        dark=True,
    )

    return navbar
