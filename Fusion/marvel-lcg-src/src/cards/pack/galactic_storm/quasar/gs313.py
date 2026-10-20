from . import *

# Quantum Absorption — amelioration signature (QUASAR 13/16). SUPERPOWER.
# Cout 1, [wild].
# Hero Interrupt: When you pay for a DEFENSE event with Quantum Bands, heal 2
#   damage from Quasar.
#
# Cartes de reference :
#  - **`32047`** Aggressive Energy / `34020` Passion for Justice : capacite qui
#    s'ouvre AU PAIEMENT d'un evenement d'un trait donne
#    (`Message.WhenCardBeSpendAsResource`, `message.pay_for_card`) ; ici la
#    carte qui paie est Quantum Bands (en jeu), d'ou la fabrique
#    `AfterGenerateResources` (helper `QuandLesBandesPaient`).
#  - `sk001b` / `47012` pour `this.HealthUnits([identite], n, effect)`.
#  - `CanPlayThisUpgradeCard()` : amelioration posee devant le joueur (sk013).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « When you PAY FOR a [[DEFENSE]] EVENT » : un evenement portant le trait
#    DEFENSE (Unbreakable Guard, Desperate Defense...), pas une amelioration ni
#    une capacite de defense d'une carte en jeu.
#  - « WITH QUANTUM BANDS » : seulement quand les Bandes font partie du
#    paiement ; une autre ressource ne declenche rien.
#  - « heal 2 damage from **Quasar** » : l'identite, en forme heros
#    (Hero Interrupt). Facultative (Interrupt).


def GetAbilities() -> Sequence['Ability']:

    def absorber(effect: 'Effect', message: 'Message.WhenCardBeSpendAsResource') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        this.HealthUnits([joueur.GetIdentity()], 2, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        QuandLesBandesPaient(
            AbilityType.HeroInterrupt,
            CardFinder2("DEFENSE", Event),
            absorber,
        ),
    ]
