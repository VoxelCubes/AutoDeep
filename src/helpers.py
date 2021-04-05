import PySide6.QtWidgets as Qw



def show_critical(parent, title, msg):
    return Qw.QMessageBox.critical(parent, title, msg, Qw.QMessageBox.Yes, Qw.QMessageBox.Abort)



def show_warning(parent, title, msg):
    Qw.QMessageBox.warning(parent, title, msg, Qw.QMessageBox.Ok)



def show_info(parent, title, msg):
    Qw.QMessageBox.information(parent, title, msg, Qw.QMessageBox.Ok)



def prepare_batch_corpus(corpus, max_characters, max_batch_size):
    """
    Given a corpus of sentences, aggregate them by batch in order to make less request on DeepL website.
    Split batches up to a maximum size to limit the requests per session.
    @param corpus: list of str
    @param max_characters: int
    @param max_batch_size: int
    @return: list of list of strings
    """

    # Batch information (reset these values after each batch finalization)
    batch = []
    batch_corpus = []
    batch_length = 0

    # Going through each sentence of the initial corpus to create the batches
    for line in corpus:
        # Check line size
        line_len = len(line)
        assert (line_len <= max_characters)

        # Checking the batch size before adding a new sentence in it
        if batch_length + line_len < max_characters:
            batch.append(line)
            batch_length += line_len
        else:
            # Store complete batch as a string and reset
            batch_corpus.append("".join(batch))
            batch = [line]
            batch_length = line_len

    if batch:
        # Append leftovers
        batch_corpus.append("".join(batch))

    # Split the corpus into chunks up to the max batch size
    return [batch_corpus[i * max_batch_size:(i + 1) * max_batch_size]
            for i in range((len(batch_corpus) + max_batch_size - 1) // max_batch_size)]
