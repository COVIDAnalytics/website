import base64
from io import BytesIO
import pickle

import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL

from risk_calculator.infection.calculator import predict_risk_infec, get_languages
from risk_calculator.features import build_feature_cards, build_feature_importance_graph, oxygen_options
from risk_calculator.utils import build_lab_ques_card, labs_ques, valid_input, switch_oxygen, get_oxygen_info


def register_callbacks(app):
    with open('assets/risk_calculators/infection/model_with_lab.pkl', 'rb') as labs, \
            open('assets/risk_calculators/infection/model_without_lab.pkl', 'rb') as no_labs:
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
    oxygen_in_infec, oxygen_infec_ind = get_oxygen_info(no_labs_cols, no_labs_features["numeric"])

    # displaying shap image
    @app.server.route("/")
    def display_fig_infec(img):
        img_byte_arr = BytesIO()
        img.savefig(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        encoded = base64.b64encode(img_byte_arr)
        return 'data:image/png;base64,{}'.format(encoded.decode())

    @app.callback(
        Output('page-desc-infection', 'children'),
        [Input('language-calc-infection', 'value')])
    def infection_page_desc(language):
        return languages["page_desc_infection"][language]

    @app.callback(
        Output('lab_values_indicator_infection_text', 'children'),
        [Input('language-calc-infection', 'value')])
    def infection_labs_card(language):
        return build_lab_ques_card(language)

    @app.callback(
        Output('lab_values_indicator_infection', 'options'),
        [Input('language-calc-infection', 'value')])
    def infection_labs_card_options(language):
        return [{'label': labs_ques(x, language), 'value': x} for x in [1, 0]]

    @app.callback(
        Output('features-infection-text', 'children'),
        [Input('language-calc-infection', 'value')])
    def infection_labs_card_text(language):
        return html.H5(languages["insert_feat_text"][language])

    @app.callback(
        Output('infection-model-desc', 'children'),
        [Input('lab_values_indicator_infection', 'value'),
         Input('language-calc-infection', 'value')])
    def get_infection_model_desc(labs, language):
        return languages["technical_details_infection_labs"][language] if labs else \
            languages["technical_details_infection_no_labs"][language]

    if oxygen_in_infec:
        @app.callback(
            Output("calc-numeric-{}-wrapper-infection-nolabs".format(oxygen_infec_ind), 'children'),
            [Input('oxygen-answer-infection', 'value'),
             Input('language-calc-infection', 'value')])
        def get_oxygen_infection(have_val, language):
            return oxygen_options(
                oxygen_infec_ind,
                False,
                have_val,
                languages["oxygen"][language],
                language
            )

    @app.callback(
        Output('feature-importance-bar-graph-infection', 'children'),
        [Input('lab_values_indicator_infection', 'value')])
    def get_infection_model_feat_importance(labs):
        return build_feature_importance_graph(False, labs)

    @app.callback(
        Output('features-infection', 'children'),
        [Input('lab_values_indicator_infection', 'value'),
         Input('language-calc-infection', 'value')])
    def get_infection_model_feat_cards(labs, language):
        if labs:
            return build_feature_cards(labs_features, False, labs, language)
        return build_feature_cards(no_labs_features, False, labs, language)

    @app.callback(
        Output('submit-features-calc-infection', 'n_clicks'),
        [Input('lab_values_indicator_infection', 'value')])
    def reset_submit_button_infection(labs):
        return 0

    @app.callback(
        Output('submit-features-calc-infection', 'children'),
        [Input('language-calc-infection', 'value')])
    def set_submit_button_infection(language):
        return html.Div(children=[
            html.Div(className="material-icons",
                     children=["face"],
                     style={"display": "inline"}),
            languages["submit"][language],
        ])

    @app.callback(
        [Output('score-calculator-card-body-infection', 'children'),
         Output('calc-input-error-infection', 'children'),
         Output('imputed-text-infection', 'children'),
         Output('visual-1-infection', 'src'),
         Output('visual-1-infection', 'style'),
         Output('visual-1-infection-explanation', 'children')],
        [Input('language-calc-infection', 'value'),
         Input('submit-features-calc-infection', 'n_clicks'),
         Input('lab_values_indicator_infection', 'value')],
        [State({'type': 'infection', 'index': ALL}, 'value'),
         State({'type': 'temperature', 'index': ALL}, 'value')]
    )
    def calc_risk_score_infection(*argv):
        language = argv[0]
        default = html.H4(languages["results_card_infection"][language][0],
                          className="score-calculator-card-content-infection"),
        submit = argv[1]
        labs = argv[2]
        feats = argv[3:-1]
        temp_unit = argv[-1]
        if not labs and oxygen_in_infec:
            feats = switch_oxygen(feats, oxygen_infec_ind)
        # if submit button was clicked
        if submit > 0:
            x = feats
            if labs:
                valid, err, x = valid_input(labs_features["numeric"], x[0], len(labs_features["numeric"]), language)
            else:
                valid, err, x = valid_input(no_labs_features["numeric"], x[0], len(no_labs_features["numeric"]),
                                            language)
            if valid:
                if labs:
                    score_card, imputed, fig = predict_risk_infec(
                        labs_cols, labs_model, labs_features, labs_imputer, labs_explainer, x, temp_unit,
                        languages["results_card_infection"][language], language)
                else:
                    score_card, imputed, fig = predict_risk_infec(
                        no_labs_cols, no_labs_model, no_labs_features, no_labs_imputer, no_labs_explainer, x, temp_unit,
                        languages["results_card_infection"][language], language)
                if fig:
                    image = display_fig_infec(fig)
                else:
                    image = ''
                return score_card, '', imputed, image, {"height": 200}, languages["visual_1"][language]
            else:
                return default, err, '', '', {}, ''
        # user has not clicked submit
        return default, '', '', '', {}, ''
        # Add js callback here to refresh


