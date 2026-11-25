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
  def __init__(self,joueurs):
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
  
  def lancer(self):
    if self._joueur_actif.a_2_des():
      a,b=randint(1,6),randint(1,6)
      if a==b and self._joueur_actif.relance_si_double():
        return a+b,True
      else:
        return a+b,False
    else:
      return randint(1,6),False

  def resolution_lancer(self):
    n,relance=self.lancer()

    #resolution cartes rouges
    for joueur in self.autres_joueurs:
      for etab in joueur.etablissements:
        if etab.couleur=="Rouge" and n in numeros: 
    pass
    
  
  
  
  

from abc import ABC, abstractmethod
class Carte(ABC):
  _COULEURS = {'Violet','Rouge','Bleu','Vert'}
  _CATEGORIE = {'rouage','blé','cochon','usine','cafe','tdt','pain','fruit'}
  def __init__(self,nom,cout):
    self._nom=nom
    self._cout=cout
  
  @property
  def nom(self):
    return self._nom
  @property
  def cout(self):
    return self._cout 



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
  def activer(self, proprio, joueur_actif=None):
    pass

#du coup la j'ai commencé a faires les sous classes dont je parlais redites moi si vous trouvez ça nul c'est ok
#et j'ai pas fini les cartes violettes psq jpense il manque une classe partie ou un truc qui réunit tout les joueurs qui jouent

class Etab_gain(etablissement):
  def __init__(self,nom,cout,categorie,couleur,numeros,montant):
    super().__init__(nom,cout,categorie,couleur,numeros)
    self._montant=montant
  
  def activer(self, proprio, joueur_actif=None):
    bonus=0
    if proprio.gain_augmente():
      bonus=1
    proprio.recevoir(self._montant+bonus)

class Etab_gain_par_cat(etablissement):
  def __init__(self,nom,cout,categorie,couleur,numeros,montant,categorie_cible):
    super().__init__(nom,cout,categorie,couleur,numeros)
    self._montant=montant
    self._categorie_cible=categorie_cible
  
  def activer(self, proprio, joueur_actif=None):
    for etab in proprio.etablissements:
      if etab.categorie == self._categorie_cible:
        proprio.recevoir(self._montant)

class Etab_perte_lanceur(etablissement):
  def __init__(self,nom,cout,categorie,couleur,numeros,montant):
    super().__init__(nom,cout,categorie,couleur,numeros)
    self._montant=montant
  
  def activer(self, proprio,joueur_actif=None):
    bonus=0
    if joueur_actif.gain_augmente():
      bonus=1
    paye = joueur_actif.payer(self._montant+bonus)
    proprio.recevoir(paye)

class Stade(etablissement):
    def __init__(self):
        super().__init__("Stade",6,[6],"Violet","tdt")

    pass

class CentreAffaires(etablissement):
  pass

class ChaineTele(etablissement):
  pass# -*- coding: utf-8 -*-




#carte verte
class Superette(Etab_gain):
  def __init__(self):
    super().__init__('Superette',2,'pain','vert',[4],1)

class Boulangerie(Etab_gain):
  def __init__(self):
    super().__init__('Boulangerie',1,'pain','vert',[2,3],3,)

class Fromagerie(Etab_gain_par_cat):
  def __init__(self):
    super().__init__('Fromagerie',5,'usine','vert',[7],3,'cochon')
    
class Fabrique_de_meubles(Etab_gain_par_cat):
  def __init__(self):
    super().__init__('Fabrique_de_meubles',3,'usine','vert',[8],3,'rouage')
    
class Marche_de_fruit_et_legumes(Etab_gain_par_cat):
  def __init__(self):
    super().__init__('Marche_de_fruit_et_legumes',2,'fruit','vert',[11,12],2,'ble')
        

"""
Created on Mon Nov  9 10:28:56 2026

@author: louis
"""

