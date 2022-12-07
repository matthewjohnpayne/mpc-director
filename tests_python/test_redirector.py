'''
These tests all use simplified synthetic inputs
 - They only test the "destination"/"result" that is returned when given perfect, simplified inputs. 


'''

# ----- Imports --------------------------------
#import mpc_director as redirector
import sys, os 
sys.path.append("../mpc_director/")
import redirector as redirector

import pytest









# ----- Test NEW-decision function --------------
def test_decision_func_NEW_A():
  
  # loop over expected inputs & corresponding expected output "destinations"
  # NB: tuple of input_values ==>> tracklet_overlap_category, overlapped_uppd_list, suppd, new_data
  input_values  = [
    ('S', [], '', True),
    ('S', [], '2022 AB', True),
    
    ('D', ['2022 AB'], '', True),
    ('D', ['2022 AB'], '2022 AB', True),
    ('D', ['2022 AB'], '2022 CD', True),
    
    ('D', ['2022 AB'], '', False),
    
    ('D', ['2022 AB', '2022 XY'], '', True),
    ('DS', ['2022 AB', '2022 XY'], '', True),
    ('DIS', ['2022 AB', '2022 XY'], '', True),
    ('DI', ['2022 AB', '2022 XY'], '', True),

    ('DS', ['2022 AB'], '', True),
    ('DS', ['2022 AB'], '2022 AB', True),
    ('DS', ['2022 AB'], '2022 CD', True),

    ('DI', ['2022 AB'], '', True),
    ('DIS', ['2022 AB'], '', True),
    ('DIS', ['2022 AB'], '2022 CD', True),

    ('I', [], '', True),
    ('I', [], '2022 AB', True),
    ('I', [], '2022 AB', False),

                    ]
  expected_values = [
    {'destination': 'ATT'},                     #S
    {'destination': 'X', 'suppd':'2022 AB'},    #S
    
    {'destination': 'X', 'suppd':'2022 AB'},    #D
    {'destination': 'X', 'suppd':'2022 AB'},    #D
    {'destination': 'X', 'suppd':'2022 AB'},    #D

    {'destination': 'SUBORDINATE'},             #D

    {'destination': 'PROBLEMS'},                #D
    {'destination': 'PROBLEMS'},                #DS
    {'destination': 'PROBLEMS'},                #DIS
    {'destination': 'PROBLEMS'},                #DI

    {'destination': 'X', 'suppd':'2022 AB'},    #DS
    {'destination': 'X', 'suppd':'2022 AB'},    #DS
    {'destination': 'X', 'suppd':'2022 AB'},    #DS

    {'destination': 'X', 'suppd':'2022 AB'},    #DI
    {'destination': 'X', 'suppd':'2022 AB'},    #DIS
    {'destination': 'X', 'suppd':'2022 AB'},    #DIS

    {'destination': 'ATT'},                     #I
    {'destination': 'X', 'suppd':'2022 AB'},    #I
    {'destination': 'ITF'},               #I
  ]
  for input, expected_result_dict in zip(input_values, expected_values):
  
    # Call the function to be tested
    destination_job_spec_dict = redirector.decision_func_NEWSUB(input[0], input[1], input[2], input[3])

    # Check that result is as expected
    assert 'destination' in destination_job_spec_dict
    assert destination_job_spec_dict['destination'] == expected_result_dict['destination']
    if 'suppd' in expected_result_dict:
      assert destination_job_spec_dict['suppd'] == expected_result_dict['suppd']




# ----- Test Extension-decision function --------------
def test_decision_func_X_A():
  
  # signature ...
  '''
success           : bool,
stacked_obs       : bool,
along_track_error : bool,
cross_track_error : bool,
cuppd             : str
  '''
  input_values  = [
    (True, False, False, False, '2022 AB'),
    (True, False, False, False, 'ufkkuffhjkhjfkkfhj'),
    (True, False, False, False, ''),

    (False, True, False, False, ''),
    (False, True, True, False, ''),
    (False, False, True, False, ''),

    (False, False, False, True, ''),
    (False, False, False, False, ''),
  ]

  expected_values = [
    {'destination': 'CUPPD', 'cuppd':'2022 AB'},
    {'destination': 'CUPPD', 'cuppd':'ufkkuffhjkhjfkkfhj'},
    {'destination': 'ATT'},

    {'destination': 'R/D'},
    {'destination': 'R/D'},
    {'destination': 'R/D'},

    {'destination': 'ATT'},
    {'destination': 'ATT'},
  ]
    
  for input, expected_result_dict in zip(input_values, expected_values):
  
    # Call the function to be tested
    destination_job_spec_dict = redirector.decision_func_X(input[0], input[1], input[2], input[3], input[4])

    # Check that result is as expected
    assert 'destination' in destination_job_spec_dict, \
        f"destination not in destination_job_spec_dict"
    assert destination_job_spec_dict['destination'] == expected_result_dict['destination'], \
        f"input={input} :{destination_job_spec_dict['destination']} != {expected_result_dict['destination']}"
    if 'cuppd' in expected_result_dict:
      assert destination_job_spec_dict['cuppd'] == expected_result_dict['cuppd'], \
        f"input={input} : {destination_job_spec_dict['cuppd']}!={expected_result_dict['cuppd']}"




# ----- Test Attribution-decision function --------------
def test_decision_func_ATT_A():
  
  # signature ...
  '''
success           : bool,
suppd             : str
neocp             : bool
  '''
  input_values  = [
    (True, '2022 AB', False),
    (True, '', False),
    (False, '', False),
    
    (True, '2022 AB', True),
    (True, '', True),
    (False, '', True)
    ]
    
  expected_values = [
    {'destination': 'X', 'suppd':'2022 AB'},
    {'destination': 'ITF'},
    {'destination': 'ITF'},

    {'destination': 'X', 'suppd':'2022 AB'},
    {'destination': 'NEOCP'},
    {'destination': 'NEOCP'},
  ]
    
  for input, expected_result_dict in zip(input_values, expected_values):
  
    # Call the function to be tested
    destination_job_spec_dict = redirector.decision_func_ATT( input[0], input[1], input[2] )

    # Check that result is as expected
    assert 'destination' in destination_job_spec_dict
    assert destination_job_spec_dict['destination'] == expected_result_dict['destination']
    if 'suppd' in expected_result_dict:
      assert destination_job_spec_dict['suppd'] == expected_result_dict['suppd']




# ----- Test IOD-decision function --------------
def test_decision_func_IOD_A():
  
  # loop over expected inputs & corresponding expected output "destinations"
  input_success_values  = [True, False]
  expected_destinations = ['DESIG', 'ATT']
  for input, expected_dest in zip(input_success_values, expected_destinations):
  
    # Call the function to be tested
    destination_job_spec_dict = redirector.decision_func_IOD(input)

    # Check that resulkt is as expected
    assert 'destination' in destination_job_spec_dict
    assert destination_job_spec_dict['destination'] == expected_dest






# ----- Test overall process_redirector function --------------
def test_process_redirector_NEWSUB():
  ''' This is essentially a copy of the test_decision_func_NEW_A function above '''
  
  # loop over expected inputs & corresponding expected output "destinations"
  # NB: tuple of input_values ==>> tracklet_overlap_category, overlapped_uppd_list, suppd, new_data
  input_values  = [
    ('S', [], '', True),
    ('S', [], '2022 AB', True),
    
    ('D', ['2022 AB'], '', True),
    ('D', ['2022 AB'], '2022 AB', True),
    ('D', ['2022 AB'], '2022 CD', True),
    
    ('D', ['2022 AB'], '', False),
    
    ('D', ['2022 AB', '2022 XY'], '', True),
    ('DS', ['2022 AB', '2022 XY'], '', True),
    ('DIS', ['2022 AB', '2022 XY'], '', True),
    ('DI', ['2022 AB', '2022 XY'], '', True),

    ('DS', ['2022 AB'], '', True),
    ('DS', ['2022 AB'], '2022 AB', True),
    ('DS', ['2022 AB'], '2022 CD', True),

    ('DI', ['2022 AB'], '', True),
    ('DIS', ['2022 AB'], '', True),
    ('DIS', ['2022 AB'], '2022 CD', True),

    ('I', [], '', True),
    ('I', [], '2022 AB', True),
    ('I', [], '2022 AB', False),

                    ]
  expected_values = [
    {'destination': 'ATT'},                     #S
    {'destination': 'X', 'suppd':'2022 AB'},    #S
    
    {'destination': 'X', 'suppd':'2022 AB'},    #D
    {'destination': 'X', 'suppd':'2022 AB'},    #D
    {'destination': 'X', 'suppd':'2022 AB'},    #D

    {'destination': 'SUBORDINATE'},              #D

    {'destination': 'PROBLEMS'},                #D
    {'destination': 'PROBLEMS'},                #DS
    {'destination': 'PROBLEMS'},                #DIS
    {'destination': 'PROBLEMS'},                #DI

    {'destination': 'X', 'suppd':'2022 AB'},    #DS
    {'destination': 'X', 'suppd':'2022 AB'},    #DS
    {'destination': 'X', 'suppd':'2022 AB'},    #DS

    {'destination': 'X', 'suppd':'2022 AB'},    #DI
    {'destination': 'X', 'suppd':'2022 AB'},    #DIS
    {'destination': 'X', 'suppd':'2022 AB'},    #DIS

    {'destination': 'ATT'},                     #I
    {'destination': 'X', 'suppd':'2022 AB'},    #I
    {'destination': 'ITF'},                     #I
  ]
  for input, expected_result_dict in zip(input_values, expected_values):
  
    # Call the function to be tested
    destination_job_spec_dict = redirector.process_redirector('NEW',
                                                                { 'tracklet_overlap_category':input[0],
                                                                'overlapped_uppd_list':input[1],
                                                                'suppd':input[2],
                                                                'new_data':input[3]}
                                                                )

    # Check that result is as expected
    assert 'destination' in destination_job_spec_dict
    assert destination_job_spec_dict['destination'] == expected_result_dict['destination']
    if 'suppd' in expected_result_dict:
      assert destination_job_spec_dict['suppd'] == expected_result_dict['suppd']



# ----- Test Extension-decision function --------------
def test_process_redirector_X():
  
  # signature ...
  '''
success           : bool,
stacked_obs       : bool,
along_track_error : bool,
cross_track_error : bool,
cuppd             : str
  '''
  input_values  = [
    (True, False, False, False, '2022 AB'),
    (True, False, False, False, 'ufkkuffhjkhjfkkfhj'),
    (True, False, False, False, ''),

    (False, True, False, False, ''),
    (False, True, True, False, ''),
    (False, False, True, False, ''),

    (False, False, False, True, ''),
    (False, False, False, False, ''),
  ]

  expected_values = [
    {'destination': 'CUPPD', 'cuppd':'2022 AB'},
    {'destination': 'CUPPD', 'cuppd':'ufkkuffhjkhjfkkfhj'},
    {'destination': 'ATT'},

    {'destination': 'R/D'},
    {'destination': 'R/D'},
    {'destination': 'R/D'},

    {'destination': 'ATT'},
    {'destination': 'ATT'},
  ]
    
  for input, expected_result_dict in zip(input_values, expected_values):


    # Call the function to be tested
    destination_job_spec_dict = redirector.process_redirector('X',
                                                            {'success':input[0],
                                                            'stacked_obs':input[1],
                                                            'along_track_error':input[2],
                                                            'cross_track_error':input[3],
                                                            'cuppd':input[4]} )

    # Check that result is as expected
    assert 'destination' in destination_job_spec_dict, \
        f"destination not in destination_job_spec_dict"
    assert destination_job_spec_dict['destination'] == expected_result_dict['destination'], \
        f"input={input} :{destination_job_spec_dict['destination']} != {expected_result_dict['destination']}"
    if 'cuppd' in expected_result_dict:
      assert destination_job_spec_dict['cuppd'] == expected_result_dict['cuppd'], \
        f"input={input} : {destination_job_spec_dict['cuppd']}!={expected_result_dict['cuppd']}"



# ----- Test Attribution-decision function --------------
def test_process_redirector_ATT():
  
  # signature ...
  '''
success           : bool,
suppd             : str
neocp             : bool
  '''
  input_values  = [
    (True, '2022 AB', False),
    (True, '', False),
    (False, '', False),
    
    (True, '2022 AB', True),
    (True, '', True),
    (False, '', True)
    ]
    
  expected_values = [
    {'destination': 'X', 'suppd':'2022 AB'},
    {'destination': 'ITF'},
    {'destination': 'ITF'},

    {'destination': 'X', 'suppd':'2022 AB'},
    {'destination': 'NEOCP'},
    {'destination': 'NEOCP'},
  ]
    
  for input, expected_result_dict in zip(input_values, expected_values):
  
    # Call the function to be tested
    destination_job_spec_dict = redirector.process_redirector( 'ATT',{'success':input[0], 'suppd':input[1], 'neocp':input[2]} )

    # Check that result is as expected
    assert 'destination' in destination_job_spec_dict
    assert destination_job_spec_dict['destination'] == expected_result_dict['destination']
    if 'suppd' in expected_result_dict:
      assert destination_job_spec_dict['suppd'] == expected_result_dict['suppd']




# ----- Test IOD-decision function --------------
def test_process_redirector_IOD():
  
  # loop over expected inputs & corresponding expected output "destinations"
  input_success_values  = [True, False]
  expected_destinations = ['DESIG', 'ATT']
  for input, expected_dest in zip(input_success_values, expected_destinations):
  
    # Call the function to be tested
    destination_job_spec_dict = redirector.process_redirector('I',{'success':input})

    # Check that resulkt is as expected
    assert 'destination' in destination_job_spec_dict
    assert destination_job_spec_dict['destination'] == expected_dest

