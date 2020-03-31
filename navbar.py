import dash_bootstrap_components as dbc
import dash_html_components as html

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"


def Navbar():
    navbar = dbc.NavbarSimple(
          children=[
             dbc.NavbarToggler(id="navbar-toggler"),
             dbc.NavItem(dbc.NavLink("Projections", href="/projections")),
             dbc.NavItem(dbc.NavLink("Interactive Graphs", href="/interactive-graph")),
             dbc.NavItem(dbc.NavLink("Insights", href="/insights")),
             dbc.NavItem(dbc.NavLink("Dataset", href="/dataset")),
             dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="About Us",
                children=[
                   dbc.DropdownMenuItem("The Team"),
                   dbc.DropdownMenuItem(divider=True),
                   dbc.DropdownMenuItem("Contact Us"),
                         ],
                     ),
             html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="assets/mit_image.png", height="40px")),
                        dbc.Col(html.Img(src="assets/orc_image.png", height="40px")),
                    ],
                    align="left",
                    no_gutters=True,
                ),
                href="https://orc.mit.edu/",
             ),
                   ],
           brand="Home",
           brand_href="/home",
           sticky="top",
           color="black",
           dark=True,
           )

    return navbar
