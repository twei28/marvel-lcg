from . import *

# Shootout — TRAITRISE. Boost 1 + ★.
# When Revealed : Deal 1 damage to the villain and each character in this turf. In expert mode, exhaust a character you control.
# ★ Boost : Deal 1 damage to each character you control.
#
# Cartes de reference : pu102 (`DealDamage` au vilain et aux sbires), pu104 (`AuChoixDuJoueur` : « a character you control » au choix du joueur),
# `Worlds.GetOnFieldAllies/GetOnFieldMinions/GetPlayersIdentities(zone)`, `Worlds.IsExpert`.
# ⚠ « each character IN THIS TURF » : les identites des joueurs de la zone, leurs allies et les sbires de la zone (pas ceux des autres rangees) ;
# « the villain » : le CAPO de la zone, blesse a part (un vilain et des sbires dans UNE liste ne se blessent pas ensemble, REPRISE) ;
# « each character YOU CONTROL » (Boost) : mon identite et mes allies.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        zone = joueur.GetIdentity().card.GetGameArea()
        vilain = LeVilain(effect, joueur)
        if vilain is not None:
            this.DealDamage([vilain], 1, effect)
        personnages = list(Worlds.GetPlayersIdentities(zone)) + list(Worlds.GetOnFieldAllies(zone)) + list(Worlds.GetOnFieldMinions(zone))
        if personnages:
            this.DealDamage(personnages, 1, effect)
        if Worlds.IsExpert(effect):
            AuChoixDuJoueur(effect, joueur, lambda cibles: Faces.ExhaustAll(cibles, effect), canbe_exhaust=True)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        if joueur is not None:
            effect.this.DealDamage(list(joueur.GetControlCharacters()), 1, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
