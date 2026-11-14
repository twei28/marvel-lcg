from . import *

# Condemned Soul Portal — ENVIRONNEMENT. Boost 2 (natif).
# When Revealed : Discard a non-ELITE minion in play. Otherwise, this card gains surge.
# Forced Response : After a printed non-ELITE MYSTIC minion is defeated, shuffle that minion into the encounter deck.
# Hero Action : If there are no MYSTIC minions in play, spend 2 resources of any type -> discard this card.
#
# Cartes de reference : sk175b (`HeroAction` + `.SetCost(Cost("2"))`), `Faces.ShuffleAllTo(.., "EncounterDeck", ..)`, `ThisCardGainSurge`, `AfterUnitBeDefeated`.
# ⚠ Mots-pieges : « a non-ELITE minion IN PLAY » (n'importe quel sbire non elite, MYSTIC ou non ; le joueur qui revele choisit) ; « Otherwise » = aucun sbire non elite : surge ;
# « PRINTED non-ELITE MYSTIC » : les traits IMPRIMES (un trait gagne ne compte pas) ; la Forced Response vaut pour tout sbire vaincu, quel que soit celui qui le bat ;
# Hero Action : seulement en forme heros, condition « aucun sbire MYSTIC en jeu » verifiee avant de payer.


def GetAbilities() -> Sequence['Ability']:
    def non_elite(face: 'CardFace') -> bool:
        return "ELITE" not in (getattr(face.paper, "traits", None) or [])

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        candidats = [m for m in Worlds.GetOnFieldMinions(effect) if non_elite(m)]
        if not candidats:
            ThisCardGainSurge(effect)
            return
        choisi = joueur.AskChooseFace(candidats, effect) if len(candidats) > 1 else candidats[0]
        if choisi is None:
            ThisCardGainSurge(effect)
            return
        Faces.DiscardAll([choisi], effect)

    def mystique_non_elite(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> bool:
        m = message.trigger
        traits = getattr(m.paper, "traits", None) or []
        return "MYSTIC" in traits and "ELITE" not in traits

    def remelange(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        Faces.ShuffleAllTo([message.trigger], "EncounterDeck", effect)

    def aucun_mystique(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        return not SbiresMystiquesEnJeu(effect)

    def defausse(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Faces.DiscardAll([effect.this], effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.AfterUnitBeDefeated(AbilityType.ForcedResponse, CardFinder(card_type=Minion), remelange, conditions=[mystique_non_elite]),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, defausse, conditions=[aucun_mystique]).SetCost(Cost("2")),
    ]
