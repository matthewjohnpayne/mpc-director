''' 
processor_categories.py
 - Defining the different types of processing "operations" we expect/allow to exist 


tracklet_processor_types
------------------------
The "single" field is attempting to indicate whether the processor type handles single tracklets (if True) or clusters (if False)

The "async" field is attempting to indicate whether this type of job is performed asyncronosly (by some process that is external to the db)
 - If so, then we allow the proc_type/job_type field in the tracklet_queue / cluster_queue tables to be set to this type.
 - I.e. whether we want to create jobs of this type in the table (if False, they are just db-update jobs, requiring no async-queuing)



MJP 2022-11-09

'''

tracklet_processor_types = {
	# --------- SINGLE TRACKLET JOBS : INTERNAL ---------------------------------------
	'NEW'	: {	'title'         	: 'New Submission',
                        'description'   	: 'A new submission has been received...',
			'single'		: True, 
			'async'			: False, 
                        }, 
        'R/D'   : {     'title'         	: 'Reject / Delete',
                        'description'   	: 'Perform all necessary tasks to label a tracklet as rejected / deleted',
                        'single'        	: True,
                        'async'         	: False,
                    },
        'ITF'   : {     'title'         	: 'Send to ITF',
                        'description'   	: 'Perform all necessary tasks to label a tracklet as being in the ITF',
                        'single'                : True, 
                        'async'                 : False,
                    },
        'CUPPD' : {     'title'         	: 'Confirmed Designation',
                        'description'   	: 'Perform all necessary operations to update database for valid CUPPD (obs, orbit, ...)',
                        'single'                : True,
                        'async'                 : False,
                    },

        # --------- SINGLE TRACKLET JOBS : EXTERNAL/ASYNC ----------------------------------
     	'X' 	: { 	'title'         	: 'Orbit extension',
                	'description'   	: 'Attempt orbit-fit that combines new tracklet with previously-published obs for known object',
                        'single'                : True,
                        'async'                 : True,
                    	},
    	'ATT' : {	'title'        		: 'Attribution',
                    	'description'   	: 'Check whether any known orbits come close to these observations: this will generate a suggested_uppd',
                        'single'        	: True,
                      	'async'      		: True,
                    	},
        'NEOCP' : {     'title'                 : 'NEOCP Calculations & Posting',
                        'description'           : 'Do orbit-fitting, variant-orbit fitting, etc, and then post to the NEOCP',
                        'single'                : True,
                        'async'                 : True,
                        },


        # --------- CLUSTER TRACKLET JOBS : INTERNAL ---------------------------------------

     	'DESIG' : { 	'title'         	: 'New Designation',
                       	'description'   	: 'Perform all necessary operations to issue a new designation (identifications, obs, orbit, ...)'
                     	'single'      		: False,
                      	'async'    		: False
                    },

        # --------- CLUSTER TRACKLET JOBS : EXTERNAL/ASYNC ----------------------------------

        'I'     : {     'title'         	: 'IOD',
                        'description'   	: 'Perform IOD on tracklets',
                        'single'        	: False, # MPC tracklets are typically less than 1-night 
                        'async'   		: True
                        },
	'L'	: {     'title'                 : 'Linking',
                        'description'           : 'Check tracklets "link" ',
                        'single'                : False, # Is there *any* functional difference between this and IOD ?
                        'async'                 : True
                        },
}
