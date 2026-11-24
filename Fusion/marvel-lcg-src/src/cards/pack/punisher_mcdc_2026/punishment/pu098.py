from . import *

# * Rachel Cole-Alves (Punishment) — SBIRE UNIQUE. MARINE. VIGILANTE. SCH ★, ATQ 2, 5 PV, Boost 1.
# Punisher cannot attack this minion.
# ★ Forced Interrupt : When Rachel Cole-Alves would scheme, she attacks the TARGETED villain instead.
#
# Cartes de reference : `WhenUnitWouldScheme` + `SetBeInstead` (pu091b), `Enemy.AttackCharacter` (brique commune).
# ⚠ « she attacks the TARGETED villain » : le vilain sous-fifre ; l'attaque ne vise aucun joueur (les joueurs peuvent la
# defendre : pu090b). Garde de re-entree : non necessaire (une manigance remplacee par une ATTAQUE ne repasse pas par la
# manigance).

def GetAbilities() -> Sequence['Ability']:

    def au_lieu_de_comploter(effect: 'Effect', message: 'Message.WhenUnitWouldScheme') -> None:
        cible = VilainCible(effect)
        if cible is None:
            return
        message.SetBeInstead(effect)
        effect.this.CastTo(Enemy).AttackCharacter(cible, effect, players_may_defend=True)

    return [
        AbilityFactory.WhenUnitWouldScheme(AbilityType.ForcedInterrupt, "This", au_lieu_de_comploter),
    ]
