import os
import docker
from docker import DockerClient

from _common import *
from _config import *


class SCImageBuilder():

    #"""
    # Constructor that takes the name of the docker container image to use
    # as the starting point for the build
    #"""
    def __init__(self, image):

        if not image:
            raise ValueError("Image cannot be empty")

        log.info(f"Setting container image to: {image}")

        try:
            repository, tag = image.split(":")
        except ValueError:
            log.info(f"Using default tag: latest")
            image += ":latest"

        self._image = image
        self._client = None
        self._packages = []
        self._files = []


    #"""
    # Base docker container image
    #"""
    @property
    def image(self):
        return self._image

    #"""
    # Files that have the lists of packages to install
    #"""
    @property
    def files(self):
        return self._files

    #"""
    # List of all packages to be installed and what level to install them
    #"""
    @property
    def packages(self):
        return self._packages

    #"""
    # The client is the connection to the docker daemon
    #"""
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

    #"""
    # Adds the packages listed in the given file to the list of packages to
    # be installed in the specified level
    #"""
    def add_file(self, level, path):
        log.info(f"Adding file {path}")
        self.files.append({"level": level, "path":path})
        log.info(f"Adding packages to {level}")
        
        with open(path, 'r') as file:
            for line in file:
                pkg = line.strip()
                if pkg[0] == "#":
                    continue
                log.info(f"Package: {pkg}")
                self._packages.append({"level": level, "package": pkg})

    #"""
    #
    #"""
    def list_packages(self, level=[str]):
        for pkg in self._packages:
            if pkg['level'] == level:
                print(pkg['level'] + " ==>> " + pkg['package'])

    #"""
    #
    #"""
    def create(self, env=[dict,list,None]):
        try:
            log.info("Creating new build container")
            c = self._client.containers.run(self._image, detach=True, tty=True, auto_remove=True, environment=env)
            log.info(f"Build container ID: {c.id}")
            return c.id
        except Exception as e:
            log.info(f"An unexpected error occurred: {e}")

    #"""
    #
    #"""
    def exec(self, cid, command, stream=True):
        try:
            log.info(f"Exec ID: {cid[0:11]}")
            log.info(f"Exec Command: {command}")
            c = self._client.containers.get(cid)
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

    #"""
    #
    #"""
    def build(self, cid, target):
        try:
            c = self._client.containers.get(cid)
            log.info(f"Build: {target}")
            log.info(f"ID: {c.short_id}")
        except Exceptions as e:
            pass

        install_list = ''

        for item in self._packages:
            if item['level'] == target:
                install_list = install_list + item['package'] + ' '

        command = f"bash -c 'apt install -y --no-install-recommends {install_list}'"

        self.exec(cid, command)
