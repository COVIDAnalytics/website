from dash.dependencies import Input, Output, ALL

from policies.main import get_num_policies, build_policy_projections

def register_callbacks(app):
    num_policies = get_num_policies()
    options = \
        {
            'none': {
                'disabled':[{'label': '  No Restrictions', 'value': 'No_Measure', 'disabled': True}],
                'enabled':[{'label': '  No Restrictions', 'value': 'No_Measure', 'disabled': False}]
            },
            'lockdown': {
                'disabled':[{'label': '  Lockdown', 'value': 'Lockdown', 'disabled': True}],
                'enabled':[{'label': '  Lockdown', 'value': 'Lockdown', 'disabled': False}]
            },
            'mass': {
                'disabled':[{'label': '  Restrict Mass Gatherings', 'value': 'Mass_Gatherings', 'disabled': True}],
                'enabled':[{'label': '  Restrict Mass Gatherings', 'value': 'Mass_Gatherings', 'disabled': False}]
            },
            'schools': {
                'disabled':[{'label': '  Restrict Schools', 'value': 'Schools', 'disabled': True}],
                'enabled':[{'label': '  Restrict Schools', 'value': 'Schools', 'disabled': False}]
            },
            'others': {
                'disabled':[{'label': '  Restrict Non-Essential Businesses, Travel Restriction and Workplaces', 'value': 'Others', 'disabled': True}],
                'enabled':[{'label': '  Restrict Non-Essential Businesses, Travel Restriction and Workplaces', 'value': 'Others', 'disabled': False}]
            }
        }
    for p in range(num_policies):
        @app.callback(
            [Output({'type': 'none', 'index': p}, "options"),
            Output({'type': 'lockdown', 'index': p}, "options"),
            Output({'type': 'mass', 'index': p}, "options"),
            Output({'type': 'schools', 'index': p}, "options"),
            Output({'type': 'others', 'index': p}, "options")],
            [Input({'type': 'none', 'index': p}, "value"),
            Input({'type': 'lockdown', 'index': p}, "value"),
            Input({'type': 'mass', 'index': p}, "value"),
            Input({'type': 'schools', 'index': p}, "value"),
            Input({'type': 'others', 'index': p}, "value"),]
        )
        def update_policy_options(no_measure,lockdown,mass,schools,others):
            if no_measure:
                return [options['none']['enabled'],options['lockdown']['disabled'],options['mass']['disabled'],options['schools']['disabled'],options['others']['disabled']]
            if lockdown:
                return [options['none']['disabled'],options['lockdown']['enabled'],options['mass']['disabled'],options['schools']['disabled'],options['others']['disabled']]
            if mass:
                return [options['none']['disabled'],options['lockdown']['disabled'],options['mass']['enabled'],options['schools']['enabled'],options['others']['enabled']]
            if others:
                return [options['none']['disabled'],options['lockdown']['disabled'],options['mass']['enabled'],options['schools']['disabled'],options['others']['enabled']]
            return [options['none']['enabled'],options['lockdown']['enabled'],options['mass']['enabled'],options['schools']['disabled'],options['others']['enabled']]

        @app.callback(
            Output('policy-week-text-{}'.format(p), 'children'),
            [Input({'type': 'timeline', 'index': p}, "value")]
        )
        def get_text_for_timeline(t):
            if t == 0:
                return "Policy change taking effect now."
            if t == 1:
                return "Policy change taking effect 1 week from now."
            if t == 2:
                return "Policy change taking effect 2 weeks from now."
            if t == 3:
                return "Policy change taking effect 4 weeks from now."
            return "Policy change taking effect 6 weeks from now."

    @app.callback(
        [Output('policy_projection_graph', 'children'),
        Output('policy_deaths_projection_graph', 'children')],
        [Input('state_policies', "value"),
        Input({'type': 'none', 'index': ALL}, "value"),
        Input({'type': 'lockdown', 'index': ALL}, "value"),
        Input({'type': 'mass', 'index': ALL}, "value"),
        Input({'type': 'schools', 'index': ALL}, "value"),
        Input({'type': 'others', 'index': ALL}, "value"),
        Input({'type': 'none', 'index': ALL}, "options"),
        Input({'type': 'lockdown', 'index': ALL}, "options"),
        Input({'type': 'mass', 'index': ALL}, "options"),
        Input({'type': 'schools', 'index': ALL}, "options"),
        Input({'type': 'others', 'index': ALL}, "options"),
        Input({'type': 'timeline', 'index': ALL}, "value")]
    )
    def get_policy_projections(*argv):
        policy_options = 5
        input_policies = argv[1:policy_options+1]
        input_options = argv[policy_options+1:-1]
        times = argv[-1]
        policies = [[0,0,0,0,0] for i in range(num_policies)]
        for p in range(num_policies):
            for i in range(policy_options):
                if input_options[i][p]:
                    if input_policies[i][p] and not input_options[i][p][0]["disabled"]:
                        policies[p][i] = 1
        return [build_policy_projections(argv[0],policies,times,"Total Detected"),
                    build_policy_projections(argv[0],policies,times,"Total Detected Deaths")]
