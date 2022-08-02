##
REGISTRY_CONFIGURATION_DEFAULTS = {}
##
REGISTRY_URI_REGEX = r'^(https?://)?[^\s/]+/?$'
REGISTRY_CONFIGURATION = {
    'type': 'dict',
    'keysrules': {
        'type': 'string',
        'regex': REGISTRY_URI_REGEX,
    },
    'valuesrules': {
        'type': 'dict',
        'schema': {
            # https://docker-py.readthedocs.io/en/stable/client.html#docker.client.DockerClient.login
            'username': {'type': 'string', 'required': True},
            'password': {'type': 'string', 'required': False},
            'email': {'type': 'string', 'required': False},
            'dockercfg_path': {'type': 'string', 'required': False},
        },
    },
    'default': {},
}

## Internal
def _load_cerberus_registries():
    import cerberus
    cerberus.rules_set_registry.extend({
        'registry-configurations': REGISTRY_CONFIGURATION
    })


# We will load registry when loading
_load_cerberus_registries()