# -*- coding: utf-8 -*-

#*********************************************
#         CATÁLOGO DE USUARIOS
#*********************************************
#1
@auth.requires_membership('Administrator')
def users():
    users = db(db.auth_user).select(db.auth_user.id,
                                    db.auth_user.first_name,
                                    db.auth_user.last_name,
                                    db.auth_user.email)
    def get_membership(user_id):
		return db(db.auth_membership.user_id == user_id).select(db.auth_membership.group_id)
    return dict(users = users,
                get_membership = get_membership)

@auth.requires_membership('Administrator')
def edit_user():
    user_id = request.vars.user_id

    form = SQLFORM(db.auth_user,
                   record = user_id,
                   _class = 'form-horizontal',
                   showid =False)

    if form.process().accepted:
    	session.flash = T('Saved')
        redirect(URL('users'))
    elif form.errors:
        response.flash = T('Check your data')
    return dict(form = form,
    			      user_id = user_id)

@auth.requires_membership('Administrator')
def delete_user():
	#db(db.auth_user.id == request.vars.user_id).delete()
	session.flash = T('Deleted')
	redirect(URL('users'))

@auth.requires_membership('Administrator')
def edit_roles():
    user_id     = request.vars.user_id
    user = db(db.auth_user.id == user_id).select(db.auth_user.first_name,
                                                 db.auth_user.last_name).first()
    new_groups  = request.vars.new_groups
    qry_already = (db.auth_membership.user_id == user_id)& (db.auth_group.id == db.auth_membership.group_id)
    groups      = db(db.auth_group).select()    
    
    already_groups  = to_list(db(qry_already).select(db.auth_group.id))

    if request.vars.update_roles:
        if not new_groups:
            new_groups = []
        elif type(new_groups) is str:
            new_groups = [new_groups]
        #Se añaden los nuevos grupos
        for new_group in new_groups:
            auth.add_membership(new_group, user_id)
        #Se generan los grupos que se deben eliminar
        #es la diferencia entre todos los grupos y los que se asignaron
        delete_groups = list(set(to_list(groups)) - set(new_groups))
        for delete_group in delete_groups:
            auth.del_membership(delete_group, user_id)
        session.flash = T('Saved')
        redirect(URL('users'))


    return dict(already_groups  = already_groups,
				groups 		    = groups,
				user_id 	    = user_id,
                user            = user)

def to_list(results):
    return [str(result.id) for result in results] if results else []


@cache.action()
def download():
    return response.download(request, db)
