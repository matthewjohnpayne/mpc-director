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
# Import Orbit Criteria (from json)
# - This does *not* seem like the correct way to do this ... 
# --------------------------------------------------
import json
with open("../config_jsons/orbit_fitting_criteria.json") as f:
  orbit_criteria_dict = json.load(f)
print(orbit_criteria_dict)

# --------------------------------------------------
# Evaluation Class(es) / Function(s)
# --------------------------------------------------

class EvaluateOrbitFit():

  

  def __init__(self, criteria_key ):
  
    # Get criteria from dict
    for k,v in criteria_dicts[criteria_key]:
      self.__dict__[k] = v["value"]


    # --- Allow for the possibility of overriding defaults using kwargs ---
    # - I'm dubious about doing this ... 
    #for k,v in self.__dict__.items():
    #  if k in kwargs:
    #    self.__dict__[k] = kwargs[k]



  

  # (A) Functions to evaluate IOD orbit-fits  
  # - I.e. Criteria for that would allow us to designate a new object ... 
  # ------------------------------------------------------------------------------------

  def itf_2_itf(self, 
		number_tracklets,     # Do  
		number_observations,  # we
		number_nights,        # care?
		rms):
    '''
    Linking ITF tracklets [Identification pipeline]
    - I guess this is also the criteria that should be applied to ...
      the creation of any generic MBA designation (e.g. when removing non-NEOs from the NEOCP)
    - I guess that somewhere I/we need to think about the IAUs/MPCs old habit ...
      of allowing any 2-nighter to be designated
    '''
    if number_tracklets    >= minimum_number_tracklets    and \
       number_observations >= minimum_number_observations and \
       number_nights       >= minimum_number_nights       and \
       rms                 <= maximum_scaled_rms:
      return True
    return False 

