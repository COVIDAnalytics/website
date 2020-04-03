import dash_bootstrap_components as dbc
import dash_html_components as html

def Navbar():
    # navbar = dbc.NavbarSimple(
    #       children=[
    #          dbc.NavbarToggler(id="navbar-toggler"),
    #          dbc.NavItem(dbc.NavLink("Projections", href="/projections")),
    #          dbc.NavItem(dbc.NavLink("Interactive Graphs", href="/interactive-graph")),
    #          dbc.DropdownMenu(
    #             nav=True,
    #             in_navbar=True,
    #             label="Dataset",
    #             children=[
    #                dbc.DropdownMenuItem("Download", href="/dataset"),
    #                dbc.DropdownMenuItem(divider=True),
    #                dbc.DropdownMenuItem("Documentation", href="/dataset_documentation"),
    #                      ],
    #                  ),
    #          dbc.DropdownMenu(
    #             nav=True,
    #             in_navbar=True,
    #             label="About Us",
    #             children=[
    #                dbc.DropdownMenuItem("The Team", href="/team"),
    #                dbc.DropdownMenuItem(divider=True),
    #                dbc.DropdownMenuItem("Contact Us", href="/contact"),
    #                      ],
    #                  ),
    #          html.A(
    #             # Use row and col to control vertical alignment of logo / brand
    #             dbc.Row(
    #                 [
    #                     dbc.Col(html.Img(src="assets/mit.png", height="40px")),
    #                     dbc.Col(html.Img(src="assets/orc.png", height="40px")),
    #                 ],
    #                 align="left",
    #                 no_gutters=True,
    #             ),
    #             href="https://orc.mit.edu/",
    #          ),
    #         ],
    #        brand=[html.Img(src="assets/mit.png", height="40px")],
    #        brand_href="/home",
    #        sticky="top",
    #        color="black",
    #        dark=True,
    #        )
    links = dbc.Row(
        [
                dbc.NavLink("Projections", href="/projections"),
                dbc.NavLink("Interactive Graphs", href="/interactive-graph"),
                dbc.DropdownMenu(
                   nav=True,
                   in_navbar=True,
                   label="Dataset",
                   children=[
                      dbc.DropdownMenuItem("Download", href="/dataset"),
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
                        dbc.Col(html.Img(src="assets/logo_black.png", height="80px")),
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
