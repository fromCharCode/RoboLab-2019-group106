#!/usr/bin/env python3

import os
import subprocess


class Unix:
    """
    Deploy class for Unix systems
    """

    def __init__(self, configure, base_path, bin_path, settings):
        """
        Initializes Windows class, prepares environment defaults
        :param configure: Bool
        :param base_path: Pathlib
        :param bin_path: Pathlib
        :param settings: Dict
        """
        # Variables setup
        self.base_path = base_path
        self.bin_path = bin_path
        self.settings = settings
        self.ssh_key = bin_path.joinpath('brick_id_rsa')
        self.ssh_pub = bin_path.joinpath('brick_id_rsa.pub')

        # Path setup
        self.src_path = self.base_path.joinpath(self.base_path.parent, 'src')
        self.log_path = self.base_path.joinpath(self.base_path.parent, 'logs')

        # Start re-configuration or create new one
        if configure or not self.ssh_key.exists():
            self.__setup_deploy()

    def __setup_deploy(self):
        """
        Creates or updates SSH Key pair for Unix
        :return: void
        """
        # Create a SSH Key-pair and push it to the robot
        if not self.ssh_key.exists():
            subprocess.run(['ssh-keygen',
                            '-b', '4096',
                            '-t', 'rsa',
                            '-f', self.ssh_key,
                            '-q', '-N', ''
                            ])

        os.chmod(self.ssh_key, 0o600)
        os.chmod(self.ssh_pub, 0o600)
        print('Please enter the password if asked.')
        subprocess.run(
            ['ssh-copy-id',
             '-i', self.ssh_key,
             'robot@{}'.format(self.settings['ip'])
             ], stderr=open(os.devnull, 'wb'))
        print('Try to log into the brick:')
        print('\tssh -i {} robot@{}'.format(self.ssh_key, self.settings['ip']))

    def backup(self):
        """
        Backup existing files on the brick
        :return: void
        """
        print('Backing up old files...')

        # Connect with SSH-PubKey and execute backup script
        subprocess.run(
            ['ssh',
             '-i', self.ssh_key,
             '-o', 'StrictHostKeyChecking=no',
             'robot@{}'.format(self.settings['ip']),
             'robolab-backup'
             ])

        print('Done.')

    def copy_files(self):
        """
        Copy local files to brick
        :return: void
        """
        print('Copying new files...')

        # Connect with SSH-PubKey and copy files
        subprocess.run(
            ['scp',
             '-i', self.ssh_key,
             '-o', 'StrictHostKeyChecking=no',
             '-r', self.src_path,
             'robot@{}:/home/robot/'.format(self.settings['ip'])
             ])

        print('Done.')

    def sync_log(self):
        """"
        Sync tmux log files from the brick
        :return: void
        """
        print('Synchronizing log files...')

        # Connect with SSH-PubKey and synchronize files
        subprocess.run(
            ['scp',
             '-i', self.ssh_key,
             '-o', 'StrictHostKeyChecking=no',
             'robot@{}:/home/robot/.bin/*_tmux.log'.format(self.settings['ip']),
             self.log_path
             ])

        print('Done.')

    def start_session(self):
        """
        Spawn or enter tmux session on brick
        :return: void
        """
        print('Executing code by running main.run()...')
        print('This will open a tmux session...')
        print('Detach by pressing CTRL + B and then D')

        # Connect with SSH-PubKey and execute tmux script
        subprocess.run(
            ['ssh',
             '-i', self.ssh_key,
             '-o', 'StrictHostKeyChecking=no',
             'robot@{}'.format(self.settings['ip']),
             '-t', 'robolab-tmux'
             ])

        print('Done.')
