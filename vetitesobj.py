from datetime import datetime as DT


class Vetites(object):

    def __init__(self, film, library, date, guest, program, identifier=''):
        self.film = film
        self.library = library
        self.date = DT.strptime(date, '%Y.%m.%d. %H:%M:%S')
        self.guest = guest
        self.program = program
        self.uniq_identifier = identifier

    def set_identifier(self, identifier):
        self.uniq_identifier = identifier
       