from . import *

# Imperial Formation — TRAITRISE (Imperial Guard). Aucune icone de boost.
# When Revealed: Resolve the "When Revealed" ability of each IMPERIAL GUARD minion in play. If you cannot, search the
#   encounter deck and discard pile for an IMPERIAL GUARD minion and reveal it.
#
# Cartes de reference :
#  - « Resolve the When Revealed ability of each ... » : `Faces.ResolveAbility(sbires, joueur, AbilityType.WhenRevealed,
#    effect)`, modeles sm 27083 / sk046.
#  - « search the encounter deck and discard pile for a minion and reveal it » : `Search.EncounterCard(include_discard_pile=True,
#    ..)` + `Reveal`, modele fne 60185 Police Cordon.
#
# ⚠ Mots-pieges : « EACH IMPERIAL GUARD minion IN PLAY » (tous, Hobgoblin compris : il copie alors le When Revealed d'un autre) ; « If you
# CANNOT » = aucun sbire IMPERIAL GUARD en jeu ; la recherche vise un SBIRE IMPERIAL GUARD (pas la traitrise) ; « YOU » = le joueur qui revele.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        sbires = SbiresImperialGuard(effect)
        if sbires:
            Faces.ResolveAbility(sbires, joueur, AbilityType.WhenRevealed, effect)
            return
        face = Search.EncounterCard(effect, include_discard_pile=True, trait=IG, card_type=Minion)
        if face:
            face.Reveal(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
