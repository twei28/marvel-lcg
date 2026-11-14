from . import *

# * External Darkness : COMPLOT ANNEXE (paysage), menace de depart 2 par joueur, Crisis, boost 3. Set « Merged Sentry ».
# When Revealed: Find Merged Sentry and put him into play engaged with you. Place X overwhelm counters on Merged Sentry, where X is equal to the main scheme's current stage number.
#
# CARTES DE REFERENCE
#  - « Find X and put it into play engaged with you » : `ca016` / `ca022` (`Search.EncounterCard(.., include_discard_pile=True, include_set_aside=True, name=..)` + `face.PutIntoPlay(joueur, effect)`) ; stade : `printed_stage` (`has_stage.py`).
#  - Crisis : lu dans `desc` (fiche `crisis.md`).
#
# TEXTE CONTRE CODE
#  « Find » : deck, defausse et zone de cote. Deja en jeu : il s'engage avec le joueur (pas de recherche). « X = the MAIN SCHEME's current stage » : le stade du complot principal (pas du vilain, voir rr022). Absent : rien.


def GetAbilities() -> Sequence['Ability']:

    def external_darkness(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        merged = Worlds.FindCardOnField(effect, name=NOM_MERGED, card_type=Minion)
        if merged is None:
            merged = Search.EncounterCard(effect, joueur, include_discard_pile=True, include_set_aside=True, name=NOM_MERGED)
            if merged is not None:
                merged.PutIntoPlay(joueur, effect)
        elif merged.CastTo(Minion).engaged_player is not joueur:
            merged.CastTo(Minion).EngagePlayer(joueur, effect)
        if merged is None or not merged.IsInPlay():
            return
        complot = Worlds.FindMainScheme(effect)
        x = int(getattr(complot, "printed_stage", 1) or 1)
        Faces.PlaceCountersOn([merged], x, NOM_SUBMERSION, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, external_darkness),
    ]
