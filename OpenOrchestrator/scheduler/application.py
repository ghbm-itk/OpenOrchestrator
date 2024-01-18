"""This module is the entry point for the Scheduler app. It contains a single class
that when created starts the application."""

from nicegui import ui, app

from OpenOrchestrator.scheduler.settings_tab import SettingsTab
from OpenOrchestrator.scheduler.run_tab import RunTab


# pylint: disable-next=too-few-public-methods
class Application():
    """The main application object of the Scheduler app."""
    def __init__(self) -> None:
        with ui.header():
            with ui.tabs() as self.tabs:
                ui.tab('Run')
                ui.tab('Settings')

            ui.space()
            # TODO: Dark mode

        with ui.tab_panels(self.tabs, value='Settings').classes('w-full'):
            RunTab('Run')
            SettingsTab("Settings")

        self._define_on_close()
        app.on_disconnect(app.shutdown)
        ui.run(title="Scheduler", favicon='🤖', native=False, port=34538, reload=True)  # TODO: Set reload false

    def _define_on_close(self) -> None:
        """Tell the browser to ask for confirmation before leaving the page."""
        ui.add_body_html('''
            <script>
                window.addEventListener("beforeunload", (event) => event.preventDefault());
            </script>
            ''')


if __name__ in {'__main__', '__mp_main__'}:
    Application()
