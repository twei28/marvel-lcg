from . import *

# Satchel Charge (1B) — ENVIRONNEMENT.
# This card's effects cannot be canceled.
# When Revealed : Deal 2[per hero] damage to the villain. The players as a group take 3[per hero] indirect damage.
#   Shuffle Punisher and each ARMAMENT card in play and in the encounter discard pile into the encounter deck. Flip this
#   card.
#
# Cartes de reference : `DealDamage` (pu059), `TakeIndirectDamage(..., as_group=True)` (can_health.py), `Faces.ShuffleAllTo`
# (jigsaw/pu065 pour la defausse), `this.card.Flip(effect)`.
# ⚠ « as a GROUP » : un seul bloc de 3[per hero] degats indirects reparti entre tous les personnages des joueurs ;
# « shuffle Punisher AND each ARMAMENT in play AND in the discard pile » : les armes attachees quittent le jeu ;
# « effects cannot be canceled » : natif impossible a annuler dans ce script (aucune annulation prevue par le moteur
# pour un When Revealed d'environnement).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        n = len(list(Worlds.GetPlayers(effect)))
        vilains = Worlds.GetVillains(effect)
        if vilains:
            this.DealDamage(vilains[:1], 2 * n, effect)
        joueur = message.GetToPlayer() or Worlds.GetFirstPlayer(effect)
        joueur.GetIdentity().TakeIndirectDamage(this, 3 * n, effect, as_group=True)
        a_melanger = [c for c in Worlds.FindCardsOnField(effect, trait="ARMAMENT")]
        punisher = Worlds.FindCardOnField(effect, name="Punisher", card_type=Minion)
        if punisher is not None:
            a_melanger.append(punisher)
        a_melanger += [c for c in Worlds.GetEncounterDiscardPileCards(effect) if c.HasTrait("ARMAMENT") or c.paper.name.strip("* ") == "Punisher"]
        if a_melanger:
            Faces.ShuffleAllTo(a_melanger, Worlds.GetEncounterDeck(effect), effect)
        this.card.Flip(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
