from . import *

# The Grim Hunt — custom « Kajislav », complot secondaire nemesis
# When Revealed: Set Kraven the Hunter aside, out of play.
# 3 menaces par joueur au depart (cards.json), +1 par joueur a la fin de chaque
# phase du vilain, et si le complot est « complete » (5 menaces par joueur) on
# met en jeu le Kraven mis de cote, engage avec le premier joueur.
#
# ECART ASSUME : le moteur ne gere `TargetThreat` et `EscalationThreat` que sur
# les complots PRINCIPAUX (scheme_main.py). Les deux valeurs imprimees sur ce
# complot secondaire sont donc cablees ici, a la main.

MENACE_CIBLE = "5*"
MENACE_PAR_TOUR = "1*"


def GetAbilities() -> Sequence['Ability']:

    def trouver_kraven(effect: 'Effect') -> 'CardFace|None':
        faces = Worlds.GetSetAsideAreaCards(
            effect,
            CardFinder(name="Kraven the Hunter", card_type=Minion)
        )
        return faces[0] if faces else None

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)

        face = Search.EncounterCard(
            effect,
            include_discard_pile=True,
            name="Kraven the Hunter",
            card_type=Minion,
        )
        if face:
            Faces.SetAside([face], effect)

    def fin_de_phase(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        this = effect.this.CastTo(EncounterSideScheme)

        valeur = Worlds.ConvertPerPlayerIconToInt(MENACE_PAR_TOUR, effect)
        this.PlaceThreatOnSchemes([this], valeur, effect)

        cible = Worlds.ConvertPerPlayerIconToInt(MENACE_CIBLE, effect)
        if this.threat < cible:
            return

        kraven = trouver_kraven(effect)
        if kraven:
            kraven.PutIntoPlay("FirstPlayer", effect)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
        AbilityFactory.WhenVillainPhaseEnd(
            AbilityType.ForcedResponse,
            fin_de_phase
        ),
    ]
