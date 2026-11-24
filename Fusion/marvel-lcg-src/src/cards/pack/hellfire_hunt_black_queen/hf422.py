from . import *

# Immortal Moon Goddess. Manigance annexe, menace 7, Hinder 2[per_hero], Victory 1 (desc, natifs), icone d'acceleration. « While Under the
# Moonlight is in play, Black Queen cannot be defeated. »
# Cartes de reference : gs115 Deathbird (`UnitCannotBeDefeatedWhile` + relance de la defaite quand la condition tombe), 35029 The Carbonadium
# Synthesizer. ⚠ La relance : la condition tombe (a) quand l'environnement se retourne sur le JOUR, (b) quand cette manigance quitte le jeu
# (ajoutee par la fabrique, `AfterCardLeavePlay`) : Selene a 0 PV ou moins est alors vaincue.


def GetAbilities() -> Sequence['Ability']:
    def relancer(effect: 'Effect', message: 'Message.AfterCardFlip') -> None:
        selene = Selene(effect)
        if selene is not None and selene.IsInPlay() and selene.health <= 0 and not EstLaNuit(effect):
            selene.Defeated(None, effect)

    return [
        *AbilityFactory.UnitCannotBeDefeatedWhile(AbilityType.NonKeyword, ChercheurSelene(), condition=lambda effect: EstLaNuit(effect)),
        Ability(AbilityType.NonKeyword, Message.AfterCardFlip,
                [lambda effect, message: Environment.IsType(message.to_face) and effect.this.IsInPlay()], relancer),
    ]
