''' 
redirector.py
 - code to direct tracklet / cluster jobs
 - I.e. based upon the results from a previous job, the tracklet / cluster is assigned to a subsequent processing job ...

MJP Did a lot of process sketching in ..
(1) Initial Desig / Overlap Flow:   https://app.diagrams.net/#G1B5l1AMNGYVKv8mMLZB286md4zeD6f6o2
(2) Overall Orbit/Attribution Flow: v5: https://app.diagrams.net/#G1bDLya4pWqjadyVlF4l1UT8riBw8nNRCm
                                    v6: https://drive.google.com/file/d/1HOVxIsQtfyFIIdKVKIY-eDt7YIU4o2TM/view?usp=share_link
MJP 2022-12-01


'''

# --------------------------------------------------
# Imports ...
# --------------------------------------------------
import json

# --------------------------------------------------
# Import Orbit Criteria (from json)
# - This does *not* seem like the correct way to do this ...
# --------------------------------------------------
with open("../config_jsons/processor_types.json") as f:
    allowed_processor_types = json.load(f)["values"]
with open("../config_jsons/tracklet_overlap_categories.json") as f:
    allowed_tracklet_overlap_categories = json.load(f)["values"]

# --------------------------------------------
# Overall control function(s)
# --------------------------------------------
def process_redirector( from_proc_type, proc_results_dict ) :
  '''
    Given the results from a preceeding processing step,
    decide what the next processing step should be.
    
    Intended to work for both *single*-tracklet processing
    jobs (e.g. orbit-extension), and *multiple*-tracklet processing
    jobs (e.g. IOD/linking)
    
    inputs:
    -------
    from_proc_type      : str
     - the type of processing job previously performed
     
    proc_results_dict   : dict
     - the results from the previous processing job
     - different jobs will return different variables within the dictionary
    
    returns:
    --------
    destination_job_spec_dict : dict
     - must contain at least a key = 'destination'
  '''
  assert from_proc_type in allowed_processor_types
 
  # -------------------------------------------------
  # ----- SINGLE-TRACKLET REDIRECTION  FUNCTIONS ----
  # -------------------------------------------------

  # redirect NEW tracklet
  if from_proc_type == 'NEW':
    destination_job_spec_dict = decision_func_NEWSUB(   proc_results_dict["tracklet_overlap_category"] ,
                                                        proc_results_dict["overlapped_uppd_list"],
                                                        proc_results_dict["suppd"],
                                                        proc_results_dict["new_data"])

  # redirect results from orbit-extension
  elif from_proc_type == 'X':
    destination_job_spec_dict = decision_func_X(proc_results_dict["success"],
                                                proc_results_dict["stacked_obs"],
                                                proc_results_dict["along_track_error"],
                                                proc_results_dict["cross_track_error"],
                                                proc_results_dict["cuppd"])

  # redirect results from attribution
  elif from_proc_type == 'ATT':
    destination_job_spec_dict = decision_func_ATT(  proc_results_dict["success"],
                                                    proc_results_dict["suppd"],
                                                    proc_results_dict["neocp"])
  
  # redirect results from NEOCP
  elif from_proc_type == 'NEOCP':
    destination_job_spec_dict = decision_func_NEOCP(  proc_results_dict["success"] )


  # -------------------------------------------------
  # ----- MULTI-TRACKLET REDIRECTION  FUNCTIONS -----
  # -------------------------------------------------

  # redirect results from IOD
  elif from_proc_type == 'I':
    destination_job_spec_dict = decision_func_IOD( proc_results_dict["success"] )





  # -------------------------------------------------
  # - Anything else is currently undefined ----------
  # -------------------------------------------------
  else:
    destination_job_spec_dict = {}
    
  # -------------------------------------------------
  # Check that the destination is defined/allowed !!
  # -------------------------------------------------
  assert 'destination' in destination_job_spec_dict
  assert destination_job_spec_dict['destination'] in allowed_processor_types, \
    f"{destination_job_spec_dict['destination']} not in {allowed_processor_types}"
  
  return destination_job_spec_dict
  







# --------------------------------------------
# Single-Tracklet-Processor Decision functions
# --------------------------------------------

def decision_func_NEWSUB(   tracklet_overlap_category : str ,
                            overlapped_uppd_list : list,
                            suppd : str,
                            new_data : bool ) -> dict:
  ''' Decide what to do with *new* submissions
      primarily relates to what we should do for tracklet-overlap "types"

      For flowchart pf logic, see: "https://app.diagrams.net/#G1B5l1AMNGYVKv8mMLZB286md4zeD6f6o2"

      NB:
       - Trying to be explicit about the input variables

    inputs:
    -------
    tracklet_overlap_category : str
     - Defining tracklet overlap categories. These would be evaluated / defined by looking at the *obs_group* status for each constituent observation of a new tracklet. Allowed values are in config_jsons/tracklet_overlap_categories.json
                            
    overlapped_uppd_list : list
     - If observations overlap with previously designated objects, we list the overlapped uppd. If *no* overlap, then list empty
                            
    suppd : str
     - Suggested unpacked primary provisional designation
     - If the submitters provided a suggested designation, this is it
                            
    new_data : bool
     - Did the submitted tracklet contain any new data, in the sense of changing the "primary obs" for the obs_group?

    returns:
    -------
    destination_job_spec_dict : dict
     - must contain at least a key = 'destination' describing the next task to be performed
  '''

  # check input tracklet_overlap_category
  assert tracklet_overlap_category in [ k for k in allowed_tracklet_overlap_categories]
  if 'D' not in tracklet_overlap_category: assert not overlapped_uppd_list
  
  # if there are multiple overlapped designations, send to problems
  # (the destination could change in the future to R/D, but clearly these are complex case)
  if len(overlapped_uppd_list) > 1:
    destination_job_spec_dict = {
        'destination' : 'PROBLEMS',
        'description' : 'Overlaps multiple designated objects:{overlapped_uppd_list}'
  }
  
  # if we have no new data for designated object, terminate
  # *** WE PROBABLY NEED TO DO *SOMETHING* : E.g. set status = ??? ***
  # ***   WHATEVER NEEDS GOING WILL BE SPECIFIED IN "SUBORDINATE"  ***
  elif tracklet_overlap_category == 'D' and new_data == False:
    destination_job_spec_dict = {
        'destination' : 'SUBORDINATE',
        'description' : 'No new data'
  }

  # if we have no new data for itf object, terminate
  elif tracklet_overlap_category == 'I' and new_data == False:
    destination_job_spec_dict = {
        'destination' : 'ITF',
  }

  # if some form of designation is available, send for orbit-fitting
  # NB: Could imagine making a different decision here, and sending suppd-only for Attribution first
  elif tracklet_overlap_category in ['D','DS','DIS','DI']  or  suppd :
    destination_job_spec_dict = {
        'destination'   : 'X',
        'suppd'         : overlapped_uppd_list[0] if overlapped_uppd_list else suppd
  }

        
  # anything else, send for attribution
  # NB: This should be S/SI/I (where the I must have new data)
  else:
    destination_job_spec_dict = {
        'destination' : 'ATT',
  }

  # could change the return signature to explicitly return a string (destination) first ...
  return destination_job_spec_dict








def decision_func_X( success           : bool,
                     stacked_obs       : bool,
                     along_track_error : bool,
                     cross_track_error : bool,
                     cuppd             : str) -> dict:
  ''' decide what to do with results from ORBIT EXTENSION
  
    Note that there are some old ideas in https://app.diagrams.net/#G1bDLya4pWqjadyVlF4l1UT8riBw8nNRCm
     - Either that flow diagram or this function should be updated to maintain consistency
  
    inputs:
    -------
    success           : bool
     - whether the orbit-extension orbit-fit was successful
     
    stacked_obs       : bool
     - whether the tracklet contains stacked observations
     
    along_track_error : bool
     - whether the rejected tracklet had significant along-track errors
     
    cross_track_error : bool
     - whether the rejected tracklet had significant across-track errors

    cuppd             : str
     - confirmed unpacked primary provisional designation for successful orbit-fit

    returns:
    -------
    destination_job_spec_dict : dict
     - must contain at least a key = 'destination' describing the next task to be performed
  '''
  # if the orbit-fit extension was successful, then perform
  # all operations necessary to associate tracklet with designated object
  if success and cuppd:
    destination_job_spec_dict = {
        'destination'   : 'CUPPD',
        'cuppd'         : cuppd
    }
  
  # if the IOD orbit-fit did not work
  # (in the sense that it executed but the tracklet does not belong),
  # then ...
  # ...
  # Delete / Reject when ..
  # (i) the tracklet obs are stacked and/or
  # (ii) the tracklet obs are "offset" from the expected locn
  elif stacked_obs or along_track_error :
    destination_job_spec_dict = {
        'destination'   : 'R/D',
    }
  
  # Send for Attribution (and hence perhaps ITF) when we have obvious cross-track residuals
  elif cross_track_error:
    destination_job_spec_dict = {
        'destination'   : 'ATT',
    }

  # Other failure: E.g. perhaps caused by generically shitty residuals, then ...
  # send for Attribution
  # NB(1) *** Might have had NEW ->> ATT (suggest #1) -->> X -->> ... And now we want to try for ATT (suggest #2) ...
  # NB(2) *** can argue later about whether to just directly reject this ***
  else:
    destination_job_spec_dict = {
        'destination'   : 'ATT',
    }

  return destination_job_spec_dict





def decision_func_ATT(  success : bool,
                        suppd   : str,
                        neocp   : bool
                        ) -> dict:
  ''' decide what to do with results from ATTRIBUTION
  
    inputs:
    -------
    success           : bool
     - whether the ATTRIBUTION was successful and found a possible designation
     
    suppd             : str
     - suggested unpacked primary provisional designation from successful ATTRIBUTION

    neocp : bool
     - is this an neocp-related submission

    returns:
    -------
    destination_job_spec_dict : dict
     - must contain at least a key = 'destination' describing the next task to be performed
  '''

  # if the attribution was successful, in the sense that an "suppd" was returned,
  # then send for orbit extension
  # NB I will assume that the Attribution func is in charge of **NOT** returning results
  #    that have already been returned recently
  #    (it could perhaps return 2nd choice if 1st choice was tried recently)
  if success and suppd:
    destination_job_spec_dict = {
        'destination'   : 'X',
        'suppd'         : suppd
    }
    
  # if this was flagged as being a possible NEOCP tracklet, then if attribution
  # failed, we send it on to the NEOCP
  elif neocp:
    destination_job_spec_dict = {
        'destination'   : 'NEOCP',
    }

  # If none of the above, then send to ITF (i.e. could not attribute)
  else:
    destination_job_spec_dict = {
        'destination'   : 'ITF',
    }
    
  return destination_job_spec_dict
    
    
    
def decision_func_NEOCP(    success : bool) -> dict:
  ''' decide what to do with results from NEOCP
  
    inputs:
    -------
    success           : bool
     - whether the NEOCP var-orb generation was successful
    
    returns:
    -------
    destination_job_spec_dict : dict
     - must contain at least a key = 'destination' describing the next task to be performed
  '''

  # if NEOCP fitting/var-orb generation was successful, we can probably terminate
  # *** might need to update some tables / fields ***
  if success:
    destination_job_spec_dict = {
        'destination'   : 'TERMINATE',
    }
    
  # if unsuccessful, send to ITF
  # NB: we assume that prior to NEOCP it has already been through (and failed) attribution, ...
  # ...so we do NOT need to send it their again
  else:
    destination_job_spec_dict = {
        'destination'   : 'ITF',
    }
    
  return destination_job_spec_dict
    
    

    
# --------------------------------------------
# Cluster-Processor Decision function(s)
# --------------------------------------------

def decision_func_IOD( success : bool) -> dict:
  ''' decide what to do with results from IOD
  
      NB(1): Especially for failures, it might be useful to define
             the "context" in which this IOD was performed ...
             "linking" => reject linkage
             "NEOCP" => ???
             "direct submission (e.g. LSST)" => reject tracklet / problems
          
      NB(2): There may also need to be a more nuanced consideration
             of whether the tracklet is submitted as a single thing,
             but then got split by the MPC ...


    inputs:
    -------
    success           : bool
     - whether the NEOCP var-orb generation was successful
    
    returns:
    -------
    destination_job_spec_dict : dict
     - must contain at least a key = 'destination' describing the next task to be performed

  '''
  
  # if the IOD orbit-fit was successful, then designate
  if success:
    destination_job_spec_dict = {
        'destination'   : 'DESIG',
    }

  # if the IOD orbit-fit did not work, then try attribution
  else:
    destination_job_spec_dict = {
        'destination'   : 'ATT',
    }

  return destination_job_spec_dict



# --------------------------------------------
# Whole-Orbit Decision function(s)
# --------------------------------------------
'''
I.e. what to do with results from,
E.g.
 - whole-orbit refitting (checking);
 - whole-orbit refitting (change ephem/pert );
 - epoch propagation;
 - ...
'''
