# -*- coding: utf-8 -*-
"""

    This function filters the "notes" field associated with each missed game
    or inactive list event.
    
    Input:
        -Text string 'c'
    Outputs: 
        -  "note keyword" (e.g. calf, shin),
        -  a note "category" (eg. lower leg sick, healthy inactive)

@author: evanl
"""

def notes_filter(c):
    
    """
    This function filters the "notes" field associated with each missed game
    or inactive list event. It returns: (a)  "note keyword" (e.g. calf, shin),
    and (b) a note "category" (eg. lower leg sick, healthy inactive)
    """
    
    #convert string to lower case characters
    note = c['Notes']
    lower_case_note =note.lower()
    
    #-------------Player activated or returned to lineup----------------------
    if any(x in lower_case_note for x in ['return', 'returned','activate', 'activated']):
        return 'returned to lineup', 'n/a'
               
    #----------Healthy Inactive/Missed Game--------------------------
    #If no reason is given for missed game or move to inactive list, assume it
    #was a non-injury move.
    elif lower_case_note == 'placed on il' or lower_case_note == 'placed on il (p)':
        return 'roster move', 'healthy inactive'
    
    elif 'suspension' in lower_case_note:
        return 'suspension', 'healthy inactive'
    
    elif any(x in lower_case_note for x in ['family','personal','birth', 'death']):
        return 'personal reasons', 'healthy inactive'
    
        
    #-------Rest Inactive--------------------------------
    elif 'rest' in lower_case_note:
        return 'rest', 'rest'
           
     #-------Sick Inactive  -------------------------------
    elif any(x in lower_case_note for x in ['virus','headache','flu', 'sick', 'illness','infection','pneumonia', 'gastro','appende','nausea', 'pox', 'dizziness', 'poisoning','bronchitis']):
        return 'sick', 'sick'
    
    #--------Foot Injuries------------------------------------
    elif 'foot' in lower_case_note:
        return 'foot', 'foot'
    elif 'toe' in lower_case_note:
        return 'toe', 'foot'
    elif 'heel' in lower_case_note:
        return 'heel', 'foot'
    
    #-------Lower leg injuries---------------------------
    elif 'ankle' in lower_case_note:
        return 'ankle', 'lower leg'             
    elif 'achilles'in lower_case_note:
        return 'achilles', 'lower leg'  
    elif 'calf' in lower_case_note:
        return 'calf', 'lower leg'
    elif 'shin' in lower_case_note:
        return 'shin', 'lower leg'
    elif 'tibia' in lower_case_note:
        return 'tibia', 'lower leg'
    elif 'fibula' in lower_case_note:
        return 'fibula','lower leg'
   
    #---------Knee injuries------------------------------------
    elif 'acl' in lower_case_note:
        return 'ACL', 'knee'
    elif 'mcl' in lower_case_note:
        return 'MCL', 'knee'
    elif any(x in lower_case_note for x in ['knee','patella','meniscus']):
        return 'knee', 'knee'
    
    #---------Upper leg injuries---------------------------------
    elif any(x in lower_case_note for x in ['quad','quadriceps','thigh']):
        return 'quad', 'upper leg'
    elif 'hamstring' in lower_case_note:
        return 'hamstring', 'upper leg'
    elif 'groin' in lower_case_note:
        return 'groin', 'upper leg'
    elif any(x in lower_case_note for x in ['hip','adductor']):
        return 'hip', 'upper leg'
    elif 'femur' in lower_case_note:
        return 'femur', 'upper leg'
    
    #-----------leg catch all------------------------------------
    elif 'leg' in lower_case_note:
        return 'leg', 'leg'
    
    
    #-----------Torso injuries--------------------------
    elif any(x in lower_case_note for x in ['chest', 'pectoral']):
        return 'chest', 'torso'
    elif any(x in lower_case_note for x in ['shoulder','rotator cuff']):
        return 'shoulder', 'torso'
    elif 'back' in lower_case_note:
        return 'back', 'torso'
    elif 'collarbone' in lower_case_note:
        return 'collarbone', 'torso'
    elif 'rib' in lower_case_note:
        return 'ribs', 'torso'
    elif any(x in lower_case_note for x in ['abdom','abductor','oblique']):
        return 'abdominal', 'torso'
    
    #------------Head/neck injuries----------------------------
    elif 'neck' in lower_case_note:
        return 'neck', 'head'
    elif any(x in lower_case_note for x in ['head', 'concussion']):
        return 'head', 'head'
    elif 'eye' in lower_case_note:
        return 'eye', 'head'
    elif 'nose' in lower_case_note:
        return 'nose', 'head'
    
    #------------ Hand injuries---------------------------------
    elif 'hand' in lower_case_note:
        return 'hand', 'hand'
    elif any(x in lower_case_note for x in ['finger', 'thumb']):
        return 'finger', 'hand'

    
    #------------ Arm injuries---------------------------------
    elif 'arm' in lower_case_note:
        return 'arm', 'arm'
    elif 'elbow' in lower_case_note:
        return 'elbow', 'arm'
    elif 'bicep' in lower_case_note:
        return 'bicep', 'arm'
    elif 'tricep' in lower_case_note:
        return 'tricep', 'arm'
    elif 'wrist' in lower_case_note:
        return 'wrist', 'arm'     
    else:
        return 'other', 'other'