""" 
Dummy Data for Database

data = {
    'users': [
        { 
            'u_id': 1,                                              
            'email': harrypotter@gmail.com,                         
            'name_first': Harry,                       
            'name_last': Potter,                         
            'handle_str': harrypotter,     
            'password': password_1_1324&#!$,
            'permission_id': 1,
            'notifications' : [],
            'session_list': [123e4567-e89b-12d3-a456-426614174000]
        },
        { 
            'u_id': 2,                                              
            'email': bobsmith@gmail.com,                         
            'name_first': Bob,                       
            'name_last': Smith,                         
            'handle_str': bobsmith,    
            'password': password_2_1324&#!$,
            'permission_id': 2,
            'notifications' : []
            'session_list': []
        },
    ],
    'channels': [           
        {
            'channel_id': 1,
            'name': Sample_channel_1,
            'owner_members': [
                { 
                    'u_id': 1,                                              
                    'email': harrypotter@gmail.com,                        
                    'name_first': Harry,                       
                    'name_last': Potter,                         
                    'handle_str': harrypotter,    
                    'password': password_1_1324&#!$,
                    'permission_id': 1,
                    'session_list': [123e4567-e89b-12d3-a456-426614174000]
                },
            ],
            'all_members': [
                { 
                    'u_id': 1,                                              
                    'email': harrypotter@gmail.com,                        
                    'name_first': Harry,                       
                    'name_last': Potter,                         
                    'handle_str': harrypotter,    
                    'password': password_1_1324&#!$,
                    'permission_id': 1,                        
                    'session_list': [123e4567-e89b-12d3-a456-426614174000]
                },
                { 
                    'u_id': 2,                                              
                    'email': bobsmith@gmail.com,                         
                    'name_first': Bob,                      
                    'name_last': Smith,                         
                    'handle_str': bobsmith,     
                    'password': password_2_1324&#!$,                         
                    'permission_id': 2,                        
                    'session_list': []
                },
            ],
            'messages': [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'Hello world',
                    'time_created': 1582426789,
                }
            ],
            'is_public': TRUE,
        }
    ],
    'dms': [
        {
            'auth_user_id': 1,
            'dm_id': 1,
            'u_ids': [1, 2]
            'dm_name': "bobsmith, harrypotter",
            'messages': []
        }
    ],

    'user_count': 2,
    'message_count': 1,
    'channel_count': 1,
    'dm_count': 1,
    'owner_count': 1
}
"""