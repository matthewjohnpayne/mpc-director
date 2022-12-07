'''
Working towards a centralized, standardized set of criteria to use when orbit-fitting in various contexts/pipelines

The functions in this module are intended to provide a standardized way to evaluate whether a particular orbit fit should be classed as successful. 
 - To do this they use standardized criteria defined in various json-files contained in ../config_jsons
 - The criteria are *context-dependent* : ddifferent criteria are used depending on whether this is mp-vs-comet, iod-vs-extension, etc

We expect that there will always be exceptions, especially when manually dealing with some emergency:

Should link to criteria document(s):
 - https://docs.google.com/document/d/12QQl34Sg6BEqZauiA8P115rYSg3TIPdyn-PimMUv-FI/edit#


*******************************************
There are different ways to view the kinds of orbit-fitting we do ...
(i) Linking -vs- Pipelines -vs- Cleaning
(ii) IOD -vs- Extension -vs- Cleaning

(A) Linking
 - itf-2-itf    == IOD
 - itf-2-desig  == Extension

(B) Automated submission pipelines
 - Extension : but lots of possible criteria depending on mp/comet/sat, n_opp, ...

(C) Removing Incorrect Tracklets
 - Cleaning

(D) NEOCP/PCCP
 - MPECs == IOD
 - Non-MPECS == IOD 


*******************************************
Different subdivisions...

IOD
 - NEO / Comet / MBA / TNO / Nat-Sat 
 - ITF -vs- New (NEOCP/New-Sub)

Extension 
 - MP
   --- Short (1-opp) / Short-to-Long (newid) / Long (multi-opp)

 - Comet
   --- ??? / ??? 

 - TNO
   --- ???

 - Nat-Sat
   --- ??? 

Cleaning 
 - Arc-Length Reduced / Same 




*******************************************
MJP: 2022-11-03
'''

# --------------------------------------------------
# Imports ...
from enum import Enum
import json
import itertools


# --------------------------------------------------
# Import Orbit Criteria (from json)
# - This does *not* seem like the correct way to do this ... 
# --------------------------------------------------
with open("../config_jsons/orbit_fitting_criteria.json") as f:
  orbit_criteria_dict = json.load(f)

# These top-level categories look like ...
# [<ocdCategories.multi_tracklet: 1>, <ocdCategories.single_tracklet: 2>]
ocdCategories = Enum( "ocdCategories", list(orbit_criteria_dict.keys()) )

# These lower level criteria sets look like ...
# [<ocdCriteriaSets.mp_iod: 1>, <ocdCriteriaSets.cmt_iod: 2>, <ocdCriteriaSets.mp_X: 3>]
ocdCriteriaSets = Enum( "ocdCriteriaSets", list(itertools.chain(*[list(v['value'].keys()) for v in orbit_criteria_dict.values()])) )


# --------------------------------------------------
# Evaluation Class(es) / Function(s)
# --------------------------------------------------

class EvaluateOrbitFit():

  

  def __init__(self, criteria_key ):

    # ensure that the "criteria_key" is in ocdCriteriaSets
    assert criteria_key in ocdCriteriaSets.__dict__ , f'{criteria_key} is an unknown orbit-fitting criteria-type'
  
    # Get criteria from dict/json
    for k,v in orbit_criteria_dict.items():                     # top-level ocdCategories, E.g. k = 'single_tracklet'
      if criteria_key in v['value'].keys():                     # lower-level ocdCriteriaSets, E.g. 'mp_X'
        for kk,vv in v['value'][criteria_key]['value'].items(): # lowest level criteria, E.g. "minimum_number_tracklets"
          self.__dict__[kk] = vv['value']



  # Single-Tracklet Evaluation Functions ...
  # ------------------------------------------------------------------------------------
  def _eval_mp_X(   self,
                    bad_obs_weight,
                    fraction_bad,
                    bad_obs_threshhold,
                    discard_threshhold):
    '''
    Evaluate the results from minor-planet orbit extension
    - These should be used in most pipeline orbit fits
    '''
    if number_tracklets    >= self.minimum_number_tracklets    and \
       number_observations >= self.minimum_number_observations and \
       number_nights       >= self.minimum_number_nights       and \
       rms                 <= self.maximum_scaled_rms:
      return True
    return False





  # Multi-Tracklet Evaluation Functions ...
  # ------------------------------------------------------------------------------------
  def _eval_mp_iod( self,
                    number_tracklets,     # Do
                    number_observations,  # we
                    number_nights,        # care?
                    rms):
    '''
    Evaluate the results from minor-planet IOD
    - By definition these results must apply across the entire object (i.e. across multiple tracklets)
    - I guess this is also the criteria that should be applied to the linking of itf-2-itf
      -- There are criteria in Margaret's pipeline ...
    - I guess that somewhere I/we need to think about the IAUs/MPCs old habit ...
      of allowing any 2-nighter to be designated
    '''
    if number_tracklets    >= self.minimum_number_tracklets    and \
       number_observations >= self.minimum_number_observations and \
       number_nights       >= self.minimum_number_nights       and \
       rms                 <= self.maximum_scaled_rms:
      return True
    return False 

