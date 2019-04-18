import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import ckanext.userautoadd.logic.action.create
import ckanext.userautoadd.logic.action.update

import ckanext.userautoadd.helpers as h_user_extra

class UserautoaddPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'userautoadd')

    # IActions
    def get_actions(self):
        return {
            'user_create':
            ckanext.userautoadd.logic.action.create.user_create,
            'user_update':
            ckanext.userautoadd.logic.action.update.user_update,
        }
    # IConfigurable
    def configure(self, config):
        import ckanext.userautoadd.model as user_extra_model
        user_extra_model.setup()

    def get_helpers(self):
        return {'get_user_extra': h_user_extra.get_user_extra}
