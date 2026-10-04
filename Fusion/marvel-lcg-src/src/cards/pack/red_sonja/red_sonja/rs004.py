from . import *

# Scarlet Huntress — evenement signature, x2 (4-5/15). THWART. Cout 3,
# ressource [B].
# Hero Action (thwart): Remove 6 threat from a scheme. For each point of
# excess threat removed by this thwart, reduce the cost of the next event
# you play this phase by 1.
#
# CARTE DE REFERENCE : `rs003` Savage Steel, meme structure ("excess" +
# "reduce the cost of the next event"). Symetrique cote menace :
# `MenaceExcedentaireDeCeContre` (`__init__.py` de ce dossier) calcule
# l'exces a la main (« excess threat » n'a pas d'equivalent officiel
# « excess damage », voir le commentaire de cette fonction).
#
# TEXTE CONTRE CODE : identique a `rs003`, cote menace. « For each point of
# excess threat removed » : seulement si la manigance est ENTIEREMENT VIDEE
# par ce contre, jamais un simple retrait partiel.

def GetAbilities() -> Sequence['Ability']:

    def scarlet_huntress(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if not isinstance(joueur, Player):
            return

        exces = MenaceExcedentaireDeCeContre(effect, effect.targets, 6)
        if exces > 0:
            Worlds.UpdateNextCardPlayCost(
                joueur, -exces, effect,
                finder=CardFinder(card_type=Event),
                in_this="Phase",
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            scarlet_huntress,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
