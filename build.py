#!/usr/bin/env python3

from lib import app_argparse
import json
import logging
import traceback
import sys
import functools
from typing import List

from docker.errors import DockerException
from podman.errors import APIError as PodmanAPIError

HANDLED_ERRORS = (DockerException, PodmanAPIError)


LOG_FORMAT = '%(asctime)s\t%(levelname)s\t[%(filename)s:%(lineno)s]\t%(message)s'
LOG_DATE_FORMAT = '%Y-%M-%d %H:%m:%S'


class StepError(object):
    
    def __init__(self, image: str, step: str, exception: Exception):
        self.image = image
        self.step = step
        self.exception = exception

    def __str__(self) -> str:
        return 'Image [{}], step [{}]\nGot exception :\n\t{}'.format(
            self.image,
            self.step,
            StepError.format_exception(self.exception).replace('\n', '\n\t'),
        ).replace('\n', '\n\t')

    @staticmethod
    def format_exception(exception: Exception):
        return ''.join(traceback.format_exception(
            type(exception),
            exception,
            exception.__traceback__
        ))

def _log_to_string(log_line):
    return json.loads(log_line).get('stream', '')

def format_errors(errors: List[StepError]) -> str:
    '''
        List of errors to a format like :
        ```text
            - ${IMAGE_NAME}
              -> [... error 1]
              -> [... error 2]
              [...]
        ```
    '''
    def _reduce_by_image(values: dict, element: StepError) -> dict:
        if element.image in values:
            values[element.image].append(element)
        else:
            values[element.image] = [element]
        return values

    msg = ''

    for image_name, image_errors in functools.reduce(_reduce_by_image, errors, {}).items():
        msg += '- {}{}'.format(
            image_name,
            ''.join(map(
                lambda image_error: '\n\t-> {} ({})'.format(
                    image_error.step,
                    str(image_error.exception),
                ),
                image_errors,
            )),
        )

    return msg


if __name__ == '__main__':

    logging.basicConfig(format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

    errors = []
    
    client, config = app_argparse()

    logging.info('Logging to the backends')
    for registry_url, registry_args in config['registries'].items():
        logging.info('Logging in with [{}] using username [{}]'.format(registry_url, registry_args['username']))
        client.login(registry=registry_url, **registry_args)
        logging.info('Done')

    for image_name, image_def in config['images'].items():
        try:
            image_def_tags = image_def['tags']

            logging.info('Building image [{}]'.format(image_name))
            image, logs = client.images.build(**image_def)
            logging.debug(''.join(map(_log_to_string, logs)))
            
            for tag_name in image_def_tags:
                try:
                    logging.info('Tagging image [{}] with tag [{}]'.format(image_name, tag_name))
                    image.tag(image_name, tag_name)
                except HANDLED_ERRORS as ex:
                    logging.debug(ex)
                    errors.append(StepError(image_name, 'Tagging image with tag {}'.format(tag_name), ex))

                try:
                    logging.info('Pushing image [{}] with tag [{}]'.format(image_name, tag_name))
                    logs = client.images.push(image_name, tag_name)
                    logging.debug(''.join(map(_log_to_string, logs)))
                except HANDLED_ERRORS as ex:
                    logging.debug(ex)
                    errors.append(StepError(image_name, 'Pushing image with tag {}'.format(tag_name), ex))

        except HANDLED_ERRORS as ex:
            logging.debug(ex)
            errors.append(StepError(image_name, 'Building image', ex))

    if len(errors) > 0:
        logging.error('Some errors occured :\n{}'.format(
            format_errors(errors)
        ))
        sys.exit(1)
    else:
        sys.exit(0)