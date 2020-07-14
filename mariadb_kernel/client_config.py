"""ClientConfig deals with the args passed to the MariaDB client"""

# Copyright (c) MariaDB Foundation.
# Distributed under the terms of the Modified BSD License.

import os
import json


class ClientConfig:
    def __init__(self, log, name="mariadb_config.json"):
        self.log = log
        self.config_name = name
        self.default_config = {
            "user": "root",
            "host": "localhost",
            "port": "3306",
            "password": "",
        }

        self._load_config()

    def _load_config(self):
        path = self._config_path()
        self.log.info(f"Loading config file at {path}...")
        cfg = {}
        using_default = False

        try:
            f = open(path, "r")
            cfg = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            if isinstance(e, OSError):
                self.log.info(
                    f"Config file {self.config_name} at {path} " "does not exist"
                )
            if isinstance(e, json.JSONDecodeError):
                self.log.info(
                    f"Config file {self.config_name} at {path} "
                    f"is not valid JSON: {e}"
                )
            using_default = True

        # We should abort loading the custom config if the user passes
        # an unsupported option
        customk = cfg.keys()
        defaultk = self.default_config.keys()
        if len(customk - defaultk) > 0:
            self.log.info(
                f"Config file {self.config_name} at {path} "
                f"contains unsupported options: {customk - defaultk}"
            )
            using_default = True

        if using_default:
            self.log.info(f"Using default config: {self.default_config}")
            return

        self.default_config.update(cfg)

    def _config_path(self):
        default_dir = os.path.join(os.path.expanduser("~"), ".jupyter")
        custom_dir = os.environ.get("JUPYTER_CONFIG_DIR")
        if custom_dir:
            default_dir = custom_dir
        return os.path.join(default_dir, self.config_name)

    def get_args(self):
        rv = ""
        for key, value in self.default_config.items():
            rv += f"--{key}={value} "
        return rv
