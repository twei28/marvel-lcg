from . import *

# Time Out — obligation. Boost 2 (`desc`). GiveTo: Alligator Loki.
# Give to the Alligator Loki player. Search the set-aside area for Frogjolnir
#   and shuffle it into the encounter deck.
# You get -2 ATK while in hero form.
# Alter-Ego Action: Exhaust your alter-ego → remove Time Out from the game.
#
# Cartes de reference :
#  - 32055 Permanently Phased : `WhenThisObligationGiveToYou` pour ce qui se
#    passe A LA REMISE, et `PlayerActionToRemoveThisFromGame(AlterEgoAction)`
#    pour la sortie ;
#  - aa017 Funeral : le malus continu par `GiveKeywordToInPlayWhenApplyThis(
#    ..., control_by="You", ...)`, l'obligation vivant dans la zone du joueur
#    a qui elle a ete remise ;
#  - 56023 In Too Deep : `CostFunc.Exhaust("YourIdentity")` pour « exhaust
#    your alter-ego → » (une Alter-Ego Action ne se joue qu'en alter-ego,
#    l'identite inclinee EST donc l'alter-ego) ;
#  - ab016 : `Faces.ShuffleAllTo([...], "EncounterDeck", effect)`.
#
# ⚠ « -2 ATK WHILE IN HERO FORM » -> cible `Hero`, pas `Identity` : l'ATK
# n'existe qu'en forme heros, et le mot-cle ne s'applique qu'a la face heros.
# Retour en alter-ego : la face heros n'est plus en jeu, le malus dort.
# ⚠ « Search the set-aside area for Frogjolnir » -> al022, par `card_ids`,
# `include_set_aside=True` (search.py:199). Si Frogjolnir n'y est plus (deja
# melange par une premiere remise, ou en jeu), rien ne se passe.
# ⚠ « Remove from the game » (pas « discard ») : l'obligation ne revient
# jamais, contrairement a Funeral.
# ⚠ EMPLACEMENT DU MODULE : `set_name` de la carte = « Alligator Loki » (elle
# vient par la liste `obligations` du deck de depart, pas par le set nemesis),
# et `CardsDB.FindAbilities` (database.py:193) cherche le module dans le
# dossier du set : `alligator_loki/al017.py`, PAS `alligator_loki_nemesis/`.
# Rangee d'abord chez les nemesis : la carte entrait en jeu nue, sans aucune
# capacite (constate au harnais le 01/09/2026). aa017 Funeral, elle, vit chez
# les nemesis parce que son `set_name` est « Agatha Harkness Nemesis ».

def GetAbilities() -> Sequence['Ability']:

    def time_out(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(this)
        joueur = message.GetGaveToPlayer()
        if joueur is None:
            return
        frogjolnir = Search.SearchForCard(
            effect,
            joueur,
            include_set_aside=True,
            card_ids=["al022"],
        )
        if frogjolnir is not None:
            Faces.ShuffleAllTo([frogjolnir], "EncounterDeck", effect)

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            time_out,
        ),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Hero,
            control_by="You",
            attack=-2,
        ),
        AbilityFactory.PlayerActionToRemoveThisFromGame(
            AbilityType.AlterEgoAction,
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]
