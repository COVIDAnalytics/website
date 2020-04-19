import dash_bootstrap_components as dbc
import dash_html_components as html

def Navbar():
    links = dbc.Row(
        [
                dbc.DropdownMenu(
                   color="link",
                   label="Dataset",
                   children=[
                      dbc.DropdownMenuItem("Data", href="/dataset"),
                      dbc.DropdownMenuItem(divider=True),
                      dbc.DropdownMenuItem("Insights", href="/interactive-graph"),
                    ],
                    style={"paddingTop": 30,"paddingBottom": 20}
                ),
                dbc.DropdownMenu(
                   color="link",
                   label="Projections",
                   children=[
                      dbc.DropdownMenuItem("Case Predictions", href="/projections"),
                      dbc.DropdownMenuItem(divider=True),
                      dbc.DropdownMenuItem("Ventilator Allocation", href="/ventilator_allocation"),
                    ],
                    style={"paddingTop": 30,"paddingBottom": 20}
                ),
                dbc.NavLink("Mortality Risk Calculator", href="/calculator",style={"paddingTop": 30,"paddingBottom": 20}),
                dbc.DropdownMenu(
                   color="link",
                   label="About Us",
                   children=[
                      dbc.DropdownMenuItem("The Team", href="/team"),
                      dbc.DropdownMenuItem(divider=True),
                      dbc.DropdownMenuItem("Contact Us", href="/contact"),
                    ],
                    style={"paddingTop": 30,"paddingBottom": 20}
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
                        dbc.Col(html.Img(src="assets/images/logo_black.png", height="60px")),
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
