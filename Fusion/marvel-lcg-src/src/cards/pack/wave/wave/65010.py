from . import *

# * Wave's Crown — amelioration signature, x1 (15/15). TECH. Cout 2.
# Wave gains +1 THW. You may play cards tucked under here as if they were in
# your hand. Action: Exhaust Wave's Crown -> tuck 1 faceup card in your
# Rising Tide area under here (max 2).
#
# TROIS mecanismes NATIFS, tous verifies sur le pack `black_cat` (Rainy) qui
# vit du meme theme « glisser puis jouer de la ce qui est glisse » :
#  - « Wave gains +1 THW » -> `GiveKeywordToAttached("You", thwart=1)`,
#    modele an009 Xiphos (Angela +1 ATK).
#  - « play cards tucked under here as if in your hand » -> facture DEDIEE,
#    `AbilityFactory.YouMayPlayCardLikeInHand(Rule, None,
#    from_where="ThisPlacedCard")` (game/ability/factory/play.py:400) : compare
#    litteralement `effect.this.GetPlacedCardArea() == face.card.area`, donc
#    exactement « cartes glissees SOUS CETTE carte ». Rien a ecrire pour jouer
#    la carte ensuite, ce hameçon suffit a la rendre jouable normalement.
#  - « tuck ... under here » -> `CardFace.TuckCardUnderHere(face, effect,
#    peek=True)`. `peek=True` (pas le defaut `False`) : sans lui la carte
#    entre face CACHEE meme au proprietaire (`PlaceCardHere`, card_face.py),
#    et le joueur ne pourrait plus savoir laquelle jouer -- la Rising Tide
#    area, elle, l'imprime EXPLICITEMENT visible au proprietaire avant le
#    glissement (elle y etait face visible, condition du cout).
#
# « (max 2) » : plafond A LA POSE (contrairement au pack `black_cat`, dont le
# plafond de 3 est une regle de MENAGE apres coup, jamais un refus -- voir le
# commentaire de tete de `black_cat/__init__.py`). Ici rien n'indique un
# nettoyage automatique : la capacite est simplement OFFERTE seulement s'il y
# a encore de la place, verifie par `conditions=[...]` avant meme de proposer
# le choix (meme lecon que `CostFunc.LookAtDeck.has_enought_size` : une
# capacite jouable sans que son cout puisse aboutir defausse la carte pour
# rien).

def GetAbilities() -> Sequence['Ability']:

    def moins_de_deux_glissees(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        this = effect.this.CastTo(Upgrade)
        return this.GetPlacedCardArea().GetSize() < 2

    def waves_crown(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        initiator = effect.GetInitiator()
        if not isinstance(initiator, Player):
            return
        candidates = CartesDansRisingTide(initiator, face_visible=True)
        if not candidates:
            return
        choisie = initiator.AskChooseFace(
            candidates, effect, forced=False,
            prompt="Tuck under Wave's Crown",
        )
        if choisie is None:
            return
        this.TuckCardUnderHere(choisie, effect, peek=True)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            thwart=1,
        ),
        *AbilityFactory.YouMayPlayCardLikeInHand(
            AbilityType.Rule,
            None,
            from_where="ThisPlacedCard",
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            waves_crown,
            conditions=[moins_de_deux_glissees],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
