"""
Connect the various subpackages throughout the project to couple up the objects.
"""
import datetime
import logging
import logging.config

import actions
import core
import core.create
import tracker_utils
import yaml

APPLICATION_CREATED = True


def create_form(at_datetime: datetime.datetime) -> None:
    """
    Launch the tracker.
    """
    actions.ActionHandler(at_datetime)


def main() -> None:
    """
    Entry point into this project.
    """
    with open(tracker_utils.ROOT / "logger.yaml") as f:
        logging.config.dictConfig(yaml.safe_load(f.read()))

    logging.info("Starting tracker...")
    logging.debug(f"Setting root directory to {tracker_utils.ROOT}")

    # Just for testing
    create_form(datetime.datetime.now())
    quit()

    if APPLICATION_CREATED:
        scheduler = core.scheduler.IndefiniteScheduler(create_form)
        scheduler.schedule_first()
    else:
        # core.create.create_env()
        db_handler = core.DatabaseHandler(
            tracker_utils.ROOT / "tracker.db",
            core.configuration.get_configuration(),
        )
        # db_handler.import_history(tracker_utils.ROOT / "tracker.csv")


if __name__ == "__main__":
    main()