from . import *

# Solar Flare — EVENEMENT, cout 2, [energy]. ATTACK. SUPERPOWER. x2 (Binary 7/15, 8/15).
# Hero Action (attack): Deal 4 damage to an enemy. If you have at least
#   [energy][energy] resources in your hand, deal 2 additional damage to that
#   enemy.
#
# Cartes de reference :
#  - **`wsp/13013`** Into the Fray / **`core/05015`** Tackle : evenement
#    d'attaque, `WhenInYourPlayTurn(HeroAction, op).SetPlay().SetLabel('attack')
#    .SetTarget(Enemy)` + `this.DealDamage(effect.targets, n, effect)`.
#  - « deal N additional damage » : comme `13015` ou `05015`, la valeur de
#    l'attaque elle-meme est augmentee (une seule attaque de 6), pas une seconde
#    attaque de 2 (une seconde attaque declencherait deux fois retaliate).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « an ENEMY » : vilain ou sbire.
#  - « at least [energy][energy] resources in your hand » : 2 ICONES au moins,
#    lues A LA RESOLUTION (apres paiement : une Energy Torrent depensee pour
#    payer la carte ne compte plus). Helper `EnergieEnMain`.
#  - « to THAT enemy » : la meme cible.


def GetAbilities() -> Sequence['Ability']:

    def eruption(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = JoueurDeCetteCarte(effect)
        degats = 4
        if joueur is not None and EnergieEnMain(joueur) >= 2:
            degats += 2
        this.DealDamage(effect.targets, degats, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            eruption,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
