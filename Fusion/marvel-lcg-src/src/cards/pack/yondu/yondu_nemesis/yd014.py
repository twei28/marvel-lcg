from . import *

# Price on Your Head — complot ANNEXE nemesis (1/5). Menace de depart 2 par
# joueur, Boost 3.
# Forced Response: After a friendly character is defeated, heal 1 damage from
#   Sav'rkk. If Sav'rkk is not in play, heal 1 damage from the villain instead.
#
# Cartes de reference :
#  - `ok014` / `08031` / `as019` pour `AfterUnitBeDefeated(ForcedResponse,
#    <qui>, op)`.
#  - `42018` * Angel's Aerie pour `this.HealthUnits(cibles, 1, effect)`.
#  - `aos/batroc/__init__.py:7` pour la recherche d'une carte nommee sur le
#    terrain (`Worlds.FindCardOnField(effect, name=...)`).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « a **FRIENDLY** character » : un heros, un alter-ego ou un allie — pas un
#    sbire, pas le vilain. C'est le mot qui fait la carte : elle punit la perte
#    d'un allie, et un deck d'Agressivite en perd souvent.
#  - « heal 1 damage from **Sav'rkk**. If Sav'rkk is not in play, heal 1 from
#    the **villain** INSTEAD » : un repli, pas un cumul. `instead` veut dire
#    que le soin PART d'un endroit et ARRIVE ailleurs, jamais qu'il est
#    duplique (leçon The Spot).
#  - « **Forced** Response » : automatique, aucun choix offert.
#  - « Menace de depart 2[per_hero] » : `StartingThreat: "2*"`, base
#    automatique lue dans `desc`, aucun script.
#  - Le complot ne pose AUCUNE menace lui-meme : il ne fait que soigner. Sa
#    pression vient de sa menace de depart et de ce qu'il faut le contrer.


def GetAbilities() -> Sequence['Ability']:

    def price_on_your_head(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        this = effect.this.CastTo(SchemeSide2)
        Unused(message)

        cible = Worlds.FindCardOnField(effect, name="Sav'rkk", card_type=Minion)
        if cible is None:
            vilains = Worlds.GetVillains(effect)
            cible = vilains[0] if vilains else None
        if cible is None:
            return
        this.HealthUnits([cible], 1, effect)

    return [
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.ForcedResponse,
            Friend,
            price_on_your_head,
        ),
    ]
