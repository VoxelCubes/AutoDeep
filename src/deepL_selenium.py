import PySide6.QtCore as Qc
import clipboard
from PySide6.QtCore import Signal

from default_selenium import SeleniumDefault



class SeleniumDeepL(SeleniumDefault, Qc.QObject):
    """
    Using Selenium to translate text using deepl.com
    """
    progress_report = Signal(int, int, str)
    halted = False


    def __init__(self, destination_language="en", **kwargs):
        """
        In addition the SeleniumDefault object, we can select the translation language.
        @param driver_path: str - path to the selenium driver (mandatory)
        @param destination_language: str
        """
        SeleniumDefault.__init__(self, **kwargs)
        Qc.QObject.__init__(self)

        self.sleep(2)

        self.translations = []

        self.url_template = "https://www.deepl.com/<lang>/translator"
        self.destination_language = destination_language

        self.set_url()
        self.load_url()


    def set_url(self):
        """
        Transforms the self.url_template into self.url depending on selected self.destination_language
        """
        self.url = self.url_template.replace('<lang>', self.destination_language)


    def add_source_text(self, batch):
        """
        Place the text to be translated into the textbox on www.deepl.com
        @param batch: str - text to be translated
        """
        clipboard.copy(batch)
        input_css = "div.lmt__inner_textarea_container textarea"
        input_area = self.driver.find_element_by_css_selector(input_css)

        input_area.clear()
        self.sleep(1)
        self.paste_clipboard(input_area)


    def get_translation_copy_button(self):
        """
        When text is translated, we get it back by clicking on the "Copy to clipboard" button.
        This function gets that button.
        """
        button_css = "div.lmt__target_toolbar__copy button"
        button = self.driver.find_element_by_css_selector(button_css)
        return button


    def get_cookie_button(self):
        """
        Remove the cookie banner to prevent it from interfering.
        """
        button_css = "button.dl_cookieBanner--buttonClose"
        button = self.driver.find_element_by_css_selector(button_css)
        return button


    def get_cookie_button_gdpr(self):
        """
        Remove the cookie banner to prevent it from interfering.
        """
        button_css = "button.dl_cookieBanner--buttonSelected"
        button = self.driver.find_element_by_css_selector(button_css)
        return button


    def get_cookie_button_cta(self):
        """
        Remove the cookie banner to prevent it from interfering.
        """
        button_css = "button.dl_cookieBanner--cta-buttonClose"
        button = self.driver.find_element_by_css_selector(button_css)
        return button


    def get_translation(self, sleep_before_click_to_clipboard=2):
        """
        Click on the get to clipboard button of deepL and then return the results.
        As page might be long depending on text size, we scroll to the button so that we can click on it.
        """
        button = self.get_translation_copy_button()
        self.scroll_to_element(button, sleep_before_click_to_clipboard)
        button.click()
        self.scroll_to_element(button, 1)
        # Click a second time to fool bot detection
        button.click()
        self.sleep(1)
        content = clipboard.paste()
        return content


    def run_translation(self, corpus_batch, destination_language,
                        time_to_translate_min, time_to_translate_char,
                        time_batch_rest, session_index, total_sessions, close_banners):
        """
        Primary function
        @param corpus_batch: list
        @param destination_language: str
        @param time_to_translate_min
        @param time_to_translate_char
        @param time_batch_rest: time to wait at the end of an iteration before starting a new one.
        @param session_index: int
        @param total_sessions: int
        NO OUTPUT. Results are stored in self.translations, accessible through self.get_translated_corpus()
        """
        self.translations.clear()
        # Check data to translate
        if len(corpus_batch) == 0:
            self.add_source_text("No data to translate. Closing window.")
            self.sleep(1)
            return

        # Check destination language
        if destination_language != self.destination_language:
            self.destination_language = destination_language
            self.set_url()
            self.load_url()

        if close_banners:
            # Get rid of banner. Attempt to remove the gdpr banner, then the simple banner.
            # Carry on if both fail.
            try:
                button = self.get_cookie_button_gdpr()
                button.click()
            except:
                pass

            try:
                button = self.get_cookie_button()
                button.click()
            except:
                pass

            try:
                button = self.get_cookie_button_cta()
                button.click()
            except:
                pass

            self.sleep(1)

        # Do translation
        try:
            for idx_batch, batch in enumerate(corpus_batch):

                if self.halted:
                    return

                self.progress_report.emit(session_index, idx_batch,
                                          f"Session ({session_index + 1}/{total_sessions}) Batch ({idx_batch + 1}/{len(corpus_batch)})")
                self.add_source_text(batch)
                # Subtract 7 from the min time because these 7 seconds account for other sleep times spread throughout this process.
                # Min wait (s) time with additional wait time (ms) per character in the batch
                wait_time = round(len(batch) * time_to_translate_char * 0.001) + (time_to_translate_min - 7.00)
                self.sleep(wait_time)

                for line in self.get_translation().split("\n"):
                    self.translations.append(line)

                # Remove deepL tag
                if "www.DeepL.com/Translator" in self.translations[-1]:
                    self.translations.pop()
                    self.translations.pop()

                self.sleep(time_batch_rest)

        # Dealing with error if one occurring during translation process
        except:
            # noinspection SpellCheckingInspection
            self.translations.insert(0, "vvvvv ERROR OCCURRED DURING TRANSLATION vvvvv\n")
            self.translations.insert(0, "||||| --------------------------------- |||||\n")
            self.close_driver()
            self.translations.append("\n^^^^^ ERROR OCCURRED DURING TRANSLATION ^^^^^\n")
            self.translations.append("||||| --------------------------------- |||||\n")
            raise

        # Close the driver session
        self.close_driver()


    def abort_driver(self):
        self.halted = True


    def get_translated_corpus(self):
        return "".join(self.translations)
