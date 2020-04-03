### Data
import pandas as pd
import pickle
from datetime import datetime as dt
### Graphing
import plotly.graph_objects as go
### Dash
import dash
import flask
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

from navbar import Navbar
from footer import Footer
from interactive import demographics

nav = Navbar()
footer = Footer()

body = dbc.Container([
	dbc.Row(
        [
			dbc.Col([
				html.H1("COVID-19 Analytics"),
            	html.H2("Covid-19 Aggregated Clinical Dataset Documentation"),
                html.P('In the fog of war of the Covid-19 pandemic, a critical factor inhibiting effective decision making at regional, national, and global levels is a lack of relevant data on patient outcomes. We hope to partially alleviate this problem by sharing the following dataset, which aggregates data from over 100 published clinical studies and preprints released between December 2019 and March 2020. For each paper, a MIT researcher read the paper and gathered relevant numerical data from tables and from the text into a standard format.'),
                html.P('We would like to remind the reader that the raw data in this dataset should not be used to estimate trends in the general population such as mortality rates. Indeed, this dataset is largely derived from studies run in hospitals and nations affected with SARS-COV-2 generally only admit seriously affected patients to hospitals. However, it should be possible to derive reasonably accurate estimates of these quantities by (a) accounting for the prevalence of asymptomatic patients, and (b) only including sufficiently representative studies.'),
				html.P('At a high level, each row of the dataset represents a cohort of patients. Some papers study a single cohort, while others study several cohorts, and still others report results about one cohort and one or more subcohorts; all of these are included as rows in the dataset. Given a cohort, each column represents information about this cohort of patients, divided roughly in the following categories:'),
				dcc.Markdown(''' 
					1. demographic information (e.g. number of patients in the cohort, aggregated age and gender statistics)
					2. comorbidity information (e.g. prevalence of diabetes, hypertension, etc.)
					3. symptoms (including fever, cough, sore throat, etc.)
					4. treatments (including antibiotics, intubation, etc.)
					5. standard labs (including lymphocyte count, platelets, etc.)
					6. outcomes (including discharge, hospital length of stay, death, etc.)
					'''),
				html.P('This data aggregates data from different hospitals across the world, which may have different equipment and reporting standards. It was obtained through a human reading process, which is inherently imperfect. In addition, we often chose to prioritize standardizing information across papers over perfect accuracy. We list some important observations about the data below.'),
				dcc.Markdown(''' 
					1. The data in this spreadsheet includes data from preprints which have not yet been subject to peer review. We have chosen to include these studies because the additional predictive power from having 2-3 times more data outweighs the potential for errors in these data points. However, we remind the reader that caution should be taken when using data which has not yet been subject to peer review.
					2. To minimize human error in data reporting, we have verified some key features with additional scrutiny, including mortality, ICU and hospital length of stay, key symptoms (fever, cough, short breath, fatigue, diarrhea) and common comorbidities (hypertension, diabetes).
					3. Across papers, subcohort divisions may follow different criteria (which may be of independent interest), including: severity of disease (severe vs. mild), death (survivors vs. non-survivors), treatment (intubation vs. non-intubation), comorbidity (diabetic vs. non-diabetic).
					4. Papers are not consistent on their reporting of mortality or discharge rates. Some only report mortality; others report only discharges; many patients remain in the hospital at the conclusion of the study.
					5. Studies in this dataset do not always have the same purpose, which affects data reporting. For instance, many papers from Italy seem to report data only on non-survivors. In addition, some studies focus on the disease’s contagion profile, with little information on death, discharge, stay length. Data points from these studies may exhibit a high proportion of missing features.
					6. To the best of our ability, we avoid reporting data from metastudies to avoid double-counting patients. However, there remains a (low) risk that some patients will appear in multiple studies (for example two studies in Feb and Mar in the same hospital).
					7. We intend to continuously update this dataset, for the duration of this epidemic. If you spot any errors in the dataset, or know of any papers which you believe this dataset would benefit from including, please do not hesitate to contact us, either by filing an issue in our GitHub repo, or emailing us at covidanalytics@mit.edu.
					'''),
			])
		 ]
	 ),
])

def Dataset_documentation():
    layout = html.Div([nav, body, footer])
    return layout

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED])
app.layout = Dataset_documentation()
app.title = "MIT_ORC_COVID19"
