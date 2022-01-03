class Vetites(object):

    def __init__(self, film, library, date, guest, program, identifier=''):
        self.film = film
        self.library = library
        self.date = date
        self.guest = guest
        self.program = program
        self.uniq_identifier = identifier

    def set_identifier(self, identifier):
        self.uniq_identifier = identifier
       