''' 
redirector.py
 - pseudo-code to direct tracklet / cluster jobs
 - I.e. based upon the results from a previous job, the tracklet / cluster is assigned to a subsequent processing job ...

MJP 2022-11-09

 one could imagine using luigi/similar, but fuck-it ... 

'''
import processor_categories as proc_cats
import tracklet_overlap_categories as track_cats

# --------------------------------------------
# Overall control function(s)
# --------------------------------------------
def single_tracklet_redirector( from_proc_type, proc_results_dict ) :
  '''
    Given the results from a preceeding processing step for 
    *** single tracklets *** , decide what the next processing 
    step should be
    
    inputs:
    -------
    from_proc_type      : str
     -
     
    proc_results_dict   : dict
     -
    
    returns:
    --------
    to_proc_type        : str
     -
      
    proc_spec_dict      : dict
     -
  '''

  # check the inputs
  assert from_proc_type in proc_cats.tracklet_processor_types
  assert "success" in proc_results_dict # <<-- if "success" NOT in proc_results_dict, then input is malformed: raise error?
  assert "trkid" in proc_results_dict # <<-- if "trkid" NOT in proc_results_dict, then input is malformed: raise error?

  # define some default output values (to-be populated by subsequent functions)
  to_proc_type, proc_spec_dict = None, {'trkid' : proc_results_dict['trkid']}

  # redirect NEW tracklet
  if from_proc_type == 'NEW':
    to_proc_type, proc_spec_dict = decision_func_NEWSUB( proc_results_dict , proc_spec_dict)

  # redirect results from orbit-extension
  elif from_proc_type == 'X':
    to_proc_type, proc_spec_dict = decision_func_X(proc_results_dict, proc_spec_dict)

  # redirect results from attribution
  elif from_proc_type == 'ATT':
    to_proc_type, proc_spec_dict = decision_func_ATT(proc_results_dict, proc_spec_dict)
    
  # check that the decision is defined!!
  assert to_proc_type in proc_cats.proc_types and proc_cats.proc_types[to_proc_type]['allow_to'] 



def cluster_redirector( from_proc_type, proc_results_dict ) :
  '''
    Given the results from a preceeding ***cluster*** processing step,
    decide what the next processing step should be
    
    inputs:
    -------
    from_proc_type      : str
     -
     
    proc_results_dict   : dict
     -
    
    returns:
    --------
    to_proc_type        : str
     -
      
    proc_spec_dict      : dict
     -
  '''

  # check the inputs
  assert from_proc_type in proc_cats.tracklet_processor_types
  assert "success" in proc_results_dict # <<-- if "success" NOT in proc_results_dict, then input is malformed: raise error?
  assert "trkid" in proc_results_dict # <<-- if "trkid" NOT in proc_results_dict, then input is malformed: raise error?

  # define some default output values (to-be populated by subsequent functions)
  to_proc_type, proc_spec_dict = None, {'trkid' : proc_results_dict['trkid']}

  # redirect resultts from IOD 
  if from_proc_type == 'I':
    to_proc_type, proc_spec_dict = decision_func_I( proc_results_dict , proc_spec_dict)

  else:
    pass 


  # check that the decision is defined!!
  assert to_proc_type in proc_cats.proc_types and proc_cats.proc_types[to_proc_type]['allow_to']














# --------------------------------------------
# Single-Tracklet-Processor Decision functions
# --------------------------------------------

def decision_func_NEWSUB(proc_results_dict, proc_spec_dict):
  ''' decide what to do with *new* submissions
  
      primarily relates to what we should do for tracklet-overlap "types"
  '''
  
  # check input tracklet_overlap_category
  assert in_and_true("tracklet_overlap_category", proc_results_dict)
  assert proc_results_dict["tracklet_overlap_category"] in track_cats.allowed_tracklet_overlap_categories
  
  # if the submitted tracklet has a designation we can understand ...
  if in_and_true("suppd", proc_results_dict):
  
    # if all of the obs are single/new, send for attribution
    if proc_results_dict["tracklet_overlap_category"] == 'S':
        to_proc_type = 'X'

  
  # if *not* designation supplied ...
  else:
    # if all of the obs are single/new, send for attribution
    if proc_results_dict["tracklet_overlap_category"] == 'S':
        to_proc_type = 'ATT'
        
    # if all observations overlap with submitted observations of a single designation, send for refitting
    elif proc_results_dict["tracklet_overlap_category"] == 'D' :
        to_proc_type = 'X'


  return to_proc_type, proc_spec_dict








def decision_func_X(proc_results_dict ,  proc_spec_dict):
  ''' decide what to do with results from ORBIT EXTENSION '''

  # if the orbit-fit extension was successful, then perform
  # all operations necessary to associate tracklet with designated object
  if proc_results_dict["success"]:
    to_proc_type = 'CUPPD'
    proc_spec_dict['confirmed_uppd'] = proc_results_dict['uppd']
    
  # if the IOD orbit-fit did not work
  # (in the sense that it executed but the tracklet does not belong),
  # then ...
  else:
    # Delete / Reject when ..
    # (i) the tracklet obs are stacked and/or
    # (ii) the tracklet obs are "offset" from the expected locn
    if  in_and_true("stacked",     proc_results_dict) or \
        in_and_true("offset",      proc_results_dict):
      to_proc_type = 'R/D'
      
    # Send for Attribution (and hence perhaps ITF) when we have obvious cross-track residuals
    elif in_and_true("cross_track", proc_results_dict):
      to_proc_type = 'ATT'
      
    # Undefined outcome. E.g. generically shitty residuals
    # Send for Attribution
    # - can argue later about whether to directly reject this too ...
    else:
      to_proc_type = 'ATT'
     
  return to_proc_type, proc_spec_dict



def decision_func_ATT(proc_results_dict ,  proc_spec_dict):
  ''' decide what to do with results from ATTRIBUTION '''
  
  # if the attribution was successful, in the sense that an "suppd" was returned,
  # then send for orbit extension
  # NB it is assumed that the Attribution func is in charge of not returning results that have been returned recently...
  if proc_results_dict["success"] and \
     in_and_true("suppd", proc_results_dict) :
    to_proc_type = "X"
    proc_spec_dict['suppd'] = proc_results_dict['suppd']
      
  # Could consider adding in extra logic to look at "second-choice" suppd
  elif False:
    pass
    
  # If nothing above worked, then send to ITF (i.e. could not attribute)
  else:
    to_proc_type = "ITF"
      
  return to_proc_type, proc_spec_dict
    
    
# --------------------------------------------
# Cluster-Processor Decision functions
# --------------------------------------------



def decision_func_I(proc_results_dict, proc_spec_dict):
  ''' decide what to do with results from IOD ''
  
  # if the IOD orbit-fit was successful, then ...
  if proc_results_dict["success"]:
    to_proc_type   = 'DESIG'
    
  # if the IOD orbit-fit did not work, then try attribution
  # *** In the context of the "tracklet_queue" table, we have only a single trackid ***
  # *** we will obviously need some other way to deal with the ITF-to-ITF linkages and their potential failure ***
  else:
    to_proc_type = 'ATT'

  return to_proc_type, proc_spec_dict



# --------------------------------------------
# Assorted data / utility funcs
# --------------------------------------------

def in_and_true(k, d):
  ''' is key, k, in dict, d, and does the value d[k] retern as True/positive ? '''
  return True if k in d and d[k] else False
  
def suppd_tried_recently( suppd , time_horizon_days = 30):
  ''' stored '''

