'''
These tests all use simplified synthetic inputs
 - They only test the "destination"/"result" that is returned when given perfect, simplified inputs. 


'''

# ----- Imports --------------------------------
#import mpc_director as redirector
import sys, os 
sys.path.append("../mpc_director/")
import single_tracklet_redirector as redirector

import pytest


# ----- Test IOD-decision function --------------
def test_decision_func_I_A():
  
  # define input dict
  # - I.e. synthetic results from IOD
  proc_results_dict = {
    "success": True,
    "trkid": 'abc123',
    "some": 'words'
    }
  proc_spec_dict = {'trkid' : proc_results_dict['trkid']}
  
  # Call the function to be tested
  to_proc_type, proc_spec_dict = redirector.decision_func_I(proc_results_dict, proc_spec_dict)

  # Check that the successful tracklet is sent to be designated
  assert to_proc_type == 'DESIG'
  assert 'trkid' in proc_spec_dict


def test_decision_func_I_B():
  
  # define input dict
  # - I.e. synthetic results from IOD
  proc_results_dict = {
    "success": False,
    "trkid": 'abc123',
    "some": {"other":'dict'}
    }
  proc_spec_dict = {'trkid' : proc_results_dict['trkid']}

  # Call the function to be tested
  to_proc_type, proc_spec_dict = redirector.decision_func_I(proc_results_dict, proc_spec_dict)

  # Check that the failed tracklet is send for attribution
  assert to_proc_type == 'ATT'
  assert 'trkid' in proc_spec_dict





# ----- Test Extension-decision function --------------
def test_decision_func_X_A():
  
  # define input dict
  # - I.e. synthetic results from orbit extension
  proc_results_dict = {
    "success": True,
    "trkid": 'abc123',
    "uppd": '2022 AB2'
    }
  proc_spec_dict = {'trkid' : proc_results_dict['trkid']}

  # Call the function to be tested
  to_proc_type, proc_spec_dict = redirector.decision_func_X(proc_results_dict, proc_spec_dict)

  # Check that the successful tracklet has confirmed uppd
  assert to_proc_type == 'CUPPD'
  assert 'trkid' in proc_spec_dict
  assert 'confirmed_uppd' in proc_spec_dict


def test_decision_func_X_B():
  
  # define input dict
  # - I.e. synthetic results from orbit extension
  proc_results_dict = {
    "success": False,
    "trkid": 'abc123',
    "stacked": True
    }
  proc_spec_dict = {'trkid' : proc_results_dict['trkid']}

  # Call the function to be tested
  to_proc_type, proc_spec_dict = redirector.decision_func_X(proc_results_dict, proc_spec_dict)

  # Check that the failed tracklet is being sent for deletion/rejection
  assert to_proc_type == 'R/D'
  assert 'trkid' in proc_spec_dict


def test_decision_func_X_C():
  
  # define input dict
  # - I.e. synthetic results from orbit extension
  proc_results_dict = {
    "success": False,
    "trkid": 'abc123',
    "offset": True
    }
  proc_spec_dict = {'trkid' : proc_results_dict['trkid']}

  # Call the function to be tested
  to_proc_type, proc_spec_dict = redirector.decision_func_X(proc_results_dict, proc_spec_dict)

  # Check that the failed tracklet is being sent for deletion/rejection
  assert to_proc_type == 'R/D'
  assert 'trkid' in proc_spec_dict


def test_decision_func_X_D():
  
  # define input dict
  # - I.e. synthetic results from orbit extension
  proc_results_dict = {
    "success": False,
    "trkid": 'abc123',
    "cross_track": True
    }
  proc_spec_dict = {'trkid' : proc_results_dict['trkid']}

  # Call the function to be tested
  to_proc_type, proc_spec_dict = redirector.decision_func_X(proc_results_dict, proc_spec_dict)

  # Check that the cross-track tracklet is being sent for attribution
  assert to_proc_type == 'ATT'
  assert 'trkid' in proc_spec_dict


def test_decision_func_X_E():
  
  # define input dict
  # - I.e. synthetic results from orbit extension
  proc_results_dict = {
    "success": False,
    "trkid": 'abc123',
    "some": 'information'
    }
  proc_spec_dict = {'trkid' : proc_results_dict['trkid']}

  # Call the function to be tested
  to_proc_type, proc_spec_dict = redirector.decision_func_X(proc_results_dict, proc_spec_dict)

  # Check that the generic bad tracklet is being sent for attribution
  assert to_proc_type == 'ATT'
  assert 'trkid' in proc_spec_dict




# ----- Test Attribution-decision function --------------
def test_decision_func_ATT_A():
  
  # define input dict
  # - I.e. synthetic results from attribution
  proc_results_dict = {
    "success": True,
    "trkid": 'abc123',
    "suppd": '2022 AB2'
    }
  proc_spec_dict = {'trkid' : proc_results_dict['trkid']}

  # Call the function to be tested
  to_proc_type, proc_spec_dict = redirector.decision_func_ATT(proc_results_dict, proc_spec_dict)

  # Check that the successfully attributed tracklet is being sent for orbit-extension
  assert to_proc_type == 'X'
  assert 'trkid' in proc_spec_dict
  assert 'suppd' in proc_spec_dict


def test_decision_func_ATT_B():
  
  # define input dict
  # - I.e. synthetic results from attribution
  proc_results_dict = {
    "success": False,
    "trkid": 'abc123',
    }
  proc_spec_dict = {'trkid' : proc_results_dict['trkid']}

  # Call the function to be tested
  to_proc_type, proc_spec_dict = redirector.decision_func_ATT(proc_results_dict, proc_spec_dict)

  # Check that the failed-attribution tracklet is being sent to ITF
  assert to_proc_type == 'ITF'
  assert 'trkid' in proc_spec_dict

