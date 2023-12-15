import pandas as pd

class Escala:

  def __init__(self, vacancias, pessoas, desejos):
    self.vacancias = vacancias
    self.pessoas = pessoas
    self.desejos = {pessoas[i]: {turno: 0 for turno in desejos[i].split(' ')} for i in range(len(pessoas))}
    self.escala = {pessoa : {} for pessoa in pessoas}

  def gerarEscala(self):
    pessoas = self.pessoas
    while len(pessoas) > 0:
      desejos = self.desejos
      for pessoa in pessoas:
        for desejo in desejos[pessoa].copy(): 
          if desejo in self.vacancias:
            if self.escala[pessoa]:
              if not self.conflito(self.escala[pessoa], desejo, pessoa):
                self.vacancias.remove(desejo)
                self.escala[pessoa][desejo] = desejos[pessoa].pop(desejo)
                break
            else:
              self.vacancias.remove(desejo)
              self.escala[pessoa][desejo] = desejos[pessoa].pop(desejo)
              break
          desejos[pessoa].pop(desejo)
        if len(desejos[pessoa]) == 0:
          final = sorted(self.escala[pessoa].keys(), key=lambda x: (int(x[:-1]), x[-1]))
          count = len(final)
          plural_suffix = 'ões' if count != 1 else 'ão'
          final = f'{" ".join(final)} ({count} plant{plural_suffix})'
          self.escala[pessoa] = final
          pessoas.remove(pessoa)

  def conflito(self, escala, novoPlantao, pessoa):
    if len(escala) == 10:
      return True
    return self.seguidos(escala, novoPlantao, pessoa)

  def seguidos(self, escala, novoPlantao, pessoa):
    novoDia, novoTurno = int(novoPlantao[:-1]), novoPlantao[-1]
    seguido = []
    for plantao in escala:
      dia, turno = int(plantao[:-1]), plantao[-1]
      if (dia == novoDia and turno != novoTurno) or \
         (dia == novoDia + 1 and turno == 'D' and novoTurno == 'N') or \
         (dia == novoDia - 1 and turno == 'N' and novoTurno == 'D'):
        if escala[plantao] == 1:
          return True
        seguido.append(plantao)
        if len(seguido) == 2:
          return True
    self.desejos[pessoa][novoPlantao] = len(seguido)
    if seguido:
      escala[seguido[0]] = 1
    return False
    
  def mostrarEscala(self):
    print('Escala:')
    for pessoa in self.escala:
      print(f"{pessoa}: {self.escala[pessoa]}")
    v = len(self.vacancias)
    print(f"Vacância{'s' if v != 1 else ''}: {' '.join(self.vacancias)} ({v} plant{'ões' if v != 1 else 'ão'})" if v else "Não houve vacâncias")
    
prioridade = "Guilherme Vital Heltron Ribeiro Ramon Gleide Moisés Amanda_G Luiza Kariny Délio Amanda_A".split(" ")
desejos = {}
desejos[0] = "2D 9D 23D 30D 4D 11D 18D 4N 11N 18N 2N 9N 23N 30N 5D 26D 12N 19N 26N 8D 8N 15D 22D 29D 29N 20N 27N 7D 14D 28D 7N 14N 21N 28N 6D 6N 25D 25N 16D 16N" #Guilerme
desejos[1] = "8N 9D 18N 22N 23N 24N 25N 29N 19D 19N 20D 20N 21N 22D 24D 25D 26D 28N 29D 9N 16N 26N 30N" #Vital
desejos[2] = "10N 17N 24N 8N 9N 22N 29N 16N 23N 30N 11N 12N 18N 19N 25N 26N 13N 20N 27N 13D 20D 27D" #Heltron
desejos[3] = "1N 2N 4N 7D 7N 8N 11N 12N 13N 14D 17N 18N 19N 20N 22N 24N 25N 26N 27N 28D" #Ribeiro
desejos[4] = "2D 9D 16D 23D 30D 4D 6D 13D 20D 27D 7D 14D 21D 28D" #Ramon
desejos[5] = "14N 13N 13D 12N 14D 12D 21N 20D 21D 20N 19N 19D 11N 18N" #Gleide
desejos[6] = "8D 22D 29D 31D 10N 17N 7N 14N 21N 26N 28N 14D 21D 28D 8N 22N 29N 13N 20N 27N 20D 27D 1N" #Moisés
desejos[7] = "9D 16D 23D 30D 29D 8D" #Amanda G
desejos[8] = "5D 7N 8D 9D 10D" #Luiza
desejos[9] = "17N 12D 26D 14N 18D 3D 10D 24D 31D 20N 6N" #Kariny
desejos[10] = "4D 11D 4N 11N 3N 10N 12N 6D" #Délio
desejos[11] = "9D 23D 9N 23N 16D 10D 17D 24D 31D 19D 10N 17N 24N 31N 14N 21N 28N" #Amanda V

spreadsheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTEYffAo-dy94auNHe4OjgUpyg9MvTc20iUCqjv68l61umYUHbBoqgAfFOf6uN9SGogvImLz-YE3_h1/pub?gid=0&single=true&output=csv"
df = pd.read_csv(spreadsheet_url)
vacancias = [f'{column}{value}' for column in df.columns for value in df[column].tolist() if value == 'N' or value == 'D']

escala = Escala(vacancias, prioridade, desejos)
escala.gerarEscala()
escala.mostrarEscala()