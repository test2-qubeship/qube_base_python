import os
""" Class to set configurations
"""

from pkg_resources import resource_filename

DEFAULT_VERSION = 'v0.1'


class QubeConfig:
    QUBE_VERSION_FILE = resource_filename(
        'qube.src.resources', 'qube_version.txt')
    qube_config = None
    """
    Qube Config to pass around the jenkins server context
    """
    def __init__(self):
        self.default_ver = DEFAULT_VERSION
        self.version_str = None
        self.get_version()

    @classmethod
    def get_config(cls):
        if not cls.qube_config:
            cls.qube_config = QubeConfig()
        return cls.qube_config

    def get_version(self):
        if self.version_str:
            return self.version_str
        try:
            with open(QubeConfig.QUBE_VERSION_FILE, 'r') as f:
                version_str_file = f.read()
            if version_str_file:
                self.version_str = "{} ({})".\
                    format(self.default_ver, version_str_file.strip())
        except Exception as ex:
            self.version_str = self.default_ver

        return self.version_str
