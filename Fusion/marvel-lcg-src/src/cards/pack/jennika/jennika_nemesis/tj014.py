from . import *

# * Phantasm — SBIRE nemesis, x1 (2/5). PHANTOMS. SCH 2 / ATQ 2 / PV 1 / Boost 3.
# Retaliate 1. Toughness.
# When Defeated: Cloak each PHANTOMS minion in play.
# (Jennika's nemesis minion.)
#
# Mots-cles : Retaliate et Toughness : BASES AUTOMATIQUES (`desc`, fiches
# retaliate.md et toughness.md), aucun script. Cloak : fiche cloak.md (poser la carte
# d'etat Cloaked, decision utilisateur du 15/10/2026).
#
# Cartes de reference :
#  - `WhenUnitBeDefeated(WhenDefeated, "This", op)` : `leonardo/tl015` Karai (When
#    Defeated : Cloak le vilain) ;
#  - `Cloak(effect, face)` : helper du set (meme corps que leonardo_nemesis).
#
# ⚠ Mots-pieges :
#  - « each PHANTOMS MINION in play » : TOUS les sbires du trait PHANTOMS en jeu (de tous
#    les joueurs), sbires seulement ; Phantasm lui-meme est encore en jeu pendant sa
#    resolution et recoit donc une carte qui disparait avec lui ;
#  - « Cloak » = une carte Cloaked par sbire, sans plafond ;
#  - desc.Nemesis = « Jennika » (nom du heros).


def GetAbilities() -> Sequence['Ability']:

    def phantasm_vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this, message)

        for sbire in Worlds.FindCardsOnField(effect, card_type=Minion, trait="PHANTOMS"):
            Cloak(effect, sbire)

    return [
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            phantasm_vaincu,
        ),
    ]
