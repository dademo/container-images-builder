RUNTIME_CLIENT_CONFIGURATION_CERBERUS_REGISTRY_KEY = 'container-runtime-client-configuration'

##
RUNTIME_CLIENT_CONFIGURATION_DEFAULT_URI = r'unix:///var/run/docker.sock'
RUNTIME_CLIENT_CONFIGURATION_DEFAULT_TIMEOUT = 10
RUNTIME_CLIENT_CONFIGURATION_DEFAULT_TLS = False
RUNTIME_CLIENT_CONFIGURATION_DEFAULTS = {
    'base_url': RUNTIME_CLIENT_CONFIGURATION_DEFAULT_URI,
    'timeout': RUNTIME_CLIENT_CONFIGURATION_DEFAULT_TIMEOUT,
    'tls': RUNTIME_CLIENT_CONFIGURATION_DEFAULT_TLS,
}
##
BASE_URI_REGEX = r'^(?:http\+(?:unix|ssh)|unix|ssh|tcp|http)://[^\s]+$'
RUNTIME_CONNECTION_CONFIGURATION = {
    # https://docker-py.readthedocs.io/en/stable/client.html#docker.client.DockerClient
    'base_url': {
        'type': 'string',
        'regex': BASE_URI_REGEX,
        'required': False,
        'default': RUNTIME_CLIENT_CONFIGURATION_DEFAULTS,
    },
    'version': {
        'type': 'string',
        'required': False,
    },
    'timeout': {
        'type': 'integer',
        'required': False,
        'default': RUNTIME_CLIENT_CONFIGURATION_DEFAULT_TIMEOUT,
    },
    'tls': {
        'type': ['boolean', 'dict'],
        'required': False,
        'default': RUNTIME_CLIENT_CONFIGURATION_DEFAULT_TLS,
        'schema': {
            'client_cert': {
                'type': 'list',
                'schema': {'type': 'string'},
                'required': True,
            },
            'ca_cert': {
                'type': 'string',
                'required': False,
            },
            'verify': {
                'type': ['boolean', 'string'],
                'required': False,
            },
            'ssl_version': {
                'type': 'integer',
                'required': False,
            },
            'assert_hostname': {
                'type': 'boolean',
                'required': False,
            },
        },
    },
    'user_agent': {
        'required': False,
    },
}

## Internal
def _load_cerberus_registries():
    import cerberus
    cerberus.schema_registry.add(RUNTIME_CLIENT_CONFIGURATION_CERBERUS_REGISTRY_KEY, RUNTIME_CONNECTION_CONFIGURATION)


# We will load registry when loading
_load_cerberus_registries()