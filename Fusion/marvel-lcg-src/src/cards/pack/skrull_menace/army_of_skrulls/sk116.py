from . import *

# Skrull Assault — TRAITRISE (Army of Skrulls). ★.
# When Revealed: Each SKRULL minion attacks the hero it is engaged with. If no
#   attacks were made this way, this card gains surge.
# ★ Boost: This card gets +1 boost icon for each SKRULL enemy in play (to a
#   maximum of +4) for this activation.
#
# Cartes de reference : `Worlds.Enemies.AllMinionAttackTheHeroItEngagedWith(
# effect, trait=..., if_no_attack=...)` (operate/enemies.py) ; `46028`.
# ⚠ « attacks the HERO » : un joueur en alter ego n'est pas attaque (natif du
# helper) ; « ENEMY » pour le boost, plafond +4.


def GetAbilities() -> Sequence['Ability']:

    def assaut(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        Worlds.Enemies.AllMinionAttackTheHeroItEngagedWith(
            effect, trait="SKRULL", if_no_attack=lambda: ThisCardGainSurge(effect))

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        n = min(4, len(EnnemisSkrullEnJeu(effect)))
        if n:
            message.GainBoostIcon(n, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, assaut),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
