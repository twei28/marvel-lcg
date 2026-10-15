from . import *

# * Angar the Screamer — SBIRE (New Revengers). REVENGER. PV 4, MNG 1, ATQ 2 (etoile), 1 boost.
# [star] Angar the Screamer's attacks gain ranged.
# Forced Interrupt: When Angar the Screamer attacks you, also resolve his attack against each other hero.
#
# Cartes de reference :
#  - Ranged : **`41002b`** Psi-Katana / `sk070` (meme coffret) : `UnitAttackGainKeyword("This", ranged=True)`.
#  - Interruption forcee : **`core 01130`** * Whirlwind : meme texte mot pour mot (`WhenUnitAttackYou` +
#    `message.AlsoResolveThisAttackTo(Worlds.GetOnFieldHeroes(effect))`, ruling FFG : une attaque separee
#    par heros, resolues ensemble).
#
# ⚠ Mots-pieges : « his ATTACKS gain ranged » : TOUTES ses attaques (aussi celles contre les autres heros) ;
# « each OTHER hero » : le heros deja attaque n'est pas double (`AlsoResolveThisAttackTo` ignore les cibles
# deja presentes) ; un joueur en alter ego n'est pas un heros ; l'etoile du badge ATQ renvoie au texte
# (convention validee, aucune valeur a ajouter).


def GetAbilities() -> Sequence['Ability']:

    def hurlement(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.AlsoResolveThisAttackTo(Worlds.GetOnFieldHeroes(effect))

    return [
        AbilityFactory.UnitAttackGainKeyword("This", ranged=True),
        AbilityFactory.WhenUnitAttackYou(AbilityType.ForcedInterrupt, "This", hurlement),
    ]
