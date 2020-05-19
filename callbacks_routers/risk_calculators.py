import os
import base64
from io import BytesIO

import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL

from risk_calculator.mortality.calculator import valid_input_mort, predict_risk_mort, get_mort_oxygen_cols
from risk_calculator.infection.calculator import valid_input_infec, predict_risk_infec, get_infec_oxygen_cols
from risk_calculator.features import build_feature_cards, build_feature_importance_graph, oxygen_options
from risk_calculator.utils import get_languages, build_lab_ques_card, labs_ques

def register_callbacks(app):
    languages = get_languages()
    oxygen_in_infec, oxygen_infec_ind = get_infec_oxygen_cols()
    oxygen_in_mort, oxygen_mort_ind = get_mort_oxygen_cols()
    #displaying shap image
    @app.server.route("/")
    def display_fig(img, close_all=True):
        imgByteArr = BytesIO()
        img.savefig(imgByteArr, format='PNG')
        imgByteArr = imgByteArr.getvalue()
        encoded=base64.b64encode(imgByteArr)
        return 'data:image/png;base64,{}'.format(encoded.decode())

    @app.callback(
        Output('page-desc-infection', 'children'),
        [Input('language-calc-infection', 'value')])
    def infection_page_desc(language):
        return languages["page_desc_infection"][language]

    @app.callback(
        Output('page-desc-mortality', 'children'),
        [Input('language-calc-mortality', 'value')])
    def mortality_page_desc(language):
        return languages["page_desc_mortality"][language]

    @app.callback(
        Output('lab_values_indicator_infection_text', 'children'),
        [Input('language-calc-infection', 'value')])
    def infection_labs_card(language):
        return build_lab_ques_card(language)

    @app.callback(
        Output('lab_values_indicator_text', 'children'),
        [Input('language-calc-mortality', 'value')])
    def mortality_labs_card(language):
        return build_lab_ques_card(language)

    @app.callback(
        Output('lab_values_indicator_infection', 'options'),
        [Input('language-calc-infection', 'value')])
    def infection_labs_card_options(language):
        return [{'label': labs_ques(x,language), 'value': x} for x in [1,0]]

    @app.callback(
        Output('lab_values_indicator', 'options'),
        [Input('language-calc-mortality', 'value')])
    def mortality_labs_card_options(language):
        return [{'label': labs_ques(x,language), 'value': x} for x in [1,0]]

    @app.callback(
        Output('features-infection-text', 'children'),
        [Input('language-calc-infection', 'value')])
    def infection_labs_card_text(language):
        return html.H5(languages["insert_feat_text"][language])

    @app.callback(
        Output('features-mortality-text', 'children'),
        [Input('language-calc-mortality', 'value')])
    def mortality_labs_card_text(language):
        return html.H5(languages["insert_feat_text"][language])

    @app.callback(
        Output('infection-model-desc', 'children'),
        [Input('lab_values_indicator_infection', 'value'),
        Input('language-calc-infection', 'value')])
    def get_infection_model_desc(labs,language):
        return languages["technical_details_infection_labs"][language] if labs else languages["technical_details_infection_no_labs"][language]

    @app.callback(
        Output('mortality-model-desc', 'children'),
        [Input('lab_values_indicator', 'value'),
        Input('language-calc-mortality', 'value')])
    def get_mortality_model_desc(labs,language):
        return languages["technical_details_mortality_labs"][language] if labs else languages["technical_details_mortality_no_labs"][language]

    if oxygen_in_mort:
        @app.callback(
            Output("calc-numeric-{}-wrapper-mortality-nolabs".format(oxygen_mort_ind), 'children'),
            [Input('oxygen-answer-mortality', 'value'),
            Input('language-calc-mortality', 'value')])
        def get_oxygen_mortality(have_val,language):
            return oxygen_options(
                    oxygen_mort_ind,
                    True,
                    have_val,
                    languages["oxygen"][language],
                    language
                )

    if oxygen_in_infec:
        @app.callback(
            Output("calc-numeric-{}-wrapper-infection-nolabs".format(oxygen_infec_ind), 'children'),
            [Input('oxygen-answer-infection', 'value'),
            Input('language-calc-infection', 'value')])
        def get_oxygen_infection(have_val,language):
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
        return build_feature_importance_graph(False,labs)
        # if labs:
        #     image = display_fig(labs_importance_infec)
        # else:
        #     image = display_fig(no_labs_importance_infec)
        # return image

    @app.callback(
        Output('feature-importance-bar-graph', 'children'),
        [Input('lab_values_indicator', 'value')])
    def get_mortality_model_feat_importance(labs):
        return build_feature_importance_graph(True,labs)
        # if labs:
        #     image = display_fig(labs_importance_mort)
        # else:
        #     image = display_fig(no_labs_importance_mort)
        # return image

    @app.callback(
        Output('features-infection', 'children'),
        [Input('lab_values_indicator_infection', 'value'),
        Input('language-calc-infection', 'value')])
    def get_infection_model_feat_cards(labs,language):
        return build_feature_cards(False,labs,language)

    @app.callback(
        Output('features-mortality', 'children'),
        [Input('lab_values_indicator', 'value'),
        Input('language-calc-mortality', 'value')])
    def get_mortality_model_feat_cards(labs,language):
        return build_feature_cards(True,labs,language)

    @app.callback(
        Output('submit-features-calc-infection', 'n_clicks'),
        [Input('lab_values_indicator_infection', 'value')])
    def reset_submit_button_infection(labs):
        return 0

    @app.callback(
        Output('submit-features-calc', 'n_clicks'),
        [Input('lab_values_indicator', 'value')])
    def reset_submit_button_mortality(labs):
        return 0

    @app.callback(
        Output('submit-features-calc-infection', 'children'),
        [Input('language-calc-infection', 'value')])
    def set_submit_button_infection(language):
        return languages["submit"][language],

    @app.callback(
        Output('submit-features-calc', 'children'),
        [Input('language-calc-mortality', 'value')])
    def set_submit_button_mortality(language):
        return languages["submit"][language],

    def switch_oxygen(vec,ind):
        #assume there is only 1 categorical variable
        ind = ind + 1
        vec = list(vec)
        vals = vec[0]
        length = len(vals)
        if length > 0 and length > ind:
            oxygen = vals[-1]
            n = len(vals)-1
            for i in range(n,ind,-1):
                vals[i] = vals[i-1]
            vals[ind] = oxygen
            vec[0] = vals
            return tuple(vec)
        vec[0] = vals
        return tuple(vec)

    @app.callback(
        [Output('score-calculator-card-body', 'children'),
        Output('calc-input-error', 'children'),
        Output('imputed-text-mortality', 'children'),
        Output('visual-1-mortality', 'src'),
        Output('visual-1-mortality', 'style'),
        Output('visual-1-mortality-explanation', 'children')],
        [Input('language-calc-mortality', 'value'),
        Input('submit-features-calc', 'n_clicks'),
        Input('lab_values_indicator', 'value')],
        [State({'type': 'mortality', 'index': ALL}, 'value'),
        State({'type': 'temperature', 'index': ALL}, 'value')]
    )
    def calc_risk_score(*argv):
        language = argv[0]
        default = html.H4(languages["results_card_mortality"][language],className="score-calculator-card-content"),
        submit = argv[1]
        labs = argv[2]
        feats = argv[3:-1]
        temp_unit = argv[-1]
        if not labs and oxygen_in_mort:
            feats = switch_oxygen(feats,oxygen_mort_ind)
        #if submit button was clicked
        if submit > 0:
            x = feats
            valid, err, x = valid_input_mort(labs,x,language)
            if valid:
                score, imputed, fig = predict_risk_mort(labs,x,temp_unit,languages["results_card_mortality"][language],language)
                if fig:
                    image = display_fig(fig)
                else:
                    image = ''
                return score,'',imputed,image,{"height":200},languages["visual_1"][language]
            else:
                return default,err,'','',{},''
        #user has not clicked submit
        return default,'','','',{},''

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
        default = html.H4(languages["results_card_infection"][language][0],className="score-calculator-card-content-infection"),
        submit = argv[1]
        labs = argv[2]
        feats = argv[3:-1]
        temp_unit = argv[-1]
        if not labs and oxygen_in_infec:
            feats = switch_oxygen(feats,oxygen_infec_ind)
        #if submit button was clicked
        if submit > 0:
            x = feats
            valid, err, x  = valid_input_infec(labs,x,language)
            if valid:
                score, imputed, fig = predict_risk_infec(labs,x,temp_unit,languages["results_card_infection"][language],language)
                if fig:
                    image = display_fig(fig)
                else:
                    image = ''
                return score,'',imputed,image,{"height":200},languages["visual_1"][language]
            else:
                return default,err,'','',{},''
        #user has not clicked submit
        return default,'','','',{},''
