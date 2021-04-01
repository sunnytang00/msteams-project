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
            'global_permission': 1,                        
        },
        { 
            'u_id': 2,                                              
            'email': bobsmith@gmail.com,                         
            'name_first': Bob,                       
            'name_last': Smith,                         
            'handle_str': bobsmith,    
            'password': password_2_1324&#!$,
            'global_permission': 2,
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
                    'global_permission': 1,
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
                    'global_permission': 1,                        
                },
                { 
                    'u_id': 2,                                              
                    'email': bobsmith@gmail.com,                         
                    'name_first': Bob,                      
                    'name_last': Smith,                         
                    'handle_str': bobsmith,     
                    'password': password_2_1324&#!$,                         
                    'global_permission': 2,
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