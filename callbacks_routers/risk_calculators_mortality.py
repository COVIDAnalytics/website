import os
import base64
from io import BytesIO
import pickle

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL

from risk_calculator.mortality.calculator import predict_risk_mort, get_languages
from risk_calculator.features import build_feature_cards, build_feature_importance_graph, oxygen_options
from risk_calculator.utils import build_lab_ques_card, labs_ques, valid_input, switch_oxygen, get_oxygen_info, \
    cvt_temp_c2f


def register_callbacks(app):
    with open('assets/risk_calculators/mortality/model_with_lab.pkl', 'rb') as labs, \
            open('assets/risk_calculators/mortality/model_without_lab.pkl', 'rb') as no_labs:
        labs = pickle.load(labs)
        no_labs = pickle.load(no_labs)
    labs_model = labs["model"]
    labs_features = labs["json"]
    labs_imputer = labs["imputer"]
    labs_explainer = labs["explainer"]
    labs_cols = labs["columns"]
    labs_auc = labs["AUC"]
    labs_population = [labs["Size Training"], labs["Size Test"]]
    labs_positive = [labs["Percentage Training"], labs["Percentage Test"]]
    no_labs_model = no_labs["model"]
    no_labs_features = no_labs["json"]
    no_labs_imputer = no_labs["imputer"]
    no_labs_explainer = no_labs["explainer"]
    no_labs_cols = no_labs["columns"]
    no_labs_auc = no_labs["AUC"]
    no_labs_population = [no_labs["Size Training"], no_labs["Size Test"]]
    no_labs_positive = [no_labs["Percentage Training"], no_labs["Percentage Test"]]

    languages = get_languages(
        labs_auc,
        labs_population,
        labs_positive,
        no_labs_auc,
        no_labs_population,
        no_labs_positive,
    )
    oxygen_in_mort, oxygen_mort_ind = get_oxygen_info(no_labs_cols, no_labs_features["numeric"])

    # displaying shap image
    @app.server.route("/")
    def display_fig_mort(img):
        img_byte_arr = BytesIO()
        img.savefig(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        encoded = base64.b64encode(img_byte_arr)
        return 'data:image/png;base64,{}'.format(encoded.decode())

    @app.callback(
        Output('page-desc-mortality', 'children'),
        [Input('language-calc-mortality', 'value')])
    def mortality_page_desc(language):
        return languages["page_desc_mortality"][language]

    @app.callback(
        Output('lab_values_indicator_text', 'children'),
        [Input('language-calc-mortality', 'value')])
    def mortality_labs_card(language):
        return build_lab_ques_card(language)

    @app.callback(
        Output('lab_values_indicator', 'options'),
        [Input('language-calc-mortality', 'value')])
    def mortality_labs_card_options(language):
        return [{'label': labs_ques(x, language), 'value': x} for x in [1, 0]]

    @app.callback(
        Output('features-mortality-text', 'children'),
        [Input('language-calc-mortality', 'value')])
    def mortality_labs_card_text(language):
        return languages["insert_feat_text"][language]

    @app.callback(
        Output('mortality-model-desc', 'children'),
        [Input('lab_values_indicator', 'value'),
         Input('language-calc-mortality', 'value')])
    def get_mortality_model_desc(labs, language):
        return languages["technical_details_mortality_labs"][language] if labs else \
            languages["technical_details_mortality_no_labs"][language]

    if oxygen_in_mort:
        @app.callback(
            Output("calc-numeric-{}-wrapper-mortality-nolabs".format(oxygen_mort_ind), 'children'),
            [Input('oxygen-answer-mortality', 'value'),
             Input('language-calc-mortality', 'value')])
        def get_oxygen_mortality(have_val, language):
            return oxygen_options(
                oxygen_mort_ind,
                True,
                have_val,
                languages["oxygen"][language],
                language
            )

    @app.callback(
        Output('feature-importance-bar-graph', 'children'),
        [Input('lab_values_indicator', 'value')])
    def get_mortality_model_feat_importance(labs):
        return build_feature_importance_graph(True, labs)

    @app.callback(
        Output('features-mortality', 'children'),
        [Input('lab_values_indicator', 'value'),
         Input('language-calc-mortality', 'value')])
    def get_mortality_model_feat_cards(labs, language):
        labs_to_use = labs_features if labs else no_labs_features
        return build_feature_cards(labs_to_use, True, labs, language)

    @app.callback(
        Output('submit-features-calc', 'n_clicks'),
        [Input('lab_values_indicator', 'value')])
    def reset_submit_button_mortality(labs):
        return 0

    @app.callback(
        Output('submit-features-calc', 'children'),
        [Input('language-calc-mortality', 'value')])
    def set_submit_button_mortality(language):
        return html.Div(children=[
            html.Div(className="material-icons",
                     children=["send"],
                     style={"display": "inline",
                            "verticalAlign": "middle"}
            ),
            html.Div(languages["submit"][language],
                     style={"fontSize": "24px",
                            "display": "inline",
                            "paddingLeft": "10px",
                            "verticalAlign": "middle"})
        ])

    @app.callback(
        [Output('score-calculator-card', 'children'),
         Output('calc-input-error', 'children'),
         Output('imputed-text-mortality', 'children'),
         Output('visual-1-mortality', 'src'),
         Output('visual-1-mortality', 'style'),
         Output('visual-1-mortality-explanation', 'children')],
        [Input('language-calc-mortality', 'value'),
         Input('submit-features-calc', 'n_clicks'),
         Input('lab_values_indicator', 'value')],
        [State({'type': 'mortality', 'feature': ALL, 'index': ALL}, 'value'),
          State({'type': 'temperature', 'index': ALL}, 'value')]
    )
    def calc_risk_score(*argv):
        language = argv[0]
        default = dbc.Card(
            color="dark",
            inverse=True,
            style={"height": "110px"},
            className="results-card elevation-3",
            children=[dbc.CardBody(
                html.H4(languages["results_card_mortality"][language], className="score-calculator-card-content"),
            )]
        )
        submit = argv[1]
        labs = argv[2]
        feats = argv[3:-1]
        print("input states")
        user_features = dash.callback_context.states_list[0]
        print(dash.callback_context.states_list)
        print("features")
        print(feats)

        temp_unit = argv[-1]
        if len(temp_unit) > 0 and temp_unit[0] == "°C":
            temp = [f for f in user_features if f["id"]["feature"] == "Body Temperature"][0]
            if temp is not None and "value" in temp:
                print(temp)
                print("Converting temp from " + str(temp["value"]))
                temp["value"] = cvt_temp_c2f(temp["value"])
                print("to " + str(temp["value"]))

        if not labs and oxygen_in_mort:
            feats = switch_oxygen(feats, oxygen_mort_ind)
        # if submit button was clicked
        if submit > 0:
            x = feats
            numeric_features = labs_features["numeric"] if labs else no_labs_features["numeric"]
            valid, err = valid_input(numeric_features, user_features, language)
            if valid:
                if labs:
                    score_card, imputed, fig = predict_risk_mort(
                        labs_cols, labs_model, labs_features, labs_imputer, labs_explainer,
                        user_features, languages["results_card_mortality"][language], language)
                else:
                    score_card, imputed, fig = predict_risk_mort(
                        no_labs_cols, no_labs_model, no_labs_features, no_labs_imputer, no_labs_explainer,
                        user_features, languages["results_card_mortality"][language], language)
                image = display_fig_mort(fig) if fig else ''
                default.children[0].children = score_card
                default.id = argv[1]
                return default, '', imputed, image, {"height": 200}, languages["visual_1"][language]
            else:
                return default, err, '', '', {}, ''
        # user has not clicked submit
        return default, '', '', '', {}, ''
