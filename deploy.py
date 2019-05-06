#!/usr/bin/env python3

import argparse
import json
import os
from pathlib import Path
import platform
import subprocess

from lib.ip_check import *
from lib.unix import Unix
from lib.windows import Windows


class Deploy:
    """
    Base class for RoboLab Deploy-Script
    """

    def __init__(self, configure=False, execute_only=True, backup=False, sync_log=False):
        """
        Initializes Deploy-Script, creates all necessary folders and files, loads environment defaults
        :param configure: boolean
        :param execute_only: boolean
        :param backup: boolean
        :param sync_log: boolean
        """
        # Flags and variables setup
        self.configure = configure
        self.execute_only = execute_only
        self.backup = backup
        self.sync_log = sync_log
        self.settings = dict()

        # Path and File setup
        self.base_path = Path(os.path.dirname(os.path.abspath(__file__)))
        self.bin_path = self.base_path.joinpath('.bin')
        self.bin_path.mkdir(mode=0o700, exist_ok=True)
        self.settings_file = self.bin_path.joinpath('settings.json')

        # Start re-configuration or create new one
        if self.configure or not self.settings_file.exists():
            self.__setup_deploy()
        # Load configuration
        with self.settings_file.open() as file:
            self.settings = json.load(file)

        # Check system capabilities
        # @TODO: Disabled for now because rsync has problems with "-e 'ssh ...'"
        # self.__check_requirements()

    def routine(self):
        """
        Handle flags and starts tmux session
        :return: void
        """
        if self.settings['os'] == 'Windows':
            system = Windows(self.configure,
                             self.base_path,
                             self.bin_path,
                             self.settings)
        else:
            system = Unix(self.configure,
                          self.base_path,
                          self.bin_path,
                          self.settings)

        if self.backup:
            system.backup()
            return

        if self.sync_log:
            system.sync_log()
            return

        if self.execute_only:
            system.copy_files()

        system.start_session()

        return

    def __setup_deploy(self):
        """
        Creates or updates Deploy-Script configuration
        :return: void
        """
        init_dict = dict()
        init_dict['os'] = platform.system()
        init_dict['ip'] = ip_check()

        # Dump data into file
        self.settings_file.touch()
        with self.settings_file.open('w') as file:
            json.dump(init_dict, file, indent=4)

    def __check_requirements(self):
        """
        Checks system capabilities, e.g. required binaries
        :return: void
        """
        try:
            subprocess.call(
                ["rsync"],
                stdout=open(os.devnull, 'w'),
                stderr=open(os.devnull, 'w')
            )
        except OSError:
            print('"rsync" not found, abort!')
            raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--configure', help='Create new or reset current configuration', action='store_true')
    parser.add_argument(
        '-e', '--execute-only', help='Execute only without copying new files', action='store_false', default=True)
    parser.add_argument(
        '-b', '--backup', help='Create a remote backup of your files on the brick', action='store_true', default=False)
    parser.add_argument(
        '-s', '--sync-log', help='Synchronize log files from the brick', action='store_true', default=False)
    args = parser.parse_args()

    try:
        print('If you need to change the IP address or your underlying OS, please run\n\t./deploy.py -c')
        deploy = Deploy(args.configure, args.execute_only, args.backup, args.sync_log)
        deploy.routine()
    except Exception as e:
        print(e)
        raise
