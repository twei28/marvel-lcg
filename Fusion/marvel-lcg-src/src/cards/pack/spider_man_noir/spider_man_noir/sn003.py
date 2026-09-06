from . import *

# Webs Within Webs — EVENEMENT, cout 2, [mental]. THWART. x2.
# Hero Action (thwart): Discard the top card of the encounter deck -> remove
#   threat from a scheme equal to 3 plus the number of boost icons discarded
#   this way. Tuck the discarded card under your hero (to a maximum of 3).
#
# CARTES DE REFERENCE
#  - `42006` Natural Flight : « Hero Action (thwart): Remove N threat from a
#    scheme » -> `SetPlay().SetLabel('thwart').SetTarget(Scheme2)` puis
#    `RemoveThreatFromSchemes(effect.targets, N, effect)`.
#  - `15004` / `ho014` : `Worlds.DiscardEncounterTopCard` et
#    `FacesCounter.CountTotalBoostIcons`.
#  - `ho009` : `CostFunc.Custom(None, fn)` pour un cout arbitraire.
#
# TEXTE CONTRE CODE
#  ⚠ LA FLECHE EST APRES « Discard the top card of the encounter deck » :
#    c'est le COUT. Deck de rencontre vide, la carte n'est pas jouable — et
#    non « jouable pour 3 menaces ».
#  « equal to 3 PLUS the number of boost icons » -> 3 est un plancher, pas un
#    plafond. Une carte a 2 icones retire 5 menaces.
#  « discarded THIS WAY » -> les icones de LA carte defaussee a l'instant,
#    jamais celles de la pile ni de la defausse.
#  ⚠ « Tuck the discarded card under your hero » est une SECONDE phrase, pas
#    une branche : elle tombe TOUJOURS, meme si le contre n'a rien retire.
#    Et « your hero » designe la meme pile que « under your identity »
#    ailleurs dans le set (voir le `__init__.py`).
#  « (to a maximum of 3) » -> plafond applique par `GlisserSousIdentite` ;
#    pile pleine, la carte reste en defausse de rencontre.


def GetAbilities() -> Sequence['Ability']:

    def defausser_le_dessus(cibles: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(cibles)
        face = Worlds.DiscardEncounterTopCard(effect)
        if face is None:
            return False
        setattr(effect, "_sn003_carte_defaussee", face)
        return True

    def toiles_dans_les_toiles(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        defaussee = getattr(effect, "_sn003_carte_defaussee", None)
        valeur = 3 + IconesDeBoost([defaussee] if defaussee is not None else [])
        this.RemoveThreatFromSchemes(effect.targets, valeur, effect)

        if defaussee is not None:
            GlisserSousIdentite(effect, [defaussee], JoueurDeCetteCarte(effect))

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            toiles_dans_les_toiles,
        ).SetPlay().SetLabel('thwart')
        .SetCostFunc(CostFunc.Custom(None, defausser_le_dessus))
        .SetTarget(Scheme2),
    ]
