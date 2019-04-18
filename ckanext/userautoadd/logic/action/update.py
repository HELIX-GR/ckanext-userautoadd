import pylons.config as config

import ckan.logic as logic
import ckan.model as model
import ckan.lib as lib
from ckan.logic.action.update import user_update as ckan_user_update
from ckan.logic.schema import validator_args, default_user_schema

import ckan.plugins.toolkit as toolkit
import logging
log1 = logging.getLogger(__name__)
_get_action = logic.get_action

import ckanext.userautoadd.model as ue_model

def user_update(context, data_dict):
    #context['schema'] = modified_user_schema()
    session = context['session']
    
    #log1.debug('user schema is %s',context['schema'])
    user_dict = ckan_user_update(context, data_dict)
    user_extra = ue_model.UserExtra.get(user_id=user_dict['id'], key='orcid_id')
    if user_extra is None:
        raise NotFound
    user_extra.value = data_dict['orcid_id']
    session.add(user_extra)
    session.commit()
    return user_dict

@validator_args
def modified_user_schema(ignore_missing,name_validator,user_password_validator, user_name_validator, unicode_safe):
    modified_schema = default_user_schema()
    
    modified_schema['name'] = [
        ignore_missing, name_validator, user_name_validator, unicode_safe]
    modified_schema['password'] = [
        user_password_validator, ignore_missing, unicode_safe]
    modified_schema['orcid_id'] = [ignore_missing, unicode_safe]

    return modified_schema