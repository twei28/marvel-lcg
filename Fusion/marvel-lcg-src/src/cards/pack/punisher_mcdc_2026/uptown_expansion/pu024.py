from . import *

# Harlem (U2) — LIEU Uptown (environnement LOCATION).
# Response: After an identity uses a basic power, ready an ally at this location. (Limit once per phase.)
#
# Cartes de reference : galactic_storm gs065 / pu078 (`AfterUnitUseBasicPower`), `Faces.ReadyAll`, pu034 / pu033 (`Ville.Occupe`, `JoueurDuPersonnage`).
# ⚠ Mots-pieges :
#  - « AN identity » : l'identite de n'importe quel joueur (les deux formes, REC d'un alter-ego compris : « a basic power »), pas seulement l'ecran de Harlem ;
#  - « ready an ally AT THIS LOCATION » : un allie d'un joueur present a Harlem (`JoueurDuPersonnage`), epuise ; choisi par le joueur qui a utilise le pouvoir ;
#    sans allie epuise a Harlem, rien (la limite n'est pas consommee a vide : la Reponse n'est pas offerte) ;
#  - « Limit once per PHASE » : globale.

def GetAbilities() -> Sequence['Ability']:

    def allies_epuises_ici(effect: 'Effect') -> 'List[CardFace]':
        return [f for f in Worlds.FindCardsOnField(effect, finder=CardFinder(card_type=Ally))
                if f.IsExhaust() and JoueurDuPersonnage(f) is not None and Ville.Occupe(effect, JoueurDuPersonnage(f), effect.this)]

    def une_cible(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> bool:
        return len(allies_epuises_ici(effect)) > 0

    def redresser(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        joueur = message.trigger.GetControlByPlayer()
        candidats = allies_epuises_ici(effect)
        if not candidats:
            return
        allie = candidats[0] if len(candidats) == 1 else joueur.AskChooseFace(candidats, effect)
        if allie is not None:
            Faces.ReadyAll([allie], effect)

    return [
        AbilityFactory.AfterUnitUseBasicPower(AbilityType.Response, Identity, redresser, conditions=[une_cible]).LimitOncePerPhase(),
    ]
