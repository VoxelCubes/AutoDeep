import pandas as pd

import superQuickReplacer as spqr
from pathlib import Path



class TextFile:
    file_path = None
    file_name = ""
    lines_raw = []
    lines = []
    sessions = []
    meta_sessions = []
    line_lengths = []
    min_length = 0
    session_count = 0
    batch_count = 0
    char_count = 0


    def __init__(self, path, config):
        with open(path, "r", encoding="utf-8") as f:
            self.lines_raw = f.readlines()
        if not self.lines_raw:
            raise EOFError

        self.file_path = path
        self.file_name = path[path.rfind("/") + 1:]
        self.apply_glossary(config)


    def apply_glossary(self, config):
        if config["use_glossary"] and Path(config["glossary"]).is_file():
            # OSError caught during creation
            workbook = pd.read_excel(config["glossary"], sheet_name=None)
            self.lines = spqr.super_quick_replace(workbook, self.lines_raw)
        else:
            self.lines = self.lines_raw
        # Precompute meta data
        self.line_lengths = [len(line) for line in self.lines]
        self.min_length = max(self.line_lengths)
        self.char_count = sum(self.line_lengths)


    def build_meta_sessions(self, max_characters, max_batch_size):
        """
        Split line_length into batches that represent the final batching.
        This is used to calculate the processing time more efficiently,
        without having to recalculate the length of each line.
        Only stores the length of each batch.
        @param max_characters: int
        @param max_batch_size: int
        @return: list of list of ints
        """
        # Batch information (reset these values after each batch finalization)
        batches = []
        batch_length = 0

        # Going through each sentence of the initial corpus to create the batches
        for line_len in self.line_lengths:
            # Checking the batch size before adding a new line
            if batch_length + line_len < max_characters:
                batch_length += line_len
            else:
                # Store complete batch as a string and reset
                batches.append(batch_length)
                batch_length = line_len

        if batch_length > 0:
            # Append leftovers
            batches.append(batch_length)

        # Split the corpus into chunks up to the max batch size
        self.meta_sessions = [batches[i * max_batch_size:(i + 1) * max_batch_size]
                              for i in range((len(batches) + max_batch_size - 1) // max_batch_size)]
        self.session_count = len(self.meta_sessions)
        self.batch_count = len(batches)


    def estimate_total_time(self, min_time, char_time, wait_time):
        # Adding 5 to session count as an estimate for how long it takes to start the web driver
        # char_time converted to milli seconds
        print(self.batch_count, self.session_count, self.char_count, min_time, char_time, wait_time)
        return round((self.char_count * 0.001 * char_time) + (self.session_count * 5) + (self.batch_count * (min_time + wait_time)))


    def estimate_remaining_time(self, session_index, batch_index, min_time, char_time, wait_time):
        session_count = 0
        batch_count = 0
        char_count = 0
        assert session_index < len(self.meta_sessions)
        assert batch_index < len(self.meta_sessions[session_index])
        for session in self.meta_sessions[session_index:]:
            session_count += 1
            for batch in session[batch_index:]:
                batch_count += 1
                char_count += batch
            # On first session, use the batch_index, then ignore
            batch_index = 0

        print(batch_count, session_count, char_count, min_time, char_time, wait_time)
        return round((char_count * 0.001 * char_time) + ((session_count - 1) * 5) + (batch_count * (min_time + wait_time)))
