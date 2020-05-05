
["Mass Gatherings", "Schools", "Others", "Lockdown"]

policy_mapping = {
    [0,0,0,0]: 'No_Measure',
    [1,0,0,0]: 'Restrict_Mass_Gatherings',
    [0,0,1,0]: 'Mass_Gatherings_Authorized_But_Others_Restricted',
    [1,1,0,0]: 'Restrict_Mass_Gatherings_and_Schools',
    [1,0,1,0]: 'Authorize_Schools_but_Restrict_Mass_Gatherings_and_Others',
    [1,1,1,0]: 'Restrict_Mass_Gatherings_and_Schools_and_Others' ,
    [0,0,0,1]: 'Lockdown':
    }
