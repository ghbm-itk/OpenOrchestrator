"""This module is responsible for the layout and functionality of the run tab
in Scheduler."""

from datetime import datetime

from nicegui import ui


from OpenOrchestrator.database import db_util
from OpenOrchestrator.scheduler import runner


class RunTab:
    """The run tab object for Scheduler."""
    def __init__(self, tab_name: str) -> None:
        self.running = False
        self.running_jobs = []

        with ui.tab_panel(tab_name):
            with ui.row():
                self.button = ui.button("Run", on_click=self.button_click).classes("w-48")
                ui.spinner("gears", size='lg').bind_visibility_from(self, 'running')
            ui.label("Log").classes("text-xl")
            self.log_area = ui.log(max_lines=1000).classes("w-full h-96")

    def button_click(self):
        """Handler for when the run/pause button is clicked."""
        if self.running:
            self.pause()
        else:
            self.run()

    def run(self):
        """Start Scheduler."""
        if db_util.get_conn_string() is None:
            ui.notify("Not connected", type='warning')
            return

        self.log_area.push("Running...")
        self.running = True
        self.button.text = "Pause"

        ui.timer(0.1, self.loop, once=True)

    def pause(self):
        """Pause Scheduler."""
        self.log_area.push("Paused... Please wait for all processes to stop before closing the application")
        self.running = False
        self.button.text = "Run"

    def loop(self):
        """The main loop function of the Scheduler.
        Checks heartbeats, check triggers, and schedules the next loop.
        """
        self.log_area.push(datetime.now())

        self.check_heartbeats()

        if self.running:
            self.check_triggers()

        if len(self.running_jobs) == 0:
            self.log_area.push("Doing cleanup...")
            runner.clear_repo_folder()

        # Schedule next loop
        if self.running or len(self.running_jobs) > 0:
            self.log_area.push('Waiting 10 seconds...\n')
            ui.timer(10, self.loop, once=True)
        else:
            self.log_area.push("Scheduler is paused and no more processes are running.")

    def check_heartbeats(self) -> None:
        """Check if any running jobs are still running, failed or done."""
        self.log_area.push('Checking heartbeats...')
        for job in self.running_jobs:
            if job.process.poll() is not None:
                self.running_jobs.remove(job)

                if job.process.returncode == 0:
                    self.log_area.push(f"Process '{job.trigger.process_name}' is done")
                    runner.end_job(job)
                else:
                    self.log_area.push(f"Process '{job.trigger.process_name}' failed")
                    runner.fail_job(job)

            else:
                self.log_area.push(f"Process '{job.trigger.process_name}' is still running")

    def check_triggers(self) -> None:
        """Checks any process is blocking
        and if not checks if any trigger should be run.
        """
        # Check if process is blocking
        blocking = False
        for job in self.running_jobs:
            if job.trigger.is_blocking:
                self.log_area.push(f"Process '{job.trigger.process_name}' is blocking\n")
                blocking = True

        # Check triggers
        if not blocking:
            self.log_area.push('Checking triggers...')
            job = runner.poll_triggers(self)

            if job is not None:
                self.running_jobs.append(job)
