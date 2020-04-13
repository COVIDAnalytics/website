data_cols = [
    "Country",
    "Study Pop Size (N)",
    "Paper Title",
    "Peer-Reviewed? (As of 2 April 2020)",
    "Study length (days)",
    "Overall study population or subgroup?",
    "Subgroup",
    "Median Age",
    "Hypertension",
    "Diabetes",
    "Cardiovascular Disease (incl. CAD)",
    "Cerebrovascular Disease",
    "Renal Disease",
    "Chronic obstructive lung (COPD)",
    "Fever (temperature ≥37·3°C)",
    "Cough",
    "Fatigue",
    "Diarrhoea",
    "Shortness of Breath (dyspnoea)",
    "Nausea or Vomiting",
    "Loss of Appetite/Anorexia",
    "White Blood Cell Count (10^9/L) - Median",
    "Lymphocyte Count (10^9/L) - Median",
    "Platelet Count (10^9/L) - Median",
    "C-Reactive Protein (mg/L)",
    "Hemoglobin (g/L) - Median",
    "Total Bilirubin (umol/L) - Median",
    "D-Dimer (mg/L)",
    "Albumin (g/L)",
    "Uses Kaletra (lopinavir–ritonavir)",
    "Uses Arbidol (umifenovir)",
    "Corticosteroid (including Glucocorticoid, Methylprednisolone)",
    "Invasive mechanical ventilation",
    "ARDS",
    "Hospital admission (%)",
    "Discharged (%)",
    "Mortality",
    "Projected Mortality (accounting for patients not currently discharged)"
]

all_options = {
    'Comorbidities': [
        "Hypertension",
        "Diabetes",
        "Cardiovascular Disease (incl. CAD)",
        "Chronic obstructive lung (COPD)",
        "Cerebrovascular Disease",
        "Renal Disease",
    ],
    'Symptoms': [
        "Fever (temperature ≥37·3°C)",
        "Cough",
        "Fatigue",
        "Diarrhoea",
        "Shortness of Breath (dyspnoea)",
        "Nausea or Vomiting",
        "Loss of Appetite/Anorexia",
        "ARDS",
    ],
    'Treatment': [
        "Antiviral (Any)",
        "Uses Kaletra (lopinavir–ritonavir)",
        "Uses Arbidol (umifenovir)",
        "Corticosteroid (including Glucocorticoid, Methylprednisolone)",
        "Invasive mechanical ventilation",
    ],
    'Lab Test Results':[
        "White Blood Cell Count (10^9/L) - Median",
        "Lymphocyte Count (10^9/L) - Median",
        "Platelet Count (10^9/L) - Median",
        "C-Reactive Protein (mg/L)",
        "Hemoglobin (g/L) - Median",
        "Total Bilirubin (umol/L) - Median",
        "D-Dimer (mg/L)",
        "Albumin (g/L)"
    ],
}


states = {
    'US':'US','Alaska': 'AK', 'Alabama': 'AL', 'Arkansas': 'AR', 'American Samoa': 'AS',
    'Arizona': 'AZ', 'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT',
    'District of Columbia': 'DC', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Guam': 'GU', 'Hawaii': 'HI', 'Iowa': 'IA', 'Idaho': 'ID', 'Illinois': 'IL',
    'Indiana': 'IN', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA',
    'Massachusetts': 'MA', 'Maryland': 'MD', 'Maine': 'ME', 'Michigan': 'MI',
    'Minnesota': 'MN', 'Missouri': 'MO', 'Northern Mariana Islands': 'MP',
    'Mississippi': 'MS', 'Montana': 'MT', 'National': 'NA', 'North Carolina': 'NC',
    'North Dakota': 'ND', 'Nebraska': 'NE', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
    'New Mexico': 'NM', 'Nevada': 'NV', 'New York': 'NY', 'Ohio': 'OH', 'Oklahoma': 'OK',
    'Oregon': 'OR', 'Pennsylvania': 'PA', 'Puerto Rico': 'PR', 'Rhode Island': 'RI',
    'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX',
    'Utah': 'UT', 'Virginia': 'VA', 'Virgin Islands': 'VI', 'Vermont': 'VT',
    'Washington': 'WA', 'Wisconsin': 'WI', 'West Virginia': 'WV', 'Wyoming': 'WY'
    }


# colors that align with inferno
colors =[
            '#000004',
            '#e895a4',
            '#99747b',
            '#a80a29',
            '#f7d31d',
            '#913446'
        ]
