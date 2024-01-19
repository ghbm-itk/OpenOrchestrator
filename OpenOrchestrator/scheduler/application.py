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
            ui.button(icon="contrast", on_click=ui.dark_mode().toggle)

        with ui.tab_panels(self.tabs, value='Settings', on_change=self._update_tab).classes('w-full') as self.tab_panels:
            self.run_tab = RunTab('Run')
            SettingsTab("Settings")

        self._define_on_close()
        app.on_disconnect(app.shutdown)
        ui.run(title="Scheduler", favicon='🤖', native=False, port=34538, reload=False)

    def _define_on_close(self) -> None:
        """Tell the browser to ask for confirmation before leaving the page."""
        ui.add_body_html('''
            <script>
                window.addEventListener("beforeunload", (event) => event.preventDefault());
            </script>
            ''')

    def _update_tab(self):
        if self.tab_panels.value == 'Run':
            self.run_tab.update()


if __name__ in {'__main__', '__mp_main__'}:
    Application()
