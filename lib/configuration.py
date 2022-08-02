from typing import IO, Union, Tuple
import logging
import argparse
import yaml
import cerberus

from .configuration_def import \
    RUNTIME_CLIENT_CONFIGURATION_DEFAULTS, RUNTIME_CLIENT_CONFIGURATION_CERBERUS_REGISTRY_KEY

VALIDATOR_SCHEMA = {
    'docker': {
        'type': 'dict',
        'schema': RUNTIME_CLIENT_CONFIGURATION_CERBERUS_REGISTRY_KEY,
        'required': False,
        'default': RUNTIME_CLIENT_CONFIGURATION_DEFAULTS,
        'allow_unknown': False,
    },
    'podman': {
        'type': 'dict',
        'schema': RUNTIME_CLIENT_CONFIGURATION_CERBERUS_REGISTRY_KEY,
        'required': False,
        'default': RUNTIME_CLIENT_CONFIGURATION_DEFAULTS,
        'allow_unknown': False,
    },
    'registries': 'registry-configurations',
    'images': 'images-configurations'
}

def app_argparse() -> Tuple['Client', dict]:
    parser = argparse.ArgumentParser(description='Build some container images.')
    parser.add_argument('-c', '--config',
        type=argparse.FileType(mode='r', bufsize=-1, encoding='UTF-8'),
        help='the configuration file to use',
    )
    parser.add_argument('--docker',
        action='store_true',
        help='use the Docker backend',
    )
    parser.add_argument('--podman',
        action='store_true',
        default=True,
        help='use the Podman backend',
    )
    parser.add_argument('--debug',
        action='store_true',
        default=True,
        help='enable debug logging',
    )

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.docker:
        backend = 'docker'
        logging.debug('Will use the Docker backend')
    else:
        backend = 'podman'
        logging.debug('Will use the Podman backend')


    logging.info('Starting application')

    configuration = read_configuration(args.config)
    runtime_client = get_backend(backend, configuration)

    return runtime_client, configuration


def read_configuration(stream: Union[IO, None]) -> dict:
    
    validator = cerberus.Validator()
    validator.allow_unknown = False

    if stream:
        logging.debug('Will read configuration [{}]'.format(stream.name))
        configuration = yaml.load(stream, Loader=yaml.SafeLoader)
    # Ensure not none
    configuration = configuration or {}

    if not validator.validate(document=configuration, schema=VALIDATOR_SCHEMA):
        raise RuntimeError('Unable to validate, got issues :{}'.format(
            ''.join(map(lambda error: '\n - {}:{}'.format(error[0], error[1]), validator.errors.items())),
        ))

    return validator.normalized(configuration)

def get_backend(backend: str, configuration: dict):

    if backend == 'docker':
        import docker
        _configuration = configuration['docker']
        tls_configuration = configuration['docker']['tls']
        del _configuration['tls']
        if not isinstance(tls_configuration, bool):
            tls_configuration = docker.TLSConfig(**tls_configuration)
        return docker.DockerClient(tls_configuration=tls_configuration, **_configuration)
    else:
        import podman
        _configuration = configuration['podman']
        del _configuration['tls']
        return podman.PodmanClient(**_configuration)
