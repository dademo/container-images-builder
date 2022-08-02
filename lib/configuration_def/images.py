##
IMAGE_CONFIGURATION_DEFAULTS = {}
##
IMAGE_NAME_REGEX = r'^(https?://)?[^\s/]+/[^\s/]+/[^\s/]+?$'
IMAGE_CONFIGURATION = {
    'type': 'dict',
    'keysrules': {
        'type': 'string',
        'regex': IMAGE_NAME_REGEX,
    },
    'valuesrules': {
        'type': 'dict',
        'schema': {
            # https://docker-py.readthedocs.io/en/stable/images.html#docker.models.images.ImageCollection.build
            'path': {'type': 'string', 'required': True},
            'tags': {'type': 'list', 'required': False, 'schema': {'type':'string'}, 'default': ['latest']},
            'nocache': {'type': 'boolean', 'required': False, 'default': False},
            'rm': {'type': 'boolean', 'required': False, 'default': True},
            'timeout': {'type': 'integer', 'required': False},
            'pull': {'type': 'boolean', 'required': False},
            'forcerm': {'type': 'boolean', 'required': False},
            'dockerfile': {'type': 'string', 'required': False},
            'buildargs': {'type': 'dict', 'required': False},
            'labels': {'type': 'dict', 'required': False},
            'network_mode': {'type': 'string', 'required': False},
            'squash': {'type': 'boolean', 'required': False},
            'extra_hosts': {'type': 'dict', 'required': False},
        },
    },
    'default': {},
}

## Internal
def _load_cerberus_registries():
    import cerberus
    cerberus.rules_set_registry.extend({
        'images-configurations': IMAGE_CONFIGURATION
    })


# We will load IMAGE when loading
_load_cerberus_registries()