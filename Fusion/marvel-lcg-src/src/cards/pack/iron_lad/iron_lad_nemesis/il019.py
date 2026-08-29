from . import *

# * Kang the Conqueror — sbire nemesis d'Iron Lad (2/5)
# Toughness. Villainous.
# When Revealed: Put the highest cost Iron Lad upgrade in play under Kang
#   the Conqueror.
# When Defeated: Return the upgrade under here to its owner's hand. Set
#   Kang the Conqueror aside.
#
# Toughness/Villainous lus nativement depuis desc, aucun script requis pour
# ces deux mots-cles (voir mots-cles/toughness.md, villainous.md). "Highest
# cost" : `Filter.One(faces, effect, highest_cost=True)` (game/operate/
# filter.py), egalites tranchees par le moteur comme sur toute autre carte.
# Empiler dessous : `this.TuckCardUnderHere(...)` (modele : aos/
# aim_abduction/50080.py). Mettre de cote a la defaite :
# `Faces.SetAside([this], effect)` (game/operate/faces.py:158).
#
# CORRECTIF (trouve par test_capacites.py) : `AfterUnitBeDefeated` (message
# APRES coup) arrive TROP TARD -- le nettoyage generique de la carte
# empilee (son PlaceCardArea) la defausse deja au moment ou ce hook se
# declenche (observe : "Iron Lad's Suit were discarded" avant meme le
# message de defaite). Remplace par `WhenUnitWouldBeDefeated` (hook AVANT
# coup), qui recupere la carte empilee pendant qu'elle est encore la.

def GetAbilities() -> Sequence['Ability']:

    def kang_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)

        cible = Filter.One(UpgradesIronLadEnJeu(effect), effect, highest_cost=True)
        if cible:
            this.TuckCardUnderHere(cible, effect)

    def kang_defeated(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)

        sous_jacentes = this.GetPlacedCardArea().Get()
        for face in sous_jacentes:
            owner = face.GetOwnerPlayer()
            if owner:
                Faces.AddToHand([face], owner, effect)
        Faces.SetAside([this], effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            kang_revealed,
        ),
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            kang_defeated,
        ),
    ]
