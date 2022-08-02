# Container image builder

A simple script to build images using Docker or podman Python API.

You can configure every backend using the configuration file (default values will be applied else, see files in the [configuration_def package](lib/configuration_def/)).

The script will first try to login to every registry you described in the `registries` section.

You will need to define every build you want the script to do in the `images` section of your configuration file. It will build the image and then for every tag you provided (or only `latest` by default) it will tag the image and push it to the registry defined in the image name.

# Example configuration

```yaml
podman:
  base_url: unix:///run/user/1000/podman/podman.sock

registries:
  docker.io:
    username: dademo0
    dockercfg_path: /home/dademo/.docker/config.json

images:
  nexus.dademo.fr:5005/build_images/gradle_runner:
    path: images/gradle_runner
    dockerfile: Containerfile
    squash: true
    tags:
      - latest
      - 0.0.1
```