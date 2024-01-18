"""This module is responsible for the layout and functionality of the settings tab
in Scheduler."""

from nicegui import ui

from OpenOrchestrator.common.connection_frame import ConnectionFrame


# pylint: disable-next=too-few-public-methods
class SettingsTab():
    """The settings tab object for Scheduler."""
    def __init__(self, tab: ui.tab) -> None:
        with ui.tab_panel(tab):
            ConnectionFrame()
