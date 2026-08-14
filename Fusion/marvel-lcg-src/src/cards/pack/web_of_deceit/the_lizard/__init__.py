from cards.pack.web_of_deceit import *

# Le scenario tourne autour de DEUX compteurs, declares dans `CardFace.COUNTER` :
#
#   * « formula » vit sur The Lizard et donne +1 ATK a chaque ennemi REPTILIAN ;
#   * « sanity » vit sur Lizard Brain. Vaincre The Lizard le retourne en Curt
#     Connors et charge le cerveau ; chaque action de Connors en retire un, et
#     le dernier retire rend The Lizard.
#
# Les points de vie sont portes par la CARTE, pas par la face (leçon du lot 1) :
# les deux faces declarent donc les memes PV, et le retournement passe par
# `ResetHealth` de part et d'autre pour qu'aucune ne naisse deja vaincue.


def LizardBrain(effect: 'Effect') -> 'Environment|None':
    return Worlds.FindCardOnField(effect, name="Lizard Brain", card_type=Environment)


def CompteursDeSante(effect: 'Effect') -> int:
    cerveau = LizardBrain(effect)
    return cerveau.CastTo(CanPlaceCounter).GetCounters('sanity') if cerveau else 0


def RetirerUnCompteurDeSante(effect: 'Effect') -> None:
    cerveau = LizardBrain(effect)
    if cerveau and cerveau.CastTo(CanPlaceCounter).GetCounters('sanity') > 0:
        Faces.RemoveCountersOn([cerveau], 1, 'sanity', effect)
