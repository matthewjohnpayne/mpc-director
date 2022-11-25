''' 
tracklet_overlap_categories.py
 - defining tracklet overlap categories
 - these would be evaluated / defined by looking at the "obs_group" status for each constituent observation of a new tracklet

The "action_summary" field is trying to provide a concise description of what a processing pipeline should do with newly submitted tracklets of the specified type.


MJP 2022-11-09
'''

allowed_tracklet_overlap_categories = {
    'S' : { 'title'             : 'Single',
            'description'       : 'All observations are single, implying no overlap with previous submissions, implying all observations are new to the MPC.',
            'action_summary'    : 'If no suppd, send for attribution. If suppd, send for orbit-extension, X' },
            
    'D' : {  'title'            : 'Designation-Overlap',
            'description'       : 'All observations overlap with previously designated observations [NB: if multiple designations are overlapped, send to "problems"]',
            'action_summary'    : 'If the choice of primary-obs has changed for any obs, send for re-fitting' },
            
    'DS' : {  'title'           : 'Designation-Overlap + Single(s)',
            'description'       : 'A mixture of D & S (above), implying at least one observation is new to the MPC.',
            'action_summary'    : 'Send for orbit-extension, X'},

    'DIS' : {  'title'          : 'Designation-Overlap + ITF-Overlap + Single',
            'description'       : 'A mixture of I (below) & D (above) & S (above), implying that at least one observation is new to the MPC.',
            'action_summary'    : 'Send new data for orbit-extension, X, and perhaps try joining ITF w/ Desig as well (identification)' },

    'DI' : { 'title'            : 'Designation-Overlap + ITF-Overlap',
             'description'      : 'A mixture of I (below) & D (above).',
             'action_summary'   : 'Try joining ITF w/ Desig (identification)' },

    'IS' : {  'title'           : 'ITF-Overlap + Single(s)',
            'description'       : 'A mixture of I (below) & S (above), implying that at least one observation is new to the MPC.' ,
            'action_summary'    : 'Send for attribution'},
            
    'I' : {  'title'            : 'ITF-Overlap',
            'description'       : 'All observations overlap with observations already in the ITF, implying nothing new to the MPC.' ,
            'action_summary'    : 'Do nothing / to-itf? ' }
}
