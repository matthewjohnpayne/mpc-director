'''


'''

# Standard Imports --------------------------------
import pytest
import enum
import sys, os

# Local Imports -----------------------------------
#import mpc_director as redirector
sys.path.append("../mpc_director/")
import evaluate_orbit_fits as eof 


# ----- Test ...  --------------
def test_orbit_criteria():

    # check that orbit_criteria_dict exists
    assert isinstance(eof.orbit_criteria_dict , dict )

    # check that ocdCategories exists
    assert isinstance(eof.ocdCategories, enum.EnumMeta)

    # check that ocdCriteriaSets exists
    assert isinstance(eof.ocdCriteriaSets, enum.EnumMeta)

    # check that ocdCategories contains the expected categories
    # - It's fine to have more categoories than this, but we need to implement tests!
    assert eof.ocdCategories.single_tracklet
    assert eof.ocdCategories.multi_tracklet
    assert len(eof.ocdCategories) == 2
    
    # check that ocdCriteriaSets contains the expected categories
    # - It's fine to have more categoories than this, but we need to implement tests!
    assert eof.ocdCriteriaSets.mp_iod
    assert eof.ocdCriteriaSets.mp_X
    assert len(eof.ocdCriteriaSets) == 2



def test_EvaluateOrbitFit():
    
    # check that instantiation works
    for _ in eof.ocdCriteriaSets:
      E = eof.EvaluateOrbitFit(_._name_)
      assert hasattr(E, '__dict__')
      
    # check that the instantiated object has the expected variables
    # (here I just check one variable because I am lazy: should list more)
    # (1) 'mp_iod'
    E = eof.EvaluateOrbitFit('mp_iod')
    assert hasattr(E, 'minimum_number_tracklets')

    # (2) 'mp_X'
    E = eof.EvaluateOrbitFit('mp_X')
    assert hasattr(E, 'bad_obs_weight')



def test__eval_mp_X():
    
    # instantiate
    E = eof.EvaluateOrbitFit('mp_X')
    
    # call function we want to check/test: here we expect the result to be True
    number_tracklets, number_observations, number_nights, rms = 4, 12, 3, 0.5
    result = E._eval_mp_iod( number_tracklets, number_observations, number_nights, rms)
    assert isinstance(result, bool)
    assert result

    # call function we want to check/test: here we expect the result to be False
    number_tracklets, number_observations, number_nights, rms = 2, 12, 3, 0.5
    result = E._eval_mp_iod( number_tracklets, number_observations, number_nights, rms)
    assert isinstance(result, bool)
    assert not result



def test__eval_mp_iod():
    
    # instantiate
    E = eof.EvaluateOrbitFit('mp_iod')
    
    # call function we want to check/test: here we expect the result to be True
    number_tracklets, number_observations, number_nights, rms = 4, 12, 3, 0.5
    result = E._eval_mp_iod( number_tracklets, number_observations, number_nights, rms)
    assert isinstance(result, bool)
    assert result

    # call function we want to check/test: here we expect the result to be False
    number_tracklets, number_observations, number_nights, rms = 2, 12, 3, 0.5
    result = E._eval_mp_iod( number_tracklets, number_observations, number_nights, rms)
    assert isinstance(result, bool)
    assert not result
