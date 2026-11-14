from . import *

# * The Silver Surfboard — Upgrade, cout 0, ressource [wild]. AERIAL. COSMIC. VEHICLE.
# Hero Action: Exhaust The Silver Surfboard -> ready Silver Surfer.
# Interrupt: When you discard The Silver Surfboard, deal 1 damage to Silver Surfer -> draw a card.
#
# Cartes de reference :
#  - `tg001a` * Throg : « ready Throg » = `Faces.ReadyAll(effect.targets)` avec `.SetTarget("YourHero")`.
#  - `01027` Focused Rage : « take 1 damage -> draw 1 card », meme cout `CostFunc.TakeDamage` puis `DrawUp(1)`.
#  - `intensified.py` / `WhenCardWouldDiscard` : fenetre « When X would be discarded ».
#
# ⚠ Mots-pieges :
#  - « Silver Surfer » = la face HEROS : en alter-ego (Norrin Radd) il n'y a personne a blesser ni a redresser,
#    le cout de l'Interruption n'est alors pas payable (lecture litterale).
#  - « When YOU discard » : l'amelioration est en jeu ; une Interruption n'existe que depuis le jeu.
#  - « deal 1 damage to Silver Surfer -> » : AVANT la fleche, donc un COUT.
#  - Pas de limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def planche(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        Faces.ReadyAll(effect.targets, effect)

    def repiocher(effect: 'Effect', message: 'Message.WhenCardWouldDiscard') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is not None:
            joueur.DrawUp(1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            planche,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget("YourHero"),
        AbilityFactory.WhenCardWouldDiscard(
            AbilityType.Interrupt,
            "This",
            repiocher,
            conditions=[
                lambda effect, message: effect.this.IsInPlay(),
            ],
        ).SetCostFunc(CostFunc.DealDamage(1, "YourHero")),
    ]
