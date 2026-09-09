from . import *

# Symbiotic Sneak Attack — EVENEMENT, cout 1, RES [physical]. SYMBIOTE. TACTIC.
# Action: Choose an ally in your hand that shares a TRAIT with your identity ->
#   put that ally into play. If that ally is still in play at the end of the
#   phase, discard it.
#
# CARTE DE REFERENCE
#  - `23017` Sneak Attack (Meneur, pack warm) : meme cout, meme ressource,
#    meme texte. Corps repris tel quel.
#
# TEXTE CONTRE CODE
#  ⚠ « Action » et non « Hero Action » : la carte se joue dans LES DEUX
#    formes -> `AbilityType.Action`, et `SetLabel()` sans etiquette.
#  ⚠ « an ally IN YOUR HAND » -> `from_where=["YourHandCards"]`, sinon la
#    cible serait cherchee en jeu.
#  ⚠ « If that ally is STILL in play » : on refiltre a la fin de la phase, on
#    ne defausse pas aveuglement — l'allie a pu partir entre-temps.
def GetAbilities() -> Sequence['Ability']:

    def symbiotic_sneak_attack(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        initiator = effect.GetInitiator()
        for allie in effect.targets:
            allie.PutIntoPlay(initiator, effect)

        def defausser_en_fin_de_phase():
            encore_en_jeu: List['CardFace'] = [a for a in effect.targets if a.IsInPlay()]
            Faces.DiscardAll(encore_en_jeu, effect)

        RunAt.TheEndOfThePhase(effect, defausser_en_fin_de_phase)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            symbiotic_sneak_attack
        ).SetPlay().SetLabel()
        .SetTarget(Ally, share_trait_with_your_identity=True, from_where=["YourHandCards"]),
    ]
