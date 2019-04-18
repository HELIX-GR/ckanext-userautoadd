

import pylons.config as config

import ckan.logic as logic
import ckan.model as model
import ckan.lib as lib
from ckan.logic.action.create import user_create as ckan_user_create
from ckan.logic.schema import validator_args, user_new_form_schema

import ckan.plugins.toolkit as toolkit
import logging
log1 = logging.getLogger(__name__)
_get_action = logic.get_action

import ckanext.userautoadd.model as ue_model

def user_create(context, data_dict):
    #context['schema'] = modified_user_schema()
    
    #log1.debug('user schema is %s',context['schema'])
    #log1.debug('user create data dict %s', data_dict)

    # Add orcid id field
    user_dict = ckan_user_create(context, data_dict)
    
    user_extra = ue_model.UserExtra(user_id=user_dict['id'], key='orcid_id', value='') 
    model.Session.add(user_extra)
    model.Session.commit()

    user = model.User.get(user_dict['id'])
    org_name = config.get('ckan.userautoadd.organization_name', '')
    role = config.get('ckan.userautoadd.organization_role', '')
    
    org_list = toolkit.get_action('organization_list')(
            context,{})
    if org_name not in org_list:
        return user

    member_dict = {
	'username': user.id,
	'id': org_name,
	'role': role
    }
    context['ignore_auth'] = True
    _get_action('organization_member_create')(context, member_dict) 
    
    
    return user

@validator_args
def modified_user_schema(ignore_missing, unicode_safe):
    modified_schema = user_new_form_schema()
    modified_schema['orcid_id'] = [ignore_missing, unicode_safe]
    return modified_schema