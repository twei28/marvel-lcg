from . import *

# * Echo (Maya Lopez) — custom « DesignHacker »
# [star] Echo gets THW and ATK equal to your active hero's THW and ATK.
#   If you are in alter-ego form, Echo cannot attack or thwart.
# THW/ATK imprimés à 0 dans cards.json, remontés dynamiquement (montage
# Madame Web 69001a) ; en alter-ego, le bonus vaut 0 et les interdictions
# d'attaquer/contrer prennent le relais.


def GetAbilities() -> Sequence['Ability']:

    def heros_actif(effect: 'Effect') -> 'CardFace|None':
        controleur = effect.this.GetControlByPlayer()
        if controleur is None:
            return None
        identite = controleur.GetIdentity()
        if identite is None or not Hero.IsType(identite):
            return None
        return identite

    def valeur_atk(effect: 'Effect', ui: List['CardFace']) -> int:
        heros = heros_actif(effect)
        if heros is None:
            return 0
        ui.append(heros)
        return heros.attack

    def valeur_thw(effect: 'Effect', ui: List['CardFace']) -> int:
        heros = heros_actif(effect)
        if heros is None:
            return 0
        ui.append(heros)
        return heros.thwart

    def en_alter_ego(effect: 'Effect', message: 'Message2') -> bool:
        controleur = effect.this.GetControlByPlayer()
        return controleur is not None and controleur.IsAlterEgo()

    return [
        AbilityFactory.ThisGainKeyword(
            valeur_atk,
            attack=1,
            change_on_event=OnEvent.CardInPlay(CardFinder(card_type=Hero)),
        ),
        AbilityFactory.ThisGainKeyword(
            valeur_thw,
            thwart=1,
            change_on_event=OnEvent.CardInPlay(CardFinder(card_type=Hero)),
        ),
        *AbilityFactory.UnitCannotAttackTarget(
            "This",
            cannot_attack=True,
            conditions=[en_alter_ego],
        ),
        *AbilityFactory.UnitCannotThwartTarget(
            "This",
            cannot_thwart=True,
            conditions=[en_alter_ego],
        ),
    ]
