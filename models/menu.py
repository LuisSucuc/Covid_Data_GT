# -*- coding: utf-8 -*-

response.menu = [
    (T('Home'),     'flaticon-map',         URL('default', 'index'), []),
    (T('My Sites'), 'flaticon-line-graph',  URL('admin', 'default', 'site')),
    (T('This App'), 'flaticon-like',        None, 
        [
            (T('Design'),       False,      URL('admin', 'default', 'index'), []),
            (T('Controller'),   False,      URL('admin', 'default', 'index'), []),
            (T('Layout'),       False,      URL('admin', 'default', 'index'), []),
        ]
    ),
    (T('Menu'), 	'flaticon-time',     None, 
        [
            (T('Test'),       False,        URL( 'test', 'test'), []),
            (T('Controller'),   False,      URL( 'test', 'test2'), []),
        ]
    ),
]

if auth.has_membership(group_id='Administrator'):
    response.menu += [ (T('Manage'),     'flaticon-interface-1',        None, 
                        [
                            (T('Users'),       False,      URL('manage', 'users'), []),
                        ]),
                    ]