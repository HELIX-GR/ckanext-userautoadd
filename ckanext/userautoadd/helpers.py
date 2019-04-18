import ckanext.userautoadd.model as user_model
import ckan.logic as logic
import ckan.model as model
from ckan.common import _, c

get_action = logic.get_action


def get_user_extra(user_id=None):
    context = {'model': model, 'session': model.Session,
               'user': c.user or c.author, 'auth_user_obj': c.userobj}
    id = c.userobj.id if user_id is None else user_id

    data_dict = {'user_obj': c.userobj, 'user_id': id}

    user_id = data_dict.get('user_id')
    user_extra_list = user_model.UserExtra.get_by_user(user_id=user_id)
    if user_extra_list is None:
        raise NotFound
    if user_extra_list:
        return user_extra_list[0].value
    return 