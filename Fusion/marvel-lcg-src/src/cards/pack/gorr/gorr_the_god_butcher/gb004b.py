from . import *

# Deicide 1B — COMPLOT PRINCIPAL, face jouable. Seuil 3 par joueur,
# acceleration +1 par joueur, menace de depart 0.
#
# Forced Response: After step 1 of the villain phase, if the villain's stage
#   number is 2 or 3, place 1 plan counter here. Then, if there are 3 or more
#   plan counters here, advance to stage 2A.
# Forced Response: After Gorr the God Butcher defeats an ally, place 1 threat
#   on this scheme.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - Compteur pose a l'etape 1 de la phase du vilain puis seuil qui declenche :
#   04113b (The Mad Doctor, pack trors) — `AfterResolveVillainPhaseStep(
#   ForcedResponse, 1, ...)`, `Faces.PlaceCountersOn([this], 1, 'test', ...)`
#   puis test `this.GetCounters('test') >= 3`. Copie exacte de la forme.
# - « advance to stage 2A » : 50087b (Batroc), `this.Advance("2A", effect)`.
# - « After X defeats an ally » : `AfterUnitDefeatedUnit`, le meme declencheur
#   que gp002 (« if this attack defeats »), restreint ici a l'attaquant Gorr
#   et a une cible de type `Ally`.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « if the VILLAIN'S STAGE NUMBER is 2 or 3 » -> le stade du VILAIN (gb002 ou
#   gb003), pas celui du complot. L'entier lu dans `desc.Stage` est
#   `printed_stage` (has_stage.py ; « I »/« II »/« III » -> 1/2/3), lu comme
#   le font deja 02029, dt033 et 50067b. On interroge donc le vilain en jeu,
#   pas `this`.
# « place 1 plan counter HERE » -> sur ce complot, pas sur l'environnement.
# « Then, if there are 3 OR MORE » -> comparaison >=, et le compteur vient
#   d'etre pose : le test se fait APRES la pose, dans la meme reponse.
# « After GORR THE GOD BUTCHER defeats an ALLY » -> l'attaquant doit etre le
#   vilain (un sbire qui tue un allie ne compte pas) et la victime un allie
#   (pas un heros). C'est la seconde horloge de la carte : le complot monte
#   aussi tout seul quand les alliés tombent.
# « place 1 threat ON THIS SCHEME » -> sur lui-meme, valeur nue.


def GetAbilities() -> Sequence['Ability']:

    def stade_du_vilain(effect: 'Effect') -> int:
        vilain = Worlds.FindVillain(effect)
        return vilain.printed_stage if vilain else 0

    def le_plan_avance(effect: 'Effect', message: 'Message.AfterResolveVillainPhaseStep') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(message)

        if stade_du_vilain(effect) not in (2, 3):
            return

        Faces.PlaceCountersOn([this], 1, 'plan', effect)
        if this.GetCounters('plan') >= 3:
            this.Advance("2A", effect)

    def un_allie_tombe(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(message)

        this.PlaceThreatOnSchemes([this], 1, effect)

    return [
        AbilityFactory.AfterResolveVillainPhaseStep(
            AbilityType.ForcedResponse,
            1,
            le_plan_avance,
        ),
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.ForcedResponse,
            CardFinder(name="Gorr the God Butcher"),
            Ally,
            un_allie_tombe,
        ),
    ]
