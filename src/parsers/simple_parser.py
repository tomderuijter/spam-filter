import re
from email.parser import Parser

from dateutil.parser import parse as parse_date

from .base import BaseEmailParser
from .html_stripper import strip_tags


class SimpleEmailParser(BaseEmailParser):

    def __init__(self):
        self.parser = Parser()

    def parse(self, file_path):

        file_pointer = open(
            file_path, 'r', encoding='utf-8', errors='ignore'
        )

        email = self.parser.parse(file_pointer)

        # Mandatory fields
        document = {
            'sender': email['From'],
            'recipients': self.parse_recipients(email),
            'date': self.parse_date(email),
            'charset': email.get_charsets()[0],
            'subject': email['Subject'],
            'body': self.parse_body(email.get_payload())
        }

        # TODO tomdr 24/05/2017:
        # Check for Reply-To and Return-Path fields
        # Check for Received fields

        return document

    @staticmethod
    def parse_recipients(email):
        if 'To' in email:
            s = email['To']
        elif 'Delivered-To' in email:
            s = email['Delivered-To']
        else:
            s = ''

        regex = re.compile('[,; \n\t]+')
        recipients = regex.split(s)
        return recipients

    @staticmethod
    def parse_date(email):
        if 'Date' in email:
            s = email['Date']
        else:
            s = email['Sent']

        return parse_date(s)

    @staticmethod
    def parse_body(text):

        # Check for multipart messages
        if isinstance(text, list):
            return SimpleEmailParser.parse_body(
                text[0].get_payload()  # Shortcut: check mimetype in future.
            )
        else:
            text = strip_html(text)
            return text


def strip_html(text):
    if _contains_html(text):
        text = strip_tags(text)  # Relatively expensive
    return text


def _contains_html(text):
    return '</' in text
