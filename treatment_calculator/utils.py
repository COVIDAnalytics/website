import numpy as np
import pandas as pd
import math
import shap
import matplotlib
import matplotlib.pyplot as plt

import dash_html_components as html
from textwrap import wrap

from treatment_calculator.languages.english import English
import dash_core_components as dcc
import plotly.graph_objects as go

langs = [English()]
lang_names = {
    0: "English",
}
matplotlib.use('Agg')
oxygen = 'Oxygen Saturation'

treatments = ["Corticosteroids"]


def get_title_mapping():
    """Returns a dic that indexes language number with feature name translation. E.g. { 0: {'Age': 'Age'}, ... }"""
    return {num: lan.get_feature_names() for (num, lan) in zip(range(len(langs)), langs)}


def cvt_temp_c2f(x):
    return x*9/5+32


def labs_ques(exp, language):
    """Returns yes if exp evaluates to True"""
    return langs[language].get_yes(exp)


def oxygen_vals(val, language):
    """Returns yes if val == 92, else no"""
    return langs[language].get_yes(val == 92)


def get_oxygen_info(cols, feats):
    oxygen_in = "SaO2" in cols or 'ABG: Oxygen Saturation (SaO2)' in cols
    title_mapping = get_title_mapping()
    for i, f in enumerate(feats):
        if title_mapping[0][f["name"]] == oxygen:
            return oxygen_in, i
    return oxygen_in, None


# Validates the user input into calculator
def valid_input(numeric_features, user_features, language):
    title_mapping = get_title_mapping()
    missing = 0

    for i, user_feature in enumerate(user_features):
        f_name = user_feature["id"]["feature"]

        # Only check for numeric values
        if "numeric" in user_feature["id"]["index"]:
            user_val = user_feature["value"] if "value" in user_feature else None
            if user_val is None:
                if f_name == "Age":
                    return False, langs[language].prompt_missing_feature(f_name)
                # Change None to np.nan. +1 offset bec assume 1 catageorical at index 0
                user_features[i]["value"] = np.nan
                missing += 1
            else:
                # Find the json feature from numeric_features with the name of the current user feature
                numeric_feature = [f for f in numeric_features if f["name"] == f_name][0]

                # Lazy save the index for later (so we don't have to search the json again)
                user_features[i]["x-index"] = numeric_feature["index"]

                # Check if user provided input is within range
                min_val = numeric_feature["min_val"]
                max_val = numeric_feature["max_val"]
                if title_mapping[0][f_name] == oxygen and (user_val == 1 or user_val == 0):
                    continue
                if user_val < min_val or user_val > max_val:
                    return False, \
                        langs[language].outOfRangeValues.format(title_mapping[language][f_name], min_val, max_val),
    # user should give at least 2/3 of features
    threshold = math.floor(2 * len(numeric_features) / 3)
    if missing > threshold:
        return False, langs[language].notEnoughValues.format(threshold)
    return True, ""


# Uses model and features to predict score
def predict_risk(m, model, features, imputer, explainer, user_features, columns, language):
    x = [0] * len(model.feature_importances_)
    all_features = features["numeric"] + features["categorical"] + features["multidrop"]

    # Loop through all user provided features
    for feat in user_features:

        # Get name of current feature
        f_name = feat["id"]["feature"]

        # The index that this feature should be assigned to in the input vector, x
        index = -1

        # Check if cached index is there
        if "x-index" in feat:
            index = feat["x-index"]
        else:
            # If not, find the index
            json_feature = [f for f in all_features if f["name"] == f_name][0]
            if f_name != "Comorbidities":
                index = json_feature["index"]
            else:
                # Handle special case
                for comorb in feat["value"]:
                    c_idx = features["multidrop"][0]["vals"].index(comorb)
                    index = features["multidrop"][0]["index"][c_idx]
                    x[index] = 1
                continue

        # Assign value to right index in input vector
        x[index] = feat["value"]

    imputed = np.argwhere(np.isnan(x))
    x_full = imputer.transform([x])
    _X = pd.DataFrame(columns=columns, index=range(1), dtype=np.float)
    _X.loc[0] = x_full[0]
    score = model.predict_proba(_X)[:, 1]
    score = int(100*round(score[0], 2))
    impute_text = [''] * len(imputed)
    title_mapping = get_title_mapping()
    for i, ind in enumerate(imputed):
        ind = int(ind)
        temp = '°F' if columns[ind] == 'Body Temperature' else ''
        impute_text[i] = langs[language].missingFeatureTxt.format(
                title_mapping[language][columns[ind]],
                str(round(x_full[0][ind], 2)) + temp)

    impute_text = '  \n'.join(impute_text)
    shap_new = explainer.shap_values(_X)
    names = ['\n'.join(wrap(''.join(['{}'.format(title_mapping[language][c])]), width=12)) for c in columns]
    plot = shap.force_plot(
        np.around(explainer.expected_value, decimals=2),
        np.around(shap_new, decimals=2),
        np.around(_X, decimals=2),
        link="logit",
        matplotlib=True,
        show=False,
        feature_names=names
    )
    plt.axis('off')     # this rows the rectangular frame
    return score, impute_text, plot


def build_lab_ques_card(lang):
    return langs[lang].hasLabValues


def switch_oxygen(vec, ind):
    # assume there is only 1 categorical variable
    ind = ind + 1
    vec = list(vec)
    vals = vec[0]
    length = len(vals)
    if length > 0 and length > ind:
        oxy = vals[-1]
        n = len(vals)-1
        for i in range(n, ind, -1):
            vals[i] = vals[i-1]
        vals[ind] = oxy
        vec[0] = vals
        return tuple(vec)
    vec[0] = vals
    return tuple(vec)

treat_color = "#4141ff"
treat_high = "#8fc7ff"
ntreat_high = "#ff4141"
ntreat_color = "#d02532"

def build_vote_bar(should_treat, should_ntreat):
    nfig = go.Bar()
    nfig.x = [should_ntreat, should_treat]
    nfig.y = ["Should NOT Treat&nbsp;&nbsp;", "Should Treat&nbsp;&nbsp;"]
    nfig.textposition = "auto"
    nfig.orientation = 'h'
    nfig.width = [1, 1]
    nfig.marker.color = [ntreat_color, treat_color]
    nfig.text = ["<b>%s votes to skip Treatment</b>" % should_ntreat,
                    "<b>%s votes to do Treatment</b>" % should_treat]

    figure = go.Figure(
        data=[nfig],
        layout=go.Layout(
            title="Cumulative Voting Results",
            height=160,
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=60,
                pad=0
            ),
            bargap=1,
            bargroupgap = 0.05
        )
    )
    graph = dcc.Graph(
        figure=figure,
        config={
            'displayModeBar': False
        }
    )

    return  graph

def get_jumbo_text():
    return [
        html.H2("Evaluating ACEI / ARBS Treatments"),
        html.Hr(),
        dcc.Markdown(
            """
            There are many unanswered questions around how to most effectively treat COVID-19 patients. The
            medical community is investigating a variety of treatment options, including the repurposing
            of existing medications. One such group of medications is angiotensin-converting enzyme
            inhibitors (ACEIs) and angiotensin-receptor blockers (ARBs). These drugs are traditionally
            used to treat hypertension but have recently gained attention for mixed conclusions on their 
            effect on COVID-19 patients. The lack of consensus suggests that a "one-size-fits-all" approach 
            might be insufficient and that there could be a benefit to personalization of treatment decisions 
            for ACEI / ARBs in these patients. 
            
            The calculator below offers a machine learning-based approach
            for personalizing prescriptions of ACEI / ARBs for hospitalized, hypertensive patients with COVID-19. 
            We leverage several popular binary classification models to generate individualized predictions of 
            mortality / morbidity for each treatment alternative based on the clinical features entered by the 
            user. We then employ a voting scheme: each model "votes" whether to recommend ACEI / ARBs based
            on the predicted benefit of the drugs. An optional improvement threshold allows the user to select
            a necessary percent improvement with ACEI / ARBs that is required to vote for prescribing the drugs; 
            this is intended to limit unnecessary prescriptions. The final recommendation is based on the majority 
            vote of the individual methods. More details on the methodology and clinical insights are available 
            here, and the source code is available here.
            """
        )
    ]

def build_results_graph(results, names, thresh):

    tname = "ACEI / ARBS"
    groups = ["Without Treatment", "With Treatment"]
    traces = []

    model_map = {
        "rf": "Random Forest Class.",
        "cart": "Decision Tree Class.",
        "xgboost": "XGBoost Class.",
        "qda": "QuadDiscr. Analysis",
        "gb": "Gaussian NB"
    }
    #model_map = {x: "Treatment vs No Treatment<br>" + y for x, y in model_map.items()}

    xs = [model_map[name] for name in names]
    tfig = go.Bar()
    tfig.x = xs
    tfig.y = [results["treat"][name] * 100 for name in names]
    tfig.name = "Treat"
    tfig.textposition = "outside"
    #tfig.marker_color = "green"
    nfig = go.Bar()
    nfig.x = xs
    nfig.y = [results["ntreat"][name] * 100 for name in names]
    nfig.name = "Skip (Don't Treat)"
    nfig.textposition = "outside"

    tfig.marker.color = treat_color
    nfig.marker.color = ntreat_color

    thresh = int(thresh)
    print("THREA IS", thresh / 100)
    should_treat = [(t - n) / n <= -(thresh / 100) for t, n in zip(tfig.y, nfig.y)]

    tfig.text = ["<b>Treat</b>" if x else "" for x in should_treat]
    nfig.text = ["<b>Skip</b>" if not x else "" for x in should_treat]

    traces.append(tfig)
    traces.append(nfig)

    tfig.marker.line.color = treat_high
    nfig.marker.line.color = ntreat_high
    tfig.marker.line.width = [8 if x else 0 for x in should_treat]
    nfig.marker.line.width = [8 if not x else 0 for x in should_treat]


    bargap = 0.2
    layout = go.Layout(
        title="Recommendation per Model",
        yaxis_title="Mortality Rate in %",
        xaxis_title="Model Used",
        barmode='group',
        bargap=bargap,
        bargroupgap=0.05,
        margin=dict(
            t=60,
            b=20,
        ),
        #  showlegend=False,
    )
    figure = go.Figure(
        data=traces, layout=layout)

    graph = dcc.Graph(
        figure=figure
    )

    return html.Div([
        graph,
        build_vote_bar(should_treat.count(True), should_treat.count(False))
    ])

