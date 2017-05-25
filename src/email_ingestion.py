import glob
from os.path import isfile
from time import time

from parsers import SimpleEmailParser
from tokenizers import SimpleTextTokenizer


class EmailIngester:

    def __init__(self, tokenize=True):
        self.parser = SimpleEmailParser()
        self.tokenizer = SimpleTextTokenizer()

        self.tokenize = tokenize

    @staticmethod
    def list_emails(root_path):
        """Recursively search for all files in root path."""
        email_paths = [
            f for f in glob.glob(root_path + '**/*', recursive=True)
            if isfile(f)
        ]
        return email_paths

    def ingest_folder(self, root_path, max_files=None):

        start_time = time()
        email_paths = self.list_emails(root_path)

        emails = []

        if max_files is not None:
            email_paths = email_paths[:int(max_files)]

        # Candidate for parallel processing.
        for email_path in email_paths:

            try:
                emails.append(self.process_email(email_path))

            # TODO Remove except and improve parser.
            except (ValueError, TypeError) as e:
                continue

        # TODO tomdr 25/05/2017: add proper logging
        print("Processed %d / %d emails (%.3fs)." % (
            len(emails), len(email_paths), time() - start_time))

        return emails

    def process_email(self, email_path):
        email = self.parser.parse(email_path)
        email['url'] = email_path

        if self.tokenize:
            subject = email.pop('subject')
            body = email.pop('body')
            email['tokens'] = self.tokenizer.tokenize(subject + ' ' + body)

        return email

