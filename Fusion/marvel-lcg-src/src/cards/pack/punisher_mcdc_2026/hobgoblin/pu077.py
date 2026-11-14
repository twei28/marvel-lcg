from . import *

# * The Enforcers — SBIRE UNIQUE. CRIMINAL. MERCENARY. SCH 1★, ATQ 3★, 6 PV, Boost 2.
# ★ Forced Response : After The Enforcers activate against you, discard 3 cards from the encounter deck. Take 1
#   indirect damage for each treachery discarded this way.
#
# Cartes de reference : rainy/thor_jane_foster_nemesis/ra028.py (`AfterEnemyActivationEnd(ForcedResponse, "This")`),
# `Worlds.DiscardEncounterCards`, `TakeIndirectDamage` sur l'identite.
#
# ⚠ « activate AGAINST YOU » : le joueur contre qui il s'est active (attaque OU manigance) ; « 1 indirect damage FOR
# EACH treachery » : un seul bloc de degats indirects de N points, ou N blocs de 1 : ici N points d'un coup (le
# joueur repartit), N = nombre de traitrises ; aucune traitrise = rien. SCH/ATQ « ★ » : desc `1**` / `3**` (lus tels
# quels).

def GetAbilities() -> Sequence['Ability']:

    def apres(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        this = effect.this.CastTo(Minion)
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        cartes = Worlds.DiscardEncounterCards(3, effect)
        n = len([c for c in cartes if Treachery.IsType(c)])
        if n > 0:
            joueur.GetIdentity().TakeIndirectDamage(this, n, effect)

    return [
        AbilityFactory.AfterEnemyActivationEnd(AbilityType.ForcedResponse, "This", apres),
    ]
