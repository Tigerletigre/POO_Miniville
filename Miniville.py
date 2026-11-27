# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 13:11:23 2026

@author: louis
"""

from abc import ABC, abstractmethod
from random import randint

#Fonction utiles pour plusieurs classes
def demander_oui_non(question):
  reponse = input(question + "y/n").strip().lower()
  while reponse not in ["y","n"]:
    reponse = input("reponds par oui avec y ou non avec n : " + question + "y/n").strip().lower()
  return reponse == "y"

class Carte(ABC):
  _COULEURS = {'Violet','Rouge','Bleu','Vert'}
  _CATEGORIE = {'rouage','ble','cochon','usine','cafe','tdt','pain','fruit'}
  def __init__(self,nom,cout):
    self._nom=nom
    self._cout=cout

  @property
  def nom(self):
    return self._nom
  @property
  def cout(self):
    return self._cout

class monument(Carte):
  def __init__(self,nom,cout):
    super().__init__()


  @property
  def categorie(self):
    return self._categorie

class etablissement(Carte):
  def __init__(self,nom,cout,categorie,couleur,numeros):
    super().__init__()
    self._categorie=categorie
    self._couleur=couleur
    self._numeros=numeros

  @property
  def categorie(self):
    return self._categorie
  @property
  def couleur(self):
    return self._couleur
  @property
  def numeros(self):
    return self._numeros

  def peut_activer(self, proprio, lanceur):
        match self._couleur:
            case "Bleu":
              return True
            case "Vert":
              return proprio==lanceur
            case "Violet":
              return proprio==lanceur
            case "Rouge":
              return proprio!=lanceur
  def achetable(self,proprio):
    if self._couleur == "Violet":
      return not self._nom in proprio.etablissements
    else:
      return True
  @abstractmethod
  def activer(self,proprio,joueur_actif,joueurs):
    pass

#du coup la j'ai commencé a faires les sous classes dont je parlais redites moi si vous trouvez ça nul c'est ok
#et j'ai pas fini les cartes violettes psq jpense il manque une classe partie ou un truc qui réunit tout les joueurs qui jouent

class Etab_gain(etablissement):
  def __init__(self,nom,cout,categorie,couleur,numeros,montant):
    super().__init__(nom,cout,categorie,couleur,numeros)
    self._montant=montant

  def activer(self, proprio, joueur_actif,joueurs):
    bonus=0
    if proprio.gain_augmente() and self._categorie in ["pain","cafe"]:
      bonus=1
    proprio.recevoir(self._montant+bonus)

class Etab_gain_par_cat(etablissement):
  def __init__(self,nom,cout,categorie,couleur,numeros,montant,categorie_cible):
    super().__init__(nom,cout,categorie,couleur,numeros)
    self._montant=montant
    self._categorie_cible=categorie_cible

  def activer(self, proprio, joueur_actif,joueurs):
    for etab in proprio.etablissements:
      if etab.categorie == self._categorie_cible:
        proprio.recevoir(self._montant)

class Etab_perte_lanceur(etablissement):
  def __init__(self,nom,cout,categorie,couleur,numeros,montant):
    super().__init__(nom,cout,categorie,couleur,numeros)
    self._montant=montant

  def activer(self,proprio,joueur_actif,joueurs):
    bonus=0
    if joueur_actif.gain_augmente() and self._categorie in ["pain","cafe"]:
      bonus=1
    paye=joueur_actif.payer(self._montant+bonus)
    proprio.recevoir(paye)

class Stade(etablissement):
  def __init__(self,nom,cout,categorie,couleur,numeros,montant):
    super().__init__("Stade",6,[6],"Violet","tdt")
  def activer(self, proprio,joueur_actif,joueurs):
    for joueur in joueurs:
      paye=joueur.payer(self._montant)
      proprio.recevoir(paye)

class CentreAffaires(etablissement):
  def __init__(self,nom,cout,categorie,couleur,numeros,montant):
    super().__init__("Centre des affaires",6,[6],"Violet","tdt")


class ChaineTele(etablissement):
  def __init__(self,nom,cout,categorie,couleur,numeros,montant):
    super().__init__("Chaine de télé",6,[6],"Violet","tdt")
  def activer(self, proprio, joueur_actif,joueurs):
    while joueur in joueurs:
      joueur=input("A quel joueur voulez vous prendre de l'argent")
    paye=joueur.payer(self._montant)
    proprio.recevoir(paye)

#je sais pas ce que vous en penser il reste a ajouter toutes les cartes dans le
#plateau et de changer la fonction acheter dans la classe joueur
class plateau:
  _cartes_possible={'Superette','Boulangerie'}
  def __init__(self):
    self._liste_cartes={"Superette": [Etab_gain('Superette', 2, 'pain', 'vert', [4], 1) for _ in range(6)],
                        "Boulangerie": [Etab_gain('Boulangerie',1,'pain','vert',[2,3],3,) for _ in range(6)]}

  def ecriture_carte(self,nom):
    return 0 if nom in plateau._cartes_possible else 1

  def quantite_carte(self,nom):
    return 0 if nom in self._liste_cartes else 1

  def retirer_carte_plateau(self,nom):
    self._liste_cartes[nom].pop()

Superette=Etab_gain('Superette',2,'pain','vert',[4],1)
dicoetab={Superette:0,}

class joueur:
  def __init__(self,nom):
    self._nom=nom
    self._etablissements=[]
    self._argent=3
    self._monuments=[]
  @property
  def nom(self):
    return self._nom
  @property
  def etablissements(self):
    return self._etablissements

  def recevoir(self,n): #n est arbitraire
    self._argent+=n

  def payer(self,n):    #si on a pas assez d'argent on donne ce qu'il nous reste
      paye = min(n,self._argent)
      self._argent -= paye
      return paye

  def acheter(self):
    pass

  def ajouter_etablissement(self,etablissement):
    self._etablissements.append(etablissement)
  def retirer_etablissement(self,etablissement):
    self._etablissements.remove(etablissement)
  def possede_etablissement(self,etablissement):
    return etablissement in self._etablissements

  def a_gagne(self)->bool:
      return len(self._monuments)==4

  def a_2_des(self)->bool:
      return "Gare" in self._monuments

  def peut_relancer(self)->bool:
      return "Tour radio" in self._monuments

  def relance_si_double(self)->bool:
      return "Parc d'atractions" in self._monuments

  def gain_augmente(self)->bool:
      return "Centre commercial" in self._monuments

  def ajouter_monument(self,monument):
    self._monuments.append(monument)

from random import randint
class partie:
  def __init__(self,joueurs:list[joueur]):
    self._joueurs=joueurs
    self._tour=0
    self._joueur_actif=joueurs[0]
  @property
  def joueurs(self):
    return self._joueurs
  @property
  def tour(self):
    return self._tour
  @property
  def joueur_actif(self):
    return self._joueur_actif

  def autres_joueurs(self):
    return [joueur for joueur in self._joueurs if joueur!=self._joueur_actif]

  def gagnant(self):
    for joueur in self._joueurs:
      if joueur.a_gagne():
        return joueur
    return None

  def lancer(self)->tuple[int,bool]:
    nb_des = 1
    #Première conditions pour la gare
    if self._joueur_actif.a_2_des() and demander_oui_non("Voulez vous lancer les 2 dés ?"):
      nb_des = 2
    des = [randint(1,6) for i in range(nb_des)]
    print(f"{self._joueur_actif.nom} a obtenu {sum(des)}")

    #Deuxième conditions pour la Tour radio
    if self._joueur_actif.peut_relancer() and demander_oui_non("Voulez vous relancer ?"):
      des = [randint(1,6) for i in range(nb_des)]
      print(f"{self._joueur_actif.nom} a obtenu {sum(des)}")

    #Troisème conditions pour le parc d'attraction
    double = nb_des == 2 and des[0] == des[1] and self._joueur_actif.relance_si_double()
    #double est un booleen
    return sum(des),double

  
  def resolution_lancer(self):
    n,relance=self.lancer()
    #boucle anti horraire
    for joueur in range(self._joueurs.index()-1,self._joueurs.index()-len(self._joueurs-1),-1):
      for etab in joueur.etablissements:
        if etab.couleur=="Rouge" and n in etab.numeros:
          etab.activer(joueur,self._joueur_actif)
    for joueur in self._joueurs:
      for etab in joueur.etablissements:
        if etab.peut_activer(self._joueur_actif,joueur) and n in etab.numeros:
          etab.activer(joueur,self._joueur_actif)

