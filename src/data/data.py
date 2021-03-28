""" 
Dummy Data for Database

data = {
    'users': [
        { 
            'u_id': 1,                                              
            'email': sample_1@something.com,                         
            'name_first': first_sample_name_1,                       
            'name_last': last_sample_name_1,                         
            'handle_str': first_sample_name_1last_sample_name_1,     
            'password': password_1_1324&#!$,
            'is_globalpermission': true,                        
        },
        { 
            'u_id': 2,                                              
            'email': sample_2@something.com,                         
            'name_first': first_sample_name_2,                       
            'name_last': last_sample_name_2,                         
            'handle_str': first_sample_name_2last_sample_name_2,    
            'password': password_2_1324&#!$,
            'is_globalpermission': false,
        },
    ],
    'channels': [           
        {
            'channel_id': 1,
            'name': Sample_channel_1,
            'owner_members': [
                { 
                    'u_id': 1,                                              
                    'email': sample_1@something.com,                        
                    'name_first': first_sample_name_1,                       
                    'name_last': last_sample_name_1,                         
                    'handle_str': first_sample_name_1last_sample_name_1,    
                    'password': password_1_1324&#!$,
                    'is_globalpermission': true,
                },
            ],
            'all_members': [
                { 
                    'u_id': 1,                                              
                    'email': sample_1@something.com,                        
                    'name_first': first_sample_name_1,                       
                    'name_last': last_sample_name_1,                         
                    'handle_str': first_sample_name_1last_sample_name_1,    
                    'password': password_1_1324&#!$,
                    'is_globalpermission': true,                        
                },
                { 
                    'u_id': 2,                                              
                    'email': sample_2@something.com,                         
                    'name_first': first_sample_name_2,                      
                    'name_last': last_sample_name_2,                         
                    'handle_str': first_sample_name_2last_sample_name_2,     
                    'password': password_2_1324&#!$,                         
                    'is_globalpermission': false,
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
    'user_count'        : 2,
    'message_count'     : 1,
    'channel_count'     : 1,
}

"""
