from html.parser import HTMLParser


class HTMLStripper(HTMLParser):
    """
    Inspired by.
    https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
    """

    def __init__(self):
        super().__init__()

        self.strict = False
        self.convert_charrefs = True
        self.tag_data = []

        self.pause = 0

    def handle_data(self, d):
        if self.pause <= 0:
            self.tag_data.append(d)

    def handle_starttag(self, tag, attributes):

        # Do not record content of style tags
        if tag == 'style':
            self.pause += 1

    def handle_endtag(self, tag):

        # Do not record content of style tags
        if tag == 'style':
            self.pause -= 1

    def get_data(self):
        return ' '.join(self.tag_data)


def strip_tags(html):
    s = HTMLStripper()
    s.feed(html)
    return s.get_data()
