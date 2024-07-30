#!/usr/bin/env python3
import sys
import subprocess
import os
import time
import logging
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, pyqtSlot
from PyQt6.QtQml import QQmlApplicationEngine

logging.basicConfig(level=logging.DEBUG)

class DisplayOffApp(QObject):
    def __init__(self):
        super().__init__()
        self.power_management_cookie = None
        self.screen_saver_cookie = None

    @pyqtSlot(int, str, bool)
    def turn_off_display(self, delay, session_type, block_sleep):
        logging.debug("Turn Off Display button clicked")
        try:
            if delay > 0:
                logging.debug(f"Sleeping for {delay} seconds")
                time.sleep(delay)

            if session_type == 'Wayland':
                logging.debug("Turning off display for Wayland")
                subprocess.run(['kscreen-doctor', '--dpms=off'])
            else:
                logging.debug("Turning off display for X11")
                subprocess.run(['xset', 'dpms', 'force', 'off'])

            if block_sleep:
                self.block_sleep_and_screen_locking(True)
            else:
                self.block_sleep_and_screen_locking(False)

        except Exception as e:
            logging.error(f"Error in turn_off_display: {e}")

    def block_sleep_and_screen_locking(self, block):
        if os.path.exists('/etc/os-release'):
            with open('/etc/os-release', 'r') as f:
                for line in f:
                    if line.startswith('ID='):
                        os_id = line.split('=')[1].strip().strip('"')
                        break

            if os_id == 'arch':
                dbus_command = 'qdbus6'
            else:
                dbus_command = 'qdbus'

            try:
                if block:
                    # Inhibit power management
                    self.power_management_cookie = subprocess.run([
                        dbus_command, 'org.freedesktop.PowerManagement', '/org/freedesktop/PowerManagement', 'Inhibit', 'DisplayOffApp', 'Blocking sleep'
                    ], capture_output=True, text=True).stdout.strip()

                    # Inhibit screen locking
                    self.screen_saver_cookie = subprocess.run([
                        dbus_command, 'org.freedesktop.ScreenSaver', '/ScreenSaver', 'Inhibit', 'DisplayOffApp', 'Blocking screen locking'
                    ], capture_output=True, text=True).stdout.strip()
                else:
                    # Uninhibit power management
                    if self.power_management_cookie:
                        subprocess.run([
                            dbus_command, 'org.freedesktop.PowerManagement', '/org/freedesktop/PowerManagement', 'UnInhibit', self.power_management_cookie
                        ])

                    # Uninhibit screen locking
                    if self.screen_saver_cookie:
                        subprocess.run([
                            dbus_command, 'org.freedesktop.ScreenSaver', '/ScreenSaver', 'UnInhibit', self.screen_saver_cookie
                        ])
            except Exception as e:
                logging.error(f"Error in block_sleep_and_screen_locking: {e}")

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        engine = QQmlApplicationEngine()

        display_off_app = DisplayOffApp()
        engine.rootContext().setContextProperty("displayOffApp", display_off_app)

        engine.load(os.path.join(os.path.dirname(__file__), "Ds-claudemods.qml"))

        if not engine.rootObjects():
            sys.exit(-1)

        sys.exit(app.exec())
    except Exception as e:
        logging.error(f"Error in main: {e}")
