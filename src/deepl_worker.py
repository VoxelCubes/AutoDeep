import os
import PySide6.QtCore as Qc
from PySide6.QtCore import Signal, Slot

import deepL_selenium
import helpers as hp



class Worker(Qc.QObject):
    finished = Signal(str)
    progress = Signal(int, int)  # session, batch
    progress_message = Signal(str)
    error = Signal(str)
    chrome_driver_error = Signal()
    deepl = None
    halted = False


    def __init__(self, file, config):
        Qc.QObject.__init__(self)
        self.file = file
        self.language = config["translate_to"]
        self.close_banners = config["close_banners"]
        self.min_wait = config["deepl_min_wait_time_s"]
        self.char_time = config["deepl_wait_time_per_char_ms"]
        self.batch_time = config["deepl_wait_between_batches_s"]
        self.max_chars = config["max_characters_per_batch"]
        self.max_batches = config["max_batches_per_session"]


    @Slot(int, int, str)
    def forward_webdriver_msg(self, session, batch, msg):
        if not self.halted:
            self.progress_message.emit(msg)
            self.progress.emit(session, batch)


    def abort_work(self):
        # TODO: to halt the worker more quickly, break up the translation loop to let a slot get called in between.
        if self.deepl is not None:
            self.deepl.abort_driver()
        self.halted = True


    def run(self):
        ################################# Divide corpus
        self.progress_message.emit(f"Splitting into batches.")
        in_sessions = hp.prepare_batch_corpus(self.file.lines, self.max_chars, self.max_batches)

        ################################# DeepL
        has_error = False
        out_text = []
        fname = self.file.file_path
        out_filename = fname[:fname.rfind(".")] + "_" + self.language + fname[fname.rfind("."):]

        for session_index, session_corpus in enumerate(in_sessions):

            if self.halted:
                break

            self.progress_message.emit(f"Opening chrome driver.")
            if False and not os.path.isfile(".\\chromedriver.exe"):
                # self.error.emit("No chromedriver found!")
                self.chrome_driver_error.emit()
                self.halted = True
                break

            try:
                self.deepl = deepL_selenium.SeleniumDeepL(driver_path=".\\chromedriver")
            except Exception as e:
                # Catch missing chrome driver
                # self.error.emit("Chromedriver likely outdated or missing!")
                self.chrome_driver_error.emit()
                self.halted = True
                print(e)
                break

            self.deepl.progress_report.connect(self.forward_webdriver_msg)  # Listen for progress
            try:
                self.deepl.run_translation(corpus_batch=session_corpus,
                                           destination_language=self.language,
                                           time_to_translate_min=self.min_wait,
                                           time_to_translate_char=self.char_time,
                                           time_batch_rest=self.batch_time,
                                           session_index=session_index,
                                           close_banners=self.close_banners,
                                           total_sessions=len(in_sessions))
            except Exception as e:
                if not self.halted:
                    out_filename = fname[:fname.rfind(".")] + "_" + self.language + "_DUMP" + fname[fname.rfind("."):]
                    self.progress_message.emit("Error: aborting session.")
                    self.error.emit(f"ERROR occurred! Session aborted!\n\n{e}")
                    has_error = True
                break
            finally:
                if self.halted:
                    break
                out_text.append(self.deepl.get_translated_corpus())

        ################################# Write output
        if not self.halted:
            try:
                with open(out_filename, "w", encoding="utf-8") as outfile:
                    outfile.writelines(out_text)
            except OSError:
                self.error.emit("ERROR: Writing the file has failed!")

            if not has_error:
                self.progress_message.emit("Finished")
                self.finished.emit(out_filename)
        else:
            if self.deepl is not None:
                self.deepl.close_driver()
            self.progress_message.emit("Aborted")
