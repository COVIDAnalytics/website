import dash_bootstrap_components as dbc
import dash_html_components as html

def Navbar():
    links = dbc.Row(
        [
                dbc.DropdownMenu(
                    className = "nav-links-dd",
                    color="link",
                    label="Dataset",
                    children=[
                      dbc.DropdownMenuItem("Data", href="/dataset"),
                      dbc.DropdownMenuItem(divider=True),
                      dbc.DropdownMenuItem("Insights", href="/interactive-graph"),
                    ],
                ),
                dbc.DropdownMenu(
                    className = "nav-links-dd",
                    color="link",
                    label="Projections",
                    children=[
                      dbc.DropdownMenuItem("Case Predictions", href="/projections"),
                      dbc.DropdownMenuItem(divider=True),
                      dbc.DropdownMenuItem("Ventilator Allocation", href="/ventilator_allocation"),
                    ],
                ),
                dbc.DropdownMenu(
                    className = "nav-links-dd",
                    color="link",
                    label="Risk Calculators",
                    children=[
                       dbc.DropdownMenuItem("Mortality Risk Calculator", href="/mortality_calculator"),
                       # dbc.DropdownMenuItem(divider=True),
                       # dbc.DropdownMenuItem("Infection Risk Calculator", href="/infection_calculator")
                       ]
                ),
                dbc.DropdownMenu(
                    className = "nav-links-dd",
                    color="link",
                    label="About Us",
                    children=[
                      dbc.DropdownMenuItem("The Team", href="/team"),
                      dbc.DropdownMenuItem(divider=True),
                      dbc.DropdownMenuItem("Collaborators", href="/collaborators"),
                      dbc.DropdownMenuItem(divider=True),
                      dbc.DropdownMenuItem("Contact Us", href="/contact"),
                    ],
                ),
                dbc.Button(
                    "In the Press",
                    className = "nav-links-dd",
                     color="link", href="/press",
                    ),
            ],
            id="navbar-links",
            style={"position":"static"},
            no_gutters=True,
            className="ml-auto",
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
