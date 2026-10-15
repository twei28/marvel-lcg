from . import *

# Revelation — TRAITRISE x3 (Secret Invasion). ★ + 1 boost.
# When Revealed: Flip the CAMOUFLAGED ally with the most remaining hit points. If you cannot, put a REVEALED minion at random
#   from the IMPOSTOR deck into play engaged with you.
# ★ Boost: Flip 1 CAMOUFLAGED ally you control, after this activation ends.
#
# Cartes de reference : `Filter.One(..., most_remaining_hp=True)` (**`sk098`**) ; helpers `RetournerAllie`, `MettreSbireRevele` (set) ;
# Boost « after this activation ends » : **`sk107`** (`RunAt.AfterEnemyActivationEnd`) ; « a character you control » :
# `AuChoixDuJoueur` (**`paibok`**, `YouControlUnit`).
#
# ⚠ Mots-pieges : « the CAMOUFLAGED ally with the MOST REMAINING hit points » : de tous les joueurs, PV RESTANTS (pas imprimes), le
# joueur departage une egalite ; « If you cannot » = aucun allie CAMOUFLAGED en jeu ; Boost : « 1 CAMOUFLAGED ally YOU CONTROL » (le
# joueur choisit parmi les siens), APRES l'activation.


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        allie = AllieAvecLePlusDePv(effect, AlliesCamoufles(effect))
        if allie is not None:
            RetournerAllie(effect, allie)
        else:
            MettreSbireRevele(effect, joueur)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()

        def apres() -> None:
            siens = [a for a in AlliesCamoufles(effect) if a.GetControlByPlayer() == joueur]
            if not siens:
                return
            choisi = Filter.One(list(siens), effect)
            if choisi is not None:
                RetournerAllie(effect, choisi)

        RunAt.AfterEnemyActivationEnd(effect, message.would_message, apres)

    return [
        AbilityFactory.WhenThisRevealed(None, revelation),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
