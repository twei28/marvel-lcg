from . import *
# * Smasher, face heros. Prefixe `sz`.
#
# Forced Response: After you play an EXOSPEX upgrade, discard all other EXOSPEX upgrades you control.
#
# Cartes de reference : 56029b Teddy Altman (meme famille « une seule amelioration [[Shapeshift]] ») pour le filtre de trait ;
# `AfterPlayerPlayedCard(ForcedResponse, "You", <filtre>, op)` (hz001a) pour le declencheur.
# ⚠ « all OTHER » : la carte qu'on vient de jouer RESTE (`message.played_face`), toutes les autres EXOSPEX qu'on controle partent.
def GetAbilities() -> Sequence['Ability']:
    def smasher(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)
        joueur = effect.GetInitiator()
        jouee = message.played_face
        autres = [f for f in ExospexEnJeu(joueur) if f is not jouee]
        if autres:
            Faces.DiscardAll(autres, effect)
    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.ForcedResponse,
            "You",
            CardFinder2(TRAIT_EXOSPEX, Upgrade),
            smasher,
        ),
    ]
