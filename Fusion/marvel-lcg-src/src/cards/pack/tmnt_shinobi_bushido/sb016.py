from . import *

# * Wakizashi — AMELIORATION unique ✦ NINJA. WEAPON., classe Bushido (Inkwire, TMNT Shinobi). Cout 1, [mental].
# Restricted.
# Hero Response: After an OATH upgrade is discarded from play, exhaust this card -> draw 1 card.
# « I prefer the traditional dashido. » —Moja
#
# Mots-cles (fiches lues AVANT le code) : Restricted (restricted.md : BASE AUTOMATIQUE, `desc.Restricted = "1"`, aucun script) ;
# samurai counter / OATH (samurai-counter.md) pour le trait OATH.
#
# Cartes de reference :
#  - « After <X> is discarded from play, exhaust this card -> <effet> » : `red_guardian/rg010` Shield Harness
#    (`AfterCardDiscard(HeroResponse, CardFinder(...), op, conditions=[defausse_depuis_le_jeu]).SetCostFunc(Exhaust("This"))` ;
#    `from_where="PlayerArea"` est inutilisable pour une amelioration attachee, le test fidele de « from play » est
#    `message.from_area.flags.is_in_play`) ; le filtre « depuis le jeu » va dans `conditions`, jamais dans le corps (RECETTES §1) ;
#  - pioche : `DrawUp` (`trors/spider_woman/04032`).
#
# TEXTE CONTRE CODE
#  ⚠ « After AN OATH UPGRADE is discarded FROM PLAY » : une amelioration portant le trait OATH, celle de N'IMPORTE QUEL joueur (aucune
#    mention « you control »), quittant le JEU pour la defausse (pas depuis la main, pas depuis le deck) ; la defausse par Uses (dernier
#    compteur) en est une. Wakizashi n'est pas OATH : elle ne repond pas a sa propre defausse.
#  ⚠ « Hero Response » : forme heros seule. « exhaust this card -> » : COUT, une fois par redressement.
#  ⚠ « draw 1 card » : exactement 1.
#  ⚠ Unique ✦ (nom a « * ») ; Restricted : base automatique, lue dans `desc`.


def GetAbilities() -> Sequence['Ability']:

    def defaussee_depuis_le_jeu(effect: 'Effect', message: 'Message.AfterCardDiscard') -> bool:
        return message.from_area.flags.is_in_play

    def wakizashi(effect: 'Effect', message: 'Message.AfterCardDiscard') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is not None:
            joueur.DrawUp(1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterCardDiscard(
            AbilityType.HeroResponse,
            CardFinder(card_type=Upgrade, trait="OATH"),
            wakizashi,
            conditions=[defaussee_depuis_le_jeu],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
