from . import *

# Oathbrother — AMELIORATION, cout 2, [mental]. ASGARD. TITLE.
# Hero Response: After a minion enters play, seek an event from your deck and
#   add it to your hand. (Limit once per phase.)
#
# CARTES DE REFERENCE
#  - `bk016` Tallus et `tt018` Red Wolf : `AfterCardEnterPlay` en Reponse.
#  - `04001b` Clint Barton : la fouille du deck puis `GainCard`.
#
# TEXTE CONTRE CODE
#  « After A MINION enters play » -> n'importe lequel, y compris ceux poses
#    par le joueur lui-meme. Et c'est voulu : br005 Star Jump et br011 Hammer
#    Time CONVOQUENT des sbires, ce sont donc les cartes du pack qui
#    declenchent celle-ci. Ne PAS ajouter `under_your_control`, qui n'est pas
#    dans le texte et casserait la combinaison.
#  « seek an event FROM YOUR DECK » -> le DECK SEUL, pas la defausse : c'est
#    le contraste avec `Worthy` et `Starfarer`, qui disent « find » et
#    couvrent les deux zones. Trois formulations voisines dans le meme pack.
#  « (Limit once per PHASE.) » -> `.LimitOncePerPhase()`, et non par round :
#    la carte peut donc servir deux fois par round, une fois en phase joueur
#    et une fois en phase du vilain, ou les sbires arrivent.


def GetAbilities() -> Sequence['Ability']:

    def frere_d_armes(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        face = Search.PlayerCard(
            effect, joueur,
            include_player_deck=True,
            card_type=Event,
        )
        if face is not None:
            joueur.GainCard(face, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.HeroResponse,
            Minion,
            frere_d_armes,
        ).LimitOncePerPhase(),
    ]
