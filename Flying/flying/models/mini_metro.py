class Station:
    def __init__(self, nom: str, frequentation: int):
        self.nom = nom
        self.frequentation = frequentation

class Ligne:
    def __init__(self, station_a: str, station_b: str, nom_ligne: str):
        self.station_a = station_a
        self.station_b = station_b
        self.nom_ligne = nom_ligne

class Metro:
    def __init__(self):
        self.stations: dict[str, Station] = {}
        self.lignes: list[Ligne] = []
    
    def add_station(self, station: Station):
        self.stations[station.nom] = station


    def add_ligne(self, ligne: Ligne):
        self.lignes.append(ligne)
    
    def voisins(self, nom_station: str):
        result = []
        for l in self.lignes:
            if nom_station == l.station_a:
                result.append(l.station_b)
            elif nom_station == l.station_b:
                result.append(l.station_a)
        return result
    

if __name__ == "__main__":

    graph = Metro()

    with open("flying/models/mini_metro.txt", "r") as f:
        for line in f:

            line = line.strip()
            
            if line.startswith("station:"):

                parties = line.split(":")[1].strip().split()

                nom_station = parties[0]
                frequentation = int(parties[1])

                graph.add_station(Station(nom_station, frequentation))
            
            elif line.startswith("ligne:"):

                parties = line.split(":")[1].strip().split()
                noms = parties[0].split("-") 
                nom_station1 = noms[0]
                nom_station2 = noms[1]
                num_ligne = parties[1]

                graph.add_ligne(Ligne(nom_station1, nom_station2, num_ligne))

    print("Stations:")                                                                                                            
    for s in graph.stations.values():                                                                                               
        print(f"  {s.nom} ({s.frequentation} voyageurs/jour)")                                                                      
                                                                                                                                      
    print("Lignes:")                                                                                                              
    for l in graph.lignes:                                                                                                          
        print(f"  {l.station_a} <-> {l.station_b} ({l.nom_ligne})")                                                                 

    print("Voisins de Chatelet:")
    for v in graph.voisins("Chatelet"):
        print(f"  {v}")
    



