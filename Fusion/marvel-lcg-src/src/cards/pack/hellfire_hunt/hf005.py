from . import *

# First Command : evenement Leadership, cout 1.
# Play only during your turn. You cannot play this card if you have played another card this turn.
# Hero Action: Ready an ally. That ally gets +1 THW and +1 ATK this phrase (sic : « this PHASE »).
#
# Cartes de reference : 03003 (`GainUntilPhaseEnd`), `PlayerStat.this_turn_played_cards` (player_stat.py), `Faces.ReadyAll`.
# ⚠ « if you have played ANOTHER card this turn » : aucune carte jouee ce tour avant celle-ci ; « this phrase » : faute d'impression, lue « this phase ».
def GetAbilities() -> Sequence['Ability']:
    def premier_ordre(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        for allie in effect.targets:
            Faces.ReadyAll([allie], effect)
            allie.GainUntilPhaseEnd(effect, attack=1, thwart=1)

    def aucune_autre_carte(effect: 'Effect') -> bool:
        joueur = JoueurDe(effect)
        return joueur is not None and len([f for f in joueur.stat.this_turn_played_cards if f is not effect.this]) == 0

    action = AbilityFactory.WhenInYourPlayTurn(
        AbilityType.HeroAction,
        premier_ordre,
    ).SetPlay().SetLabel().SetTarget(Ally)
    action.conditions = [lambda effect, message: aucune_autre_carte(effect)] + action.conditions
    return [action]
