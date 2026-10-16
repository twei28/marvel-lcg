from . import *

# Prowl (x3) — EVENEMENT, cout 2, [mental]. THWART.
# Hero Action (thwart): Remove 3 threat from a scheme. Shuffle 1 card with a
#   printed [mental] resource from your discard pile into your deck.
#
# Cartes de reference :
#  - evenement de contre : `doctor_druid/dr005` (`RemoveThreatFromSchemes` +
#    `.SetPlay().SetLabel('thwart').SetTarget(Scheme2)`) ;
#  - remise d'une carte de la defausse dans le deck : `nebu/22009` Combat Ready
#    (`Faces.ShuffleAllTo(cartes, joueur.player_deck, effect)` avec
#    `SetTarget(..., from_where=["YourDiscardPile"])`) ;
#  - « with a PRINTED [mental] resource » : `CardFinder(has_printed_res="B")`
#    (checker.py:441, sans conversion des wild) — meme lecture que
#    `hc012`, `mister_fantastic/mf013`.
#
# Mots-pieges :
#  - « Shuffle 1 card » : OBLIGATOIRE (pas « up to ») et le JOUEUR choisit,
#    mais s'il n'y a aucune carte eligible, l'effet de menace se resout quand
#    meme ;
#  - « printed [mental] resource » : l'icone IMPRIMEE (desc.RES = B). Une carte
#    a ressource wild (G) n'est pas une ressource [mental] imprimee ;
#  - le deck est melange par `ShuffleAllTo` (« Shuffle ... into your deck ») ;
#  - deux phrases : le contre part d'abord, puis la remise.


def GetAbilities() -> Sequence['Ability']:

    def prowl(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        this.RemoveThreatFromSchemes(effect.targets, 3, effect)

        candidates = [f for f in joueur.discard_pile.Get(True)
                      if CardFinder(has_printed_res="B").Check(f)]
        if not candidates:
            return
        choisie = joueur.AskChooseFace(
            candidates, effect,
            prompt="Shuffle 1 card with a printed [mental] resource into your deck")
        Faces.ShuffleAllTo([choisie or candidates[0]], joueur.player_deck, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            prowl,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
