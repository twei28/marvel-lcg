from . import *

# Like and Subscribe! — MANIGANCE ANNEXE. Menace 2, Boost ★, Hinder 2[per_hero].
# Hinder 2[per hero]. Allies enter play exhausted.
# When Revealed : Find and reveal Screwball. Attach her to an unoccupied location, if able.
# ★ Boost : Reveal this card.
#
# Cartes de reference : pu009 (`Find.FindAndReveal`), pu015 (attache), sk115 (boost `RevealThisCard`), Hinder : desc ; « allies enter play exhausted » :
# sk097 / 40171 (`CardsEnterPlayExhausted(CardFinder(card_type=Ally), "AnyPlayer")`).
# ⚠ « Find and reveal » : elle s'engage d'abord avec le joueur qui revele, PUIS s'attache (si un lieu libre existe) ; « Allies enter play exhausted » :
# TOUS les allies, de tous les joueurs, tant que la manigance est en jeu.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        screwball = Find.FindAndReveal(effect, joueur, finder=CardFinder(card_type=Minion, name="Screwball"))
        if screwball is not None:
            AttacherAuLieuInoccupe(effect, screwball, SbireEngagePar(screwball))

    return [
        AbilityFactory.CardsEnterPlayExhausted(CardFinder(card_type=Ally), "AnyPlayer"),
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", RevealThisCard),
    ]
