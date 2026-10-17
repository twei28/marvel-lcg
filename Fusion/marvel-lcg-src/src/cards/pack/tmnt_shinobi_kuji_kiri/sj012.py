from . import *

# A Thin Place (sj012), Kuji-Kiri, soutien LOCATION MYSTIC, unique (Inkwire, TMNT Shinobi).
# Alter-Ego Action: Exhaust A Thin Place and remove 3 mystic counters from it → draw 2 cards and heal 2 damage
# from your identity.
# Response: After you play a Kuji-Kiri card from your hand, exhaust A Thin Place → place 1 mystic counter here.
#
# Mots-cles (fiches lues AVANT le code) : Shinobi (`shinobi.md` : `CarteShinobi("Kuji-Kiri")`, classe, Dual).
# Cartes de reference : `thor/06017` Hall of Heroes (« Alter-Ego Action: Exhaust X and remove 3 glory counters
# from it → draw 3 cards » : `CostFunc.Exhaust("This")` + `CostFunc.Counter("This", 3, ...)`) ;
# `skrull_menace/sk009` Alliance (« After you play a card ... from your hand » : `AfterPlayerPlayedCard(...,
# from_hand=True)`) ; `jennika/tj011` (Reponse sur une carte Shinobi, cout incliner).
# Compteur « mystic » : deja dans `CardFace.COUNTER` (`mk022`, `drs/09014`).
#
# TEXTE CONTRE CODE
#  ⚠ « Alter-Ego Action » : forme alter-ego SEULEMENT ; cout = incliner ET retirer 3 compteurs (les deux).
#  ⚠ « draw 2 cards AND heal 2 damage from your identity » : les deux effets.
#  ⚠ « Response: After you play a KUJI-KIRI card FROM YOUR HAND » : une carte Kuji-Kiri (Dual comprises, pas
#    un Path) jouee DEPUIS LA MAIN (pas depuis la defausse), toute forme ; cout = incliner : un compteur par
#    redressement ; « here » : sur ce soutien.
#  ⚠ « Kuji-Kiri » n'est PAS un trait : c'est la classe imprimee (`desc.Class`).


def GetAbilities() -> Sequence['Ability']:

    def a_thin_place(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        joueur.DrawUp(2, effect)
        this.HealthUnits([joueur.GetIdentity()], 2, effect)

    def poser_un_compteur(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)
        Faces.PlaceCountersOn([this], 1, "mystic", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            a_thin_place,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 3, 'mystic')),
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            CarteShinobi("Kuji-Kiri"),
            poser_un_compteur,
            from_hand=True,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
