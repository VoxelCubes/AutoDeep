import json
import os
from math import floor

import PySide6.QtCore as Qc
import PySide6.QtWidgets as Qw
from PySide6.QtCore import Slot, Signal
from pathlib import Path

import deepl_worker
from helpers import show_critical, show_warning, show_info
from src.ui_generated_files.ui_mainwindow import Ui_MainWindow
from driver_chromedriver_info import ChromedriverInfo

from text_file import TextFile

#TODO: fix crash upon starting a second file. Known issue.


class MainWindow(Qw.QMainWindow, Ui_MainWindow):
    """A window to show the books available"""

    process_next_file = Signal()

    def __init__(self):
        Qw.QMainWindow.__init__(self)
        self.setupUi(self)
        # Default values
        self.glossary_path = Path("")
        self.default_min_wait = 0
        self.default_char_wait = 0
        self.default_batch_time = 0
        self.default_max_chars = 0
        self.default_max_batches = 0
        # File handlers
        self.time_estimate = 0
        self.files = []
        self.current_file_index = 0

        self.thread = None
        self.worker = None
        # Worker timing
        self.total_time = 0
        self.total_batches = 0
        self.total_sessions = 0

        self.populate_language_selection()
        # Load default
        self.load_config(None)
        # Initialize GUI
        self.pushButton_start.setEnabled(False)
        self.pushButton_clear.setEnabled(False)
        self.pushButton_abort.hide()
        self.tableWidget.setColumnWidth(0, 300)
        self.tableWidget.setColumnWidth(1, 300)
        self.tableWidget.setFocusPolicy(Qc.Qt.NoFocus)
        self.label_deepl_copy_button.hide()
        # Connect Slots
        self.pushButton_reset_min_wait.clicked.connect(self.reset_min_wait)
        self.pushButton_reset_char_wait.clicked.connect(self.reset_char_wait)
        self.pushButton_reset_batch_time.clicked.connect(self.reset_batch_time)
        self.pushButton_reset_max_chars.clicked.connect(self.reset_max_chars)
        self.pushButton_reset_max_batches.clicked.connect(self.reset_max_batches)

        self.pushButton_get_glossary.clicked.connect(self.load_glossary)
        self.checkBox_use_glossary.stateChanged.connect(self.update_glossary_for_files)
        self.pushButton_save_file_glossary.clicked.connect(self.export_with_glossary)
        self.pushButton_cfg_save.clicked.connect(self.save_config)
        self.pushButton_cfg_load.clicked.connect(self.open_config_file)

        self.pushButton_new_file.clicked.connect(self.add_file)
        self.pushButton_start.clicked.connect(self.start_process)
        self.pushButton_clear.clicked.connect(self.clear_files)
        self.pushButton_abort.clicked.connect(self.abort_process)

        self.pushButton_refresh_estimate.clicked.connect(self.refresh_estimate)
        self.process_next_file.connect(self.process_next_file_action)


    def start_process(self):
        self.pushButton_start.setEnabled(False)
        self.pushButton_clear.hide()
        self.pushButton_abort.show()
        self.pushButton_refresh_estimate.hide()
        self.groupBox_cfg_lang.setEnabled(False)
        self.groupBox_cfg_time.setEnabled(False)
        self.groupBox_cfg_batches.setEnabled(False)
        self.pushButton_new_file.setEnabled(False)
        self.pushButton_cfg_save.setEnabled(False)
        self.pushButton_cfg_load.setEnabled(False)

        self.refresh_estimate()
        self.progressBar.setValue(0)
        self.current_file_index = -1
        self.statusbar.showMessage(f"Working...")
        self.process_next_file.emit()


    def abort_process(self):
        self.tableWidget.setCurrentText(2, "Aborting...")
        self.worker.abort_work()

    @Slot()
    def process_next_file_action(self):
        """
        Increment counter and start next file
        Using a slot to ensure other signals may be processed before starting next file
        """
        self.current_file_index += 1

        if self.current_file_index < len(self.files):
            self.tableWidget.setCurrentCell(self.current_file_index, 0)
            self.thread = Qc.QThread()
            self.worker = deepl_worker.Worker(self.files[self.current_file_index], self.read_config_from_widgets())
            self.worker.moveToThread(self.thread)
            # Connect signals and slots
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.finished.connect(self.worker_finished)
            self.worker.progress_message.connect(self.receive_worker_message)
            self.worker.progress.connect(self.receive_worker_progress)
            self.worker.chrome_driver_error.connect(self.receive_chrome_driver_error)

            self.worker.error.connect(self.thread.quit)
            self.worker.error.connect(self.worker.deleteLater)
            self.worker.error.connect(self.thread.deleteLater)
            self.worker.error.connect(self.receive_worker_error)
            # Start the thread
            self.thread.start()
        else:
            self.pushButton_clear.show()
            self.pushButton_abort.hide()
            self.pushButton_refresh_estimate.show()
            self.groupBox_cfg_lang.setEnabled(True)
            self.groupBox_cfg_time.setEnabled(True)
            self.groupBox_cfg_batches.setEnabled(True)
            self.pushButton_new_file.setEnabled(True)
            self.pushButton_cfg_save.setEnabled(True)
            self.pushButton_cfg_load.setEnabled(True)
            self.progressBar.setValue(100)
            self.statusbar.showMessage(f"Finished")
            self.label_time.setText("")
            self.current_file_index = -1


    def reenable_gui_after_abort(self):
        self.pushButton_clear.show()
        self.pushButton_abort.hide()
        self.pushButton_refresh_estimate.show()
        self.groupBox_cfg_lang.setEnabled(True)
        self.groupBox_cfg_time.setEnabled(True)
        self.pushButton_start.setEnabled(True)
        self.groupBox_cfg_batches.setEnabled(True)
        self.pushButton_new_file.setEnabled(True)
        self.pushButton_cfg_save.setEnabled(True)
        self.pushButton_cfg_load.setEnabled(True)
        self.statusbar.showMessage(f"Aborted")
        self.label_time.setText("")
        self.current_file_index = -1


    @Slot(str)
    def receive_worker_message(self, msg):
        self.tableWidget.setCurrentText(2, msg)


    @Slot(int, int)
    def receive_worker_progress(self, session, batch):
        """
        Add up the remaining time of the current workload, plus the total time for files still waiting.
        @param session: current file's progress
        @param batch: current file's progress
        """
        config = self.read_config_from_widgets()
        remaining_file_time = self.files[self.current_file_index].estimate_remaining_time(
            session,
            batch,
            config["deepl_min_wait_time_s"],
            config["deepl_wait_time_per_char_ms"],
            config["deepl_wait_between_batches_s"])
        if self.current_file_index < len(self.files)-1:
            for file in self.files[self.current_file_index+1:]:
                remaining_file_time += file.estimate_total_time(config["deepl_min_wait_time_s"],
                                                                config["deepl_wait_time_per_char_ms"],
                                                                config["deepl_wait_between_batches_s"])

        assert self.total_time > 0, "This should be impossible"
        progress = floor( (1 - (remaining_file_time / self.total_time)) * 100)
        self.progressBar.setValue(progress)
        if remaining_file_time > 60:
            self.label_time.setText(f"{round(remaining_file_time / 60)} minutes remaining")
        else:
            self.label_time.setText(f"{remaining_file_time} seconds remaining")


    @Slot(str)
    def worker_finished(self, fname):
        self.tableWidget.setCurrentText(1, fname[fname.rfind("/") + 1:])
        self.tableWidget.item(self.tableWidget.currentRow(), 1).setToolTip(fname)
        self.process_next_file.emit()


    @Slot(str)
    def receive_worker_error(self, errmsg):
        self.tableWidget.setCurrentText(2, errmsg)
        show_warning(self, "Error", errmsg)
        self.reenable_gui_after_abort()


    @Slot()
    def receive_chrome_driver_error(self):
        self.error_info = ChromedriverInfo()
        self.error_info.show()
        self.reenable_gui_after_abort()


    def populate_language_selection(self):
        # Populate the combobox
        supported_languages = {
            "English"   : "en",
            "French"    : "fr",
            "German"    : "de",
            "Spanish"   : "es",
            "Portuguese": "pt",
            "Italian"   : "it",
            "Dutch"     : "nl",
            "Polish"    : "pl",
            "Russian"   : "ru",
            "Japanese"  : "ja",
            "Chinese"   : "zh"
        }
        for lang in sorted(supported_languages.keys()):
            self.comboBox.addTextItemLinkedData(lang, supported_languages[lang])


    def add_file(self):
        config = self.read_config_from_widgets()
        file_path = Qw.QFileDialog.getOpenFileName(self, 'Open Text File', os.getcwd(), "Text files (*.txt)")[0]
        if os.path.isfile(file_path):
            try:
                new_file = TextFile(file_path, config)
            except EOFError:
                show_warning(self, "Error", "This file is empty.")
                return
            except OSError:
                show_warning(self, "Error", "Could not read file!")
                return
            # Prevent the user from setting a maximum char size lower than the minimum size in a file.
            self.spinBox_max_chars.setMinimum(max(self.spinBox_max_chars.minimum(), new_file.min_length))
            self.files.append(new_file)
            self.refresh_estimate()
            # Add file info to table
            self.tableWidget.appendRow(new_file.file_name, "", "Ready")
            self.statusbar.showMessage(f"Added file {new_file.file_path}")
            # Allow the user to start the process
            self.pushButton_start.setEnabled(True)
            self.pushButton_clear.setEnabled(True)
            self.pushButton_save_file_glossary.setEnabled(True)


    def clear_files(self):
        self.tableWidget.clearAll()
        self.time_estimate = 0
        self.files.clear()
        self.spinBox_max_chars.setMinimum(10)
        self.pushButton_start.setEnabled(False)
        self.pushButton_clear.setEnabled(False)
        self.pushButton_save_file_glossary.setEnabled(False)
        self.progressBar.reset()


    def refresh_estimate(self):
        self.total_time = 0
        self.total_batches = 0
        self.total_sessions = 0
        config = self.read_config_from_widgets()
        for file in self.files:
            file.build_meta_sessions(config["max_characters_per_batch"], config["max_batches_per_session"])
            self.total_time += file.estimate_total_time(config["deepl_min_wait_time_s"],
                                                   config["deepl_wait_time_per_char_ms"],
                                                   config["deepl_wait_between_batches_s"])
            self.total_sessions += file.session_count
            self.total_batches += file.batch_count

        if self.total_time > 60:
            self.label_time.setText(f"{round(self.total_time / 60)} minutes for {self.total_batches} batches in {self.total_sessions} sessions")
        else:
            self.label_time.setText(f"{self.total_time} seconds for {self.total_batches} batches in {self.total_sessions} sessions")


    ######################################### Glossary

    def load_glossary(self):
        file_path = Qw.QFileDialog.getOpenFileName(self, 'Open glossary', os.getcwd(), "Spreadsheet files (*.xlsx)")
        if os.path.isfile(file_path[0]):
            file_path = Path(file_path[0])
            self.label_glossary.setText(file_path.name)
            self.glossary_path = file_path
            self.checkBox_use_glossary.setChecked(True)

            self.statusbar.showMessage(f"Applying glossary to files")
            config = self.read_config_from_widgets()
            for file in self.files:
                file.apply_glossary(config)
            self.statusbar.showMessage(f"Loaded glossary {file_path.name}")
        else:
            self.statusbar.showMessage(f"No new glossary loaded.")


    @Slot(int)
    def update_glossary_for_files(self, state):
        if self.files:
            if state:
                self.statusbar.showMessage(f"Applying glossary to files")
            else:
                self.statusbar.showMessage(f"Removing glossary from files")

            config = self.read_config_from_widgets()
            for file in self.files:
                file.apply_glossary(config)
            self.statusbar.showMessage(f"Updated glossary")


    def export_with_glossary(self):
        for file in self.files:
            fname = file.file_path
            new_name = fname[:fname.rfind(".")] + "_glossary" + fname[fname.rfind("."):]
            save_path = Qw.QFileDialog.getSaveFileName(
                self, f'Save processed version of {file.file_name}', new_name, "text file (*.txt)")[0]
            if save_path:
                try:
                    with open(save_path, "w", encoding="utf-8") as out_file:
                        out_file.writelines(file.lines)
                    self.statusbar.showMessage(f"Saved modified version to {save_path}")
                except OSError:
                    self.statusbar.showMessage(f"Failed to save file to {save_path}")
                    show_critical(self, "Error", "Unable to save file.")
            else:
                self.statusbar.showMessage(f"Aborted saving file")


    ######################################### Config

    def load_config(self, path=None):
        """
        Populates the options, using the default config if none is given.
        @param path: path to a config.json
        """
        loading_default = False
        default_path = Path(os.getcwd()) / "default_config.json"

        if path is None:
            loading_default = True  # set flag
            path = default_path

        config = {}
        try:
            with open(path) as config_file:
                config = json.load(config_file)
                self.statusbar.showMessage(f"Loading configuration {path}")
        except (OSError, ValueError):
            show_warning(self, "WARNING", "Config not found. Restoring defaults.")
            config = {
                "translate_to"                : "en",
                "glossary"                    : "",
                "use_glossary"                : False,
                "close_banners"               : True,
                "max_characters_per_batch"    : 4990,
                "max_batches_per_session"     : 20,
                "deepl_wait_time_per_char_ms" : 4,
                "deepl_min_wait_time_s"       : 7,
                "deepl_wait_between_batches_s": 3,
                "deepl_copy_button"           : "div.lmt__target_toolbar__copy_container button"
            }
            try:
                with open(default_path, 'w', encoding="utf-8") as outfile:
                    json.dump(config, outfile, indent=4, ensure_ascii=False)
            except OSError:
                show_critical(self, "ERROR", "Could not restore configuration!")

        # Set the values in the input fields
        self.comboBox.setCurrentIndexByLinkedData(config["translate_to"])
        self.doubleSpinBox_min_wait.setValue(config["deepl_min_wait_time_s"])
        self.doubleSpinBox_char_wait.setValue(config["deepl_wait_time_per_char_ms"])
        self.doubleSpinBox_batch_time.setValue(config["deepl_wait_between_batches_s"])
        self.spinBox_max_chars.setValue(config["max_characters_per_batch"])
        self.spinBox_max_batches.setValue(config["max_batches_per_session"])
        self.label_deepl_copy_button.setText(config["deepl_copy_button"])
        if config["glossary"]:
            self.glossary_path = Path(config["glossary"])
            self.label_glossary.setText(self.glossary_path.name)
        self.checkBox_use_glossary.setChecked(config["use_glossary"])
        self.checkBox_banners.setChecked(config["close_banners"])

        # Remember values if this was the default config
        if loading_default:
            self.default_min_wait = config["deepl_min_wait_time_s"]
            self.default_char_wait = config["deepl_wait_time_per_char_ms"]
            self.default_batch_time = config["deepl_wait_between_batches_s"]
            self.default_max_chars = config["max_characters_per_batch"]
            self.default_max_batches = config["max_batches_per_session"]


    def read_config_from_widgets(self):
        return {"use_glossary"                : self.checkBox_use_glossary.isChecked(),
                "close_banners"               : self.checkBox_banners.isChecked(),
                "glossary"                    : str(self.glossary_path),
                "translate_to"                : self.comboBox.currentLinkedData(),
                "deepl_min_wait_time_s"       : self.doubleSpinBox_min_wait.value(),
                "deepl_wait_time_per_char_ms" : self.doubleSpinBox_char_wait.value(),
                "deepl_wait_between_batches_s": self.doubleSpinBox_batch_time.value(),
                "max_characters_per_batch"    : self.spinBox_max_chars.value(),
                "max_batches_per_session"     : self.spinBox_max_batches.value(),
                "deepl_copy_button"           : self.label_deepl_copy_button.text()
                }


    def save_config(self):
        save_path = Qw.QFileDialog.getSaveFileName(self, 'Save configuration', os.getcwd(), "JSON (*.json)")
        save_path = save_path[0]
        if save_path:
            try:
                with open(save_path, "w", encoding="utf-8") as cfg_file:
                    json.dump(self.read_config_from_widgets(), cfg_file, indent=2, ensure_ascii=False)
                self.statusbar.showMessage(f"Saved configuration to {save_path}")
            except OSError:
                self.statusbar.showMessage(f"Failed to save configuration to {save_path}")
                show_critical(self, "Error", "Unable to save config.")
        else:
            self.statusbar.showMessage(f"Aborted saving configuration")


    def open_config_file(self):
        file_path = Qw.QFileDialog.getOpenFileName(self, 'Open configuration', os.getcwd(), "JSON (*.json)")
        file_path = file_path[0]
        if os.path.isfile(file_path):
            self.load_config(file_path)


    def reset_min_wait(self):
        self.doubleSpinBox_min_wait.setValue(self.default_min_wait)


    def reset_char_wait(self):
        self.doubleSpinBox_char_wait.setValue(self.default_char_wait)


    def reset_batch_time(self):
        self.doubleSpinBox_batch_time.setValue(self.default_batch_time)


    def reset_max_chars(self):
        self.spinBox_max_chars.setValue(self.default_max_chars)


    def reset_max_batches(self):
        self.spinBox_max_batches.setValue(self.default_max_batches)
