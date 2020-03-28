import dash_bootstrap_components as dbc

def Navbar():
    navbar = dbc.NavbarSimple(
          children=[
             dbc.NavItem(dbc.NavLink("Interactive Graphs", href="/interactive-graph")),
             dbc.NavItem(dbc.NavLink("Insights", href="/insights")),
             dbc.NavItem(dbc.NavLink("Predictive Models", href="/models")),
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
                   ],
           brand="Home",
           brand_href="/home",
           sticky="top",
           )
    return navbar
