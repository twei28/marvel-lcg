from . import *

# Creeping Corruption (face B) — AMELIORATION. OVERPOWERING. Permanent. Max 1 per player.
# If there are at least 5 corruption counters here, you are defeated.
# Action : Exhaust Creeping Corruption and place 1 corruption counter here -> draw 2 cards, then discard 1 card from your hand.
#
# Cartes de reference : sl072a (meme structure), tt/enchantress/55007a (seuil de compteurs), sm/sinister_six/27099 (`DiscardHandCards((1, 1), effect)`),
#  skrull_menace/skrull_menace_campaign/sk273 (`Faces.DefeatUnits`), game/card/face/card_type/identity.py (`OnBeDefeated` : l'identite vaincue ELIMINE le joueur).
# ⚠ Mots-pieges : « you are defeated » = l'identite du joueur est vaincue (c'est ce qui l'elimine dans le moteur, regle RR : « a player is eliminated when his
#  identity is defeated ») ; elle part par `DefeatUnits` sur l'identite, pas par `Eliminate` direct (les interruptions de defaite restent valables). « then discard 1
#  card from your hand » = CHOISI par le joueur, apres la pioche de 2. Pas de « Setup » sur cette face. La face B ne se retourne jamais.


def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.AfterCardPlacedCounter') -> None:
        this = effect.this.CastTo(Upgrade)
        joueur = this.GetControlByPlayer()
        Faces.DefeatUnits([joueur.GetIdentity()], this, effect)

    def piocher(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        joueur = effect.GetInitiator()
        joueur.DrawUp(2, effect)
        joueur.DiscardHandCards((1, 1), effect)

    return [
        AbilityFactory.IfThereAreAtLeastCounterHere(SEUIL_CORRUPTION, 'corruption', vaincu),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, piocher)
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.PlaceCounter("This", 1, 'corruption')),
    ]
