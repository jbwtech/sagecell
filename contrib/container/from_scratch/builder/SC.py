import os
import docker
from docker import DockerClient

from _common import *
from _config import *


class SCImageBuilder():

    def __init__(self, image):

        if not image:
            raise ValueError("Image cannot be empty")
        else:
            log.info(f"Setting container image to: {image}")
            self._image = image
        self._client = None
        self._packages = []
        self._files = []


    @property
    def image(self):
        return self._image

    @property
    def files(self):
        return self._files

    @property
    def packages(self):
        return self._packages

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, client=[DockerClient, None]):
        try:
            self._client = client
            log.info(f"Client set to {client}")
        except Exception as e:
            log.info("Client NOT set!!!")

    def add_file(self, level, path):
        log.info(f"Adding file {path}")
        self.files.append({"level": level, "path":path})
        log.info(f"Adding packages to {level}")
        self._load_list(path, level)

    def _load_list(self, path, level):
        with open(path, 'r') as file:
            for line in file:
                pkg = line.strip()
                if pkg[0] == "#":
                    continue
                log.info(f"Package: {pkg}")
                self._packages.append({"level": level, "package": pkg})

    def list_packages(self, level=[str]):
        for pkg in self._packages:
            if pkg['level'] == level:
                print(pkg['level'] + " ==>> " + pkg['package'])

    def create(self, env=[dict,list,None]):
        try:
            log.info("Creating new build container")
            c = self._client.containers.run(self._image, detach=True, tty=True, auto_remove=True, environment=env)
            log.info(f"Build container ID: {c.id}")
            return c.id
        except Exception as e:
            log.info(f"An unexpected error occurred: {e}")

    def exec(self, container_id, command, stream=True):
        try:
            log.info(f"Exec ID: {container_id[0:11]}")
            log.info(f"Exec Command: {command}")
            c = self._client.containers.get(container_id)
            if stream != True:
                exit_code, result = c.exec_run(command, tty=True, stream=False)
                log.info(f"Output:\n{result.decode('utf-8')}")
                log.info(f"ExitCode: {exit_code}")
            else:
                exit_code, result = c.exec_run(command, tty=True, stream=True)
                for data in result:
                    log.info(data.decode())
                log.info(f"ExitCode: {exit_code}")
        except Exception as e:
            log.info(f"An unexpected error occurred: {e}")

    def install(self, container_id, level):
        try:
            pass
        except Exceptions as e:
            pass
