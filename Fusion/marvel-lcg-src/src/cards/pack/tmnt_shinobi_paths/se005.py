from . import *

# * The Last Rōnin — PATH (la Voie du Dernier Ronin), UNIQUE, Paths hybrides (avance). SENPAI.
# Permanent. You get -1 hand size.
# You may play cards tucked here as if they were in your hand. (Max 2 tucked cards.)
# Kanpeki — Action: Exhaust this card and tuck 1 Shinobi card from your hand under here -> draw 1 card.
#
# Mots-cles (fiches lues AVANT le code) : Tuck (tuck.md) ; Permanent (permanent.md) ; Shinobi / Path (shinobi.md).
#
# Cartes de reference :
#  - « You may play cards tucked here as if they were in your hand » : `casey_jones/tc013` Casey's Bag
#    (`AttachedCardCanPlayLikeInHand()` SANS `also_spend` ni `also_discard` : le texte ne dit que « play »,
#    decision deja prise sur le Sac) ;
#  - « (Max N tucked cards) » : `donatello/td012` Donatello's Shell (le plafond est une CONDITION de l'action qui
#    range) ;
#  - « tuck 1 card from your hand under here » EN COUT : `CostFunc.TuckCardHere` (`bp/51018`), cible
#    `YourHandCards` filtree par classe Shinobi.
#
# TEXTE CONTRE CODE
#  ⚠ « Action » (sans « Hero ») : possible dans les DEUX formes de l'identite.
#  ⚠ « Exhaust this card AND tuck 1 SHINOBI card from YOUR HAND » : deux couts ; la carte rangee doit etre une
#    carte Shinobi (Dual comprise), prise dans la main ; « then -> draw 1 card » : piocher UNE carte.
#  ⚠ « (Max 2 tucked cards) » : l'action est refusee quand 2 cartes sont deja rangees (sinon on inclinerait la
#    Voie pour rien) ; la pioche part meme si le deck est vide (retour au cas general du moteur).
#  ⚠ « play ... as if they were in your hand » : jouer SEULEMENT (voir Casey's Bag). Les Shinobi rangees
#    se jouent donc depuis le dessous de la Voie, aux couts habituels.
#  ⚠ Unique (✦) : une seule The Last Rōnin par deck et en jeu.


def GetAbilities() -> Sequence['Ability']:

    def moins_de_deux_rangees(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        return effect.this.GetPlacedCardArea().GetSize() < 2

    def kanpeki(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Path)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        joueur.DrawUp(1, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis("You", hand_size=-1),
        *AbilityFactory.AttachedCardCanPlayLikeInHand(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            kanpeki,
            conditions=[moins_de_deux_rangees],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.TuckCardHere(
            Select.From("YourHandCards", finder=CarteShinobi(), range=(1, 1)),
        )),
    ]
