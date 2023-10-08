"""
The configuration options of the tracker.
"""
from __future__ import annotations

import collections
import pathlib
import warnings
from typing import Any

import tracker_utils
import yaml

# TODO: Take the default values from the JSON schema validator file
DEFAULT_CONFIG = tracker_utils.ROOT / "resources/configuration.yaml"


def get_configuration(filepath: str = DEFAULT_CONFIG) -> Configuration:
    """
    Read the ``configuration.yaml`` into a Configuration object.
    """
    warnings.warn(
        "This function is deprecated, use `Configuration.from_default()` instead.",
        DeprecationWarning,
    )
    return Configuration.from_default(filepath)


def _get_configuration(filepath: str = DEFAULT_CONFIG) -> Configuration:
    """
    Read the configuration YAML files into a Configuration object.

    Uses two different configuration files: a default one that build with the
    application, and one for the user to edit.

    TODO: Include the API tokens/keys/secrets in the config file (#5)
    """
    with open(filepath) as f_custom, open(DEFAULT_CONFIG) as f_base:
        config = yaml.load(f_custom.read(), yaml.Loader)

        config["tracker"]["options"] = collections.ChainMap(
            config["tracker"]["options"],
            yaml.load(f_base.read(), yaml.Loader)["tracker"]["options"],
        )

        return Configuration(config)


class Configuration:
    """
    The configuration of the tracker.

    Extremely simple implementation -- will expand this in the future to be more
    dynamic. Or just leave as a simple dict?

    The docstrings should be taken from the ``description`` property.
    """

    def __init__(self, configuration: dict):
        self.configuration = configuration
        self.options = self.configuration["tracker"]["options"]

    @classmethod
    def from_default(cls, filepath: str = DEFAULT_CONFIG) -> Configuration:
        """
        Read the ``configuration.yaml`` into a Configuration object.

        The ``filepath`` parameter is only included for backwards compatibility
        and will be removed.
        """
        with open(filepath) as f:
            return Configuration(yaml.load(f.read(), yaml.Loader))

    def _get_option_value(self, option: str, default: Any) -> Any:
        return self.options.get(option, default)

    @property
    def interval(self) -> int:
        return self._get_option_value("interval", False)

    @property
    def run_on_startup(self) -> bool:
        return self._get_option_value("run-on-startup", False)

    @property
    def show_last_n_weeks(self) -> int:
        return self._get_option_value("show-last-n-weeks", 2)

    @property
    def use_calendar_appointments(self) -> bool:
        return self._get_option_value("use-calendar-appointments", False)

    @property
    def appointment_category_exclusions(self) -> list[str]:
        return self._get_option_value("appointment-category-exclusions", None)

    @property
    def linked_calendar(self) -> str:
        return self._get_option_value("linked-calendar", None)

    @property
    def use_jira_sprint(self) -> bool:
        return self._get_option_value("use-jira-sprint", False)

    @property
    def post_to_slack(self) -> bool:
        return self._get_option_value("post-to-slack", False)

    @property
    def post_to_jira(self) -> bool:
        return self._get_option_value("post-to-jira", False)

    @property
    def save_csv_copy(self) -> bool:
        return self._get_option_value("save-csv-copy", False)

    @property
    def csv_filepath(self) -> str:
        return self._get_option_value("csv-filepath", str(pathlib.Path.home()))