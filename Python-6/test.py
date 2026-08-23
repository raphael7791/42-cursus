from abc import ABC, abstractmethod

class Instrument(ABC):
    def __init__(self, nom):
        self.nom = nom

    def decrire(self):
        return f"Instrument : {self.nom}"

    @abstractmethod
    def jouer(self):
        pass


class Guitare(Instrument):
    def __init__(self):
        super().__init__("Guitare")

    def jouer(self):
        return "La guitare gratte un accord"


class Piano(Instrument):
    def __init__(self):
        super().__init__("Piano")

    def jouer(self):
        return "Le piano joue une mélodie"


class InstrumentFactory(ABC):

    @abstractmethod
    def creer(self):
        pass

class GuitareFactory(InstrumentFactory):

    def creer(self):
        return Guitare()

class PianoFactory(InstrumentFactory):
        
    def creer(self):
        return Piano()

def tester(factory):
    instrument = factory.creer()
    print(instrument.decrire())
    print(instrument.jouer())


tester(GuitareFactory())
tester(PianoFactory())