from . import *

# * Thunder Dojo — SOUTIEN 1 [energy], aspect Basic (Iron Fist 25). LOCATION. ✦ unique.
# Prerequisite (Defender or Martial Artist).
# Alter-Ego Action: Exhaust this card → shuffle up to 2 ATTACK events from your discard pile into your deck.
#   Any player may trigger this ability.
#
# MOTS-CLES (fiches lues) : prerequisite.md (decision du 17/10/2026, ua019 : jouable seulement si l'IDENTITE a le
# trait ; ici « Defender or Martial Artist » = l'un des deux suffit).
#
# CARTES DE REFERENCE
#  - `14007` Serval Industries : « Alter-Ego Action: Exhaust this card → shuffle 2 X cards from your discard pile into
#    your deck » = `SetCostFunc(Exhaust("This"))` + `SetTarget(..., from_where=["YourDiscardPile"])` + `Faces.ShuffleAllTo(
#    cibles, joueur.player_deck, effect)`.
#  - `22009` Combat Ready : « up to 2 » = `range=(1, 2)`.
#  - `40197` Safehouse : « Any player may trigger this ability » = `.AnyPlayerCanDoThis()` ; la defausse et le deck sont
#    ceux de CELUI QUI DECLENCHE (`effect.GetInitiator()`).
#  - `ua019` Flow of Battle : Prerequisite = `IdentiteATrait` (condition du jeu de la carte).
#
# TEXTE CONTRE CODE
#  ⚠ « up to 2 » : 1 ou 2 evenements (jamais 0 : un cout epuise sans effet n'est pas offert).
#  ⚠ « ATTACK events » : type Evenement + trait ATTACK, pas « toute carte d'attaque ».
#  ⚠ « from YOUR discard pile into YOUR deck » : celui qui declenche (un autre joueur utilise SA defausse).
#  ⚠ « Alter-Ego Action » : formes alter-ego seulement. Aucune limite imprimee (pas de « once per round »).
#  ⚠ « Prerequisite » : condition de JEU de la carte (identite DEFENDER ou MARTIAL ARTIST), pas de l'action.


def PrerequisDefenderOuArtisteMartial(effect: 'Effect', message: 'Message2|None' = None) -> bool:
    Unused(message)
    joueur = effect.GetInitiator() or effect.this.GetControlByOrOwner()
    if joueur is None or not Player.IsType(joueur):
        return False
    identite = joueur.GetIdentity()
    return identite.HasTrait("DEFENDER") or identite.HasTrait("MARTIAL ARTIST")


def GetAbilities() -> Sequence['Ability']:

    def thunder_dojo(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)
        initiator = effect.GetInitiator()
        Faces.ShuffleAllTo(effect.targets, initiator.player_deck, effect)

    return [
        AbilityFactory.CanPlayThisSupportCard(conditions=[PrerequisDefenderOuArtisteMartial]),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            thunder_dojo,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .AnyPlayerCanDoThis()
        .SetTarget(CardFinder(card_type=Event, trait="ATTACK"), range=(1, 2), from_where=["YourDiscardPile"]),
    ]
