from __future__ import annotations

from collections import namedtuple
from configparser import ConfigParser
from configparser import Interpolation
import os
from pathlib import Path
from pathlib import PurePath
from time import time
from typing import Any
from typing import Optional
from typing import Tuple


class NameConfigError(Exception):
    """
    Occurs when there is an error in the name of the file.
    For example there is no such file at all.
    """


class BackupConfigError(OSError):
    """
    Occurs when a backup of a file is impossible.
    For example, you can't read the original settings file,
    or you don't have written access to the directory.
    """


class OperationConfigError(Exception):
    """
    Occurs when an option written to a configuration file is duplicated.
    Or when a configuration file parsing error has occurred.
    """


class AccessConfigError(OSError):
    """
    Occurs when writing to the configuration file failed.
    Because of the lack of write permissions to the file
    or the lack of the file itself.
    """


class RebuildConfigError(Exception):
    """
    Occurs when the configuration file could not be restored.
    Because of the lack of permissions to write to the file
    or the absence of the file itself.
    """


class CopyConfigError(Exception):
    """
    Occurs when it was not possible to copy old configuration file to new one.
    Because there are no write permissions to the file or because the file
    itself is missing.
    """


class ConfigHandler:
    """
    Main module for work with program settings contains in configuration file.
    By default, it is config.ini

    Args:
        name (str): name of configuration file.
        interpolation: Interpolation behaviour may be customized by providing
            a custom handler through the interpolation argument,
            by default it is BasicInterpolation. None can be used to turn off
            interpolation completely, ExtendedInterpolation provides a more
            advanced variant inspired by zc.buildout. More on the subject in
            the dedicated documentation section for build-ins configparser
            modules.
    """

    _directory: Optional[str]

    def __init__(self,
                 name: str = 'config.ini',
                 interpolation: Interpolation = None) -> None:
        self._name = str(name)
        self._directory = None
        self._interpolation = interpolation
        self._set_configparser(self._name,
                               self._directory)

    def _set_configparser(self,
                          name: str,
                          directory: Any) -> None:
        """
        Starts process of finding a configuration file.
        Configures configparser module to work with it.

        Args:
            name (str): name of configuration file
            directory (Any): directory name which contain configuration file,
                e.g.: tests/fixtures

        Returns:
            None
        """

        self.file_path = self._search_config(name=name,
                                             directory=directory)
        self._config = ConfigParser(interpolation=self._interpolation)
        self._config.read(self.file_path)

    @staticmethod
    def _copy_string(src: str | PurePath,
                     dst: str | PurePath) -> str:
        """
        Copies data line by line from one file to another.

        Args:
            src (str, PurePath): source file path
            dst (str, PurePath): destination file path

        Returns:
            (str): Copied string success

        Raises:
            CopyConfigError: no write permissions to the file or because
                the file itself is missing.
        """

        try:
            with open(dst, "w+") as new_file:
                old_file = open(src, 'r')
                new_file.write(old_file.read())
                old_file.close()
        except OSError as err:
            raise CopyConfigError(err)
        else:
            return "Copied string success"

    def __str__(self) -> str:
        """
        Returned string which contains file path for opened config file.

        Returns:
            (str): Config: /path/to/the/file/config.ini
        """

        return f"Config: {self.file_path}"

    def __repr__(self) -> str:
        """
        Return name of created class and parameters send to class object.

        Returns:
            (str): Class __name__ with: config_name=config.ini,
            root_directory=None, preprocessed value=None.
        """

        return "".join((f"Class {self.__class__.__name__} with ",
                        f"config_name= {self._name}, ",
                        f"root_directory= {self._directory}, ",
                        f"preprocessed value= {self._interpolation}"))

    @staticmethod
    def _search_config(name: str,
                       directory: Any) -> str:
        """
        Searching config file and create full path to it.
        Args:
            name (str): name of configuration file
            directory (Any): directory name which contain configuration file,
                e.g.: tests/fixtures
        Returns:
            (str): /path/to/config/file/config.ini
        Raises:
            NameConfigError: no such a file.
        """

        full_path = Path(__file__)
        test_path = ''.join((name, str(directory)))
        for number in range(len(full_path.parents)):
            if directory is None:
                test_path = PurePath(full_path.parents[number],
                                     name)
            else:
                test_path = PurePath(full_path.parents[number],
                                     directory,
                                     name)
            if Path(test_path).is_file():
                return str(test_path)
        message = f"{name} in {test_path} not found"
        raise NameConfigError(message)

    def _backup_config_file(self) -> tuple[str, PurePath]:
        """
        Creating a backup copy of the configuration file.
        Also, addition at the end of the name this string: BAK + Unix time.

        Returns:
            tuple(str, PurePath): Tuple contains string 'Backup config.ini
            to: /path/to/config/file' and path-like file object.

        Raises:
            BackupConfigError: can't read the original settings file,
            or you don't have written access to the directory.
        """

        backup_config_name = "".join((self._name,
                                      ".BAK+",
                                      str(int(time()))))
        file_path = PurePath(self.file_path).parents[0]
        new_config = PurePath(file_path,
                              backup_config_name)
        try:
            self._copy_string(src=self.file_path,
                              dst=new_config)
        except CopyConfigError as err:
            os.remove(new_config)
            raise BackupConfigError(err)
        else:
            message = f"Backup config.ini to: {new_config}"
            return message, new_config

    def _to_dict(self) -> dict:
        """
        Read parameters contained in configuration file and convert to dict.

        Returns:
            dict: contains all validated parameters
        """

        sections = self._config.sections()
        items = [self._config.items(section) for section in sections]
        all_item = []
        for item in items:
            for i in item:
                all_item.append(i)
        return dict(all_item)

    def _rebuild_config(self,
                        orig_config: str = 'example_config.ini',
                        new_config: str = 'config.ini',
                        directory: str = 'tests/fixtures') -> str:
        """
        Restoring the configuration file.
        Copying lines from example_config.ini to config.ini file.

        Args:
            orig_config (str): default 'example_config.ini'
            new_config (str): default 'config.ini'
            directory (str): default 'tests/fixtures'

        Returns:
            (str): Config rebuild success

        Raises:
            RebuildConfigError: the lack of permissions to write to file
                or the absence of file itself
        """

        try:
            self._copy_string(self._search_config(name=orig_config,
                                                  directory=None),
                              self._search_config(name=new_config,
                                                  directory=directory))
        except CopyConfigError as err:
            raise RebuildConfigError(err)
        else:
            return 'Config rebuild success'

    @property
    def root_directory(self) -> str | None:
        """
        Reports name of directory that is set for initial search config file.

        Returns:
            (str, None): name of directory, if None that mean root directory
            corresponds to the main (uppermost) project directory
        """

        return self._directory

    @root_directory.setter
    def root_directory(self,
                       name: str) -> None:
        """
        Sets a new name for the root directory.

        Args:
            name(str): new name root directory

        Returns:
            None
        """

        self._directory = str(name)
        self._set_configparser(name=self._name,
                               directory=self._directory)

    @property
    def config_name(self) -> str:
        """
        Parameter that reports name of configuration file.

        Returns:
            (str): name of configuration file
        """

        return self._name

    @config_name.setter
    def config_name(self,
                    name: str) -> None:
        """
        Sets of new name for configuration file.

        Args:
            name(str): new name for configuration file

        Returns:
            None
        """

        self._name = str(name)
        self._set_configparser(name=self._name,
                               directory=self._directory)

    def read(self) -> Any:
        """
        Read settings from a configuration file.
        Also, validate settings and generate a named tuple with key=value
        parameters.

        Returns:
            Config (namedtuple): with key=value
        """

        valid = self._to_dict()
        valid_copy = valid.copy()
        namedtuple_key = []
        while len(valid) > 0:
            key, _ = valid.popitem()
            namedtuple_key.append(key)

        Config = namedtuple("Config", namedtuple_key)  # type: ignore
        return Config(**valid_copy)  # type: ignore

    def write(self,
              section: str,
              key: str,
              value: Any,
              backup: bool = True) -> tuple[str, PurePath | None]:
        """
        Writing new settings to the server configuration file.
        The backup option is used to select whether to save the previous
        settings to a special file or not.
        Args:
            section (str):  each led by a [section] header
            key (str): name of parameters
            value (Any): value of parameters, auto converted to string object
            backup (bool): save or not previous settings, default True
        Returns:
            tuple (str, PurePath | None): Tuple which contain string
            'Completed' and path-like object with backup file link or None
            if set backup is False
        Raises:
            AccessConfigError: lack of write permissions to the file
                or the lack of the file itself
        """
        backup_info: Tuple[Optional[str], Optional[PurePath]]

        if backup:
            backup_info = self._backup_config_file()
        else:
            backup_info = (None, None)

        section = section.upper()
        value = str(value)

        if self._config.has_section(section):
            self._config.set(section=section,
                             option=key,
                             value=value)
        else:
            self._config.add_section(section)
            self._config.set(section=section,
                             option=key,
                             value=value)
        try:
            with open(self.file_path, 'w+') as config_file:
                self._config.write(config_file)
        except OSError as err:
            raise AccessConfigError(err)
        else:
            backup_file = backup_info[1]
            return 'Completed', backup_file
