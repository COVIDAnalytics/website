### Data
import pandas as pd
import pickle
### Graphing
import plotly.graph_objects as go
### Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
# Navbar
from navbar import Navbar

nav = Navbar()

body = dbc.Container(
    [
      dbc.Row(
        [
          dbc.Col(
            [
            html.H1("COVID-19"),
            html.H5("Our Team comprises of passionate researchers in Analytics!")
            ]
          ),
        ],
        ),
       dbc.Row(
               [dbc.Col(
               	  [html.Div([
               	    html.Img(src='assets/team_members/Boussioux_Leonard.jpg',
               	  					  id='Boussioux_Leonard',
               	  					  alt='Image Missing',
               	  					  width='100%'),
               	    dbc.Button("Boussioux Leonard",
            							color="info",
            							block=True,
            							id="button",
            							className="mb-3",
            							href="https://sites.google.com/view/leonardboussioux/"
        					)],style = {'display': 'inline-block', 'width': '100%'})]
               	),
               	dbc.Col(
               	  [html.Div([
               	    html.Img(src='assets/team_members/Cory_Wright_Ryan.jpg',
               	  					  id='Cory_Wright_Ryan',
               	  					  alt='Image Missing',
               	  					  width='100%'),
               	    dbc.Button("Cory Wright Ryan",
            							color="info",
            							block=True,
            							id="button",
            							className="mb-3",
            							href="https://ryancorywright.github.io/"
        					)],style = {'display': 'inline-block', 'width': '100%'})]
               	),
               	dbc.Col(
               	  [html.Div([
               	    html.Img(src='assets/team_members/Delarue_Arthur.jpg',
               	  					  id='Digalakis_Vasileios',
               	  					  alt='Image Missing',
               	  					  width='100%'),
               	    dbc.Button("Digalakis Vasileios",
            							color="info",
            							block=True,
            							id="button",
            							className="mb-3",
        					)],style = {'display': 'inline-block', 'width': '100%'})]
               	),
               dbc.Col(
               	  [html.Div([
               	    html.Img(src='assets/team_members/Digalakis_Vasileios.jpg',
               	  					  id='Digalakis_Vasileios',
               	  					  alt='Image Missing',
               	  					  width='100%'),
               	    dbc.Button("Digalakis Vasileios",
            							color="info",
            							block=True,
            							id="button",
            							className="mb-3",
        					)],style = {'display': 'inline-block', 'width': '100%'})]
               	),
               dbc.Col(
               	  [html.Div([
               	    html.Img(src='assets/team_members/Gilmour_Samuel.jpg',
               	  					  id='Gilmour_Samuel',
               	  					  alt='Image Missing',
               	  					  width='100%'),
               	    dbc.Button("Gilmour Samuel",
            							color="info",
            							block=True,
            							id="button",
            							className="mb-3",
        					)],style = {'display': 'inline-block', 'width': '100%'})]
               	),

			    ]),
        dbc.Row(
            [
            dbc.Col(
               	  [html.Div([
               	    html.Img(src='assets/team_members/Graham_Justin.jpg',
               	  					  id='Graham_Justin',
               	  					  alt='Image Missing',
               	  					  width='100%'),
               	    dbc.Button("Graham Justin",
            							color="info",
            							block=True,
            							id="button",
            							className="mb-3",
        					)],style = {'display': 'inline-block', 'width': '100%'})]
               	),
            dbc.Col(
               	  [html.Div([
               	    html.Img(src='assets/team_members/Kim_Adam.jpg',
               	  					  id='Kim_Adam',
               	  					  alt='Image Missing',
               	  					  width='100%'),
               	    dbc.Button("Kim Adam",
            							color="info",
            							block=True,
            							id="button",
            							className="mb-3",
        					)],style = {'display': 'inline-block', 'width': '100%'})]
               	),
            dbc.Col(
               	  [html.Div([
               	    html.Img(src='assets/team_members/Lahlou_Kitane_Driss.jpg',
               	  					  id='Lahlou_Kitane_Driss',
               	  					  alt='Image Missing',
               	  					  width='100%'),
               	    dbc.Button("Lahlou Kitane Driss",
            							color="info",
            							block=True,
            							id="button",
            							className="mb-3",
        					)],style = {'display': 'inline-block', 'width': '100%'})]
               	),
            dbc.Col(
               	  [html.Div([
               	    html.Img(src='assets/team_members/Stellato_Bartolomeo.jpg',
               	  					  id='Stellato_Bartolomeo',
               	  					  alt='Image Missing',
               	  					  width='100%'),
               	    dbc.Button("Stellato Bartolomeo",
            							color="info",
            							block=True,
            							id="button",
            							className="mb-3",
        					)],style = {'display': 'inline-block', 'width': '100%'})]
               	),
            dbc.Col(
               	  [html.Div([
               	    html.Img(src='assets/team_members/Wiberg_Holly.jpg',
               	  					  id='Wiberg_Holly',
               	  					  alt='Image Missing',
               	  					  width='100%'),
               	    dbc.Button("Wiberg Holly",
            							color="info",
            							block=True,
            							id="button",
            							className="mb-3",
        					)],style = {'display': 'inline-block', 'width': '100%'})]
               	),
	    		]),

       ],
)



def Team():
    layout = html.Div(
    [
        nav,
        body
    ])
    return layout

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED])
app.layout = Team()
app.title = "MIT_ORC_COVID19"