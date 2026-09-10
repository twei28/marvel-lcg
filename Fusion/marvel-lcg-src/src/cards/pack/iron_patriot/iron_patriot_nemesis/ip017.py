from . import *

# Reign's End — MANIGANCE SECONDAIRE de nemesis (2/5). 6 menaces, boost 3.
# Forced Interrupt: When a character enters play, place 2 threat here.
# Forced Response: After a REGISTERED ally is defeated, place that ally
#   facedown under this scheme. If there are 3[per_hero] cards under this
#   scheme, the players lose the game.
#
# ⚠⚠ C'EST LA CONDITION DE DEFAITE DU PACK. L'insert : « Norman must deal with
# the Reign's End side scheme, forcing his surrender if he loses enough minions
# he can't control. » Elle n'entre en jeu que par `ip015` Exposed Insanity, et
# seulement si l'on n'avait AUCUN allie REGISTERED a defausser.
#
# CARTES DE REFERENCE
#  - `09029` Open the Dark Dimension : `this.PlaceCardHere(face, False, effect)`
#    pose une carte FACE CACHEE sous une manigance, et
#    `this.GetPlacedCardArea().Get()` les relit. Meme geste, meme zone.
#  - `aos/campaign.py` (Conseil de Zemo) : `Worlds.SetGameOver(False, effect)`
#    — `False` veut dire « les joueurs perdent ».
#  - `AbilityFactory.AfterUnitBeDefeated(...)` : cf. `ip001a`.
#
# TEXTE CONTRE CODE
#  ⚠ « When A CHARACTER enters play » : TOUS les personnages, allies du joueur
#    comme sbires de la rencontre, et de tous les joueurs. La manigance monte
#    donc tres vite — c'est le prix a payer pour une armee.
#  ⚠ « Forced INTERRUPT » : la menace se pose AVANT que le personnage n'entre,
#    d'ou `WhenCardEnterPlay` et non `AfterCardEnterPlay`.
#  ⚠ « place that ally FACEDOWN under this scheme » : face cachee. Deuxieme
#    argument `False` de `PlaceCardHere`. Ce n'est pas une defausse : l'allie
#    quitte le circuit du deck REGISTERED pour de bon.
#  ⚠ « 3[per_hero] cards » : PAR JOUEUR. `Worlds.ConvertPerPlayerIconToInt("3*")`.
#  ⚠ On compte APRES avoir pose : le troisieme allie declenche la defaite.
#  ⚠ Cette carte ne s'attache pas et ne se defausse pas seule : elle se contre
#    comme n'importe quelle manigance secondaire.


def GetAbilities() -> Sequence['Ability']:

    def un_personnage_entre(effect: 'Effect', message: 'Message.WhenCardEnterPlay') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(message)
        this.PlaceThreatOnSchemes([this], 2, effect)

    def un_allie_registered_tombe(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        allie = message.trigger
        if allie is None:
            return
        this.PlaceCardHere(allie, False, effect)

        limite = Worlds.ConvertPerPlayerIconToInt("3*", effect)
        if len(this.GetPlacedCardArea().Get()) >= limite:
            Worlds.SetGameOver(False, effect)

    return [
        AbilityFactory.WhenCardEnterPlay(
            AbilityType.ForcedInterrupt,
            Unit2,
            un_personnage_entre,
        ),
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.ForcedResponse,
            CardFinder(card_type=Ally, trait=TRAIT_REGISTERED),
            un_allie_registered_tombe,
        ).NoOutOfPlayLimit(),
    ]
