

import pylons.config as config

import ckan.logic as logic
import ckan.model as model
import ckan.lib as lib
from ckan.logic.action.create import user_create as ckan_user_create
import ckan.plugins.toolkit as toolkit
import logging
log1 = logging.getLogger(__name__)
_get_action = logic.get_action

def user_create(context, data_dict):
    
    user_dict = ckan_user_create(context, data_dict)
    user = model.User.get(user_dict['id'])
    org_name = config.get('ckan.userautoadd.organization_name', '')
    role = config.get('ckan.userautoadd.organization_role', '')
    
    try:
        toolkit.get_action('organization_show')(
            context, {
                'id': org_name,
            }
        )
    except logic.NotFound:
        return user
    
    member_dict = {
	'username': user.id,
	'id': org_name,
	'role': role
    }
    context['ignore_auth'] = True
    suffix = "athena-innovation.gr";
    if data_dict['email'].endswith(suffix):
        _get_action('organization_member_create')(context, member_dict) 
    
    
    return user
