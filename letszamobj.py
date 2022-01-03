from vetitesobj import Vetites


class Letszam(Vetites):

    def __init__(self, event, identifier, children, adult, granny):
        super(Letszam, self).__init__(*event)
        self.uniq_identifier = identifier
        self.children = children
        self.adult = adult
        self.granny = granny
