from ..commun import *

# Set SWAT Team (pack MC×DC 2026) : la police. Une manigance annexe permanente, SWAT, qui accumule des compteurs
# « wanted » ; les sbires POLICE y posent leurs menaces.
#
# ⚠ Compteur `wanted` ajoute a CardFace.COUNTER (21/10/2026). « place that threat on SWAT, if able » : quand un sbire
# POLICE manigance, la menace qu'il aurait posee sur le complot du joueur va sur SWAT ; si SWAT est en jeu (« if able »).

def TrouverSwat(effect: 'Effect') -> 'EncounterSideScheme|None':
    return Worlds.FindCardOnField(effect, name="SWAT", card_type=EncounterSideScheme)


def CompteursRecherche(effect: 'Effect') -> int:
    swat = TrouverSwat(effect)
    return swat.GetCounters('wanted') if swat is not None else 0


def MenaceSurSwat() -> 'Ability':
    """« When <sbire POLICE> schemes, place that threat on SWAT, if able. » Modele fne/drive/60189.py (Traffic Jam) :
    la menace que le sbire allait poser est empechee, puis posee sur SWAT. « If able » : SWAT doit etre en jeu."""

    def rediriger(effect: 'Effect', message: 'Message.WhenSchemeWouldPlaceThreat') -> None:
        this = effect.this
        swat = TrouverSwat(effect)
        valeur = message.value
        if swat is None or valeur <= 0 or message.trigger is swat:
            return
        message.PreventThreat("All", effect)
        this.PlaceThreatOnSchemes([swat], valeur, effect)

    def par_ce_sbire(effect: 'Effect', message: 'Message.WhenSchemeWouldPlaceThreat') -> bool:
        auteur = message.sch_message.trigger if message.sch_message is not None else message.by_effect.this
        return auteur is effect.this

    return AbilityFactory.WhenSchemeWouldPlaceThreat(AbilityType.ForcedInterrupt, None, rediriger, conditions=[par_ce_sbire])
