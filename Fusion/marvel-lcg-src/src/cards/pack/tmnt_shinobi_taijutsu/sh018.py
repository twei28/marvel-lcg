from . import *

# Countercross — EVENEMENT 1 [physical], Taijutsu (TMNT Shinobi, Inkwire). ATTACK. DEFENSE. THWART.
# Hero Interrupt (attack/defense/thwart): When you would take any amount of damage from an attack, prevent 1 of that
#   damage. Deal 1 damage to an enemy. Remove 1 threat from a scheme. Draw 1 card.
#
# Mots-cles : aucun (classe Taijutsu, fiche shinobi.md).
#
# Cartes de reference : `gam/18004` Crosscounter, MEME structure (« prevent N ... Deal 1 damage to an enemy. Remove 1
#   threat from a scheme », trois libelles `SetLabel('attack', 'defense', 'thwart')`, `SetTarget2(Enemy)`,
#   `SetTarget3(Scheme2)`) ; differences : « prevent 1 » au lieu de 3, « from an attack » (`is_from_attack=True`,
#   `donatello/td003`) et « Draw 1 card » (`05005` Wiggle Room : `DrawUp`).
#
# TEXTE CONTRE CODE
#  ⚠ « any amount of damage FROM AN ATTACK » -> `is_from_attack=True` (18004 n'avait pas ce filtre, son texte non plus).
#  ⚠ « prevent 1 OF THAT damage » : au plus 1. Les trois effets suivants sont SANS fleche : ils se resolvent toujours.
#  ⚠ « an enemy » / « a scheme » : deux choix au gre du joueur, sans lien avec l'attaquant.


def GetAbilities() -> Sequence['Ability']:

    def countercross(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)

        message.PreventDamage(1, effect)

        this.DealDamage(effect.targets2, 1, effect)
        this.RemoveThreatFromSchemes(effect.targets3, 1, effect)
        joueur = effect.GetInitiator()
        if joueur is not None:
            joueur.DrawUp(1, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            countercross,
            is_from_attack=True,
        ).SetPlay().SetLabel('attack', 'defense', 'thwart')
        .SetTarget2(Enemy)
        .SetTarget3(Scheme2),
    ]
