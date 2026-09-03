from . import *

# Impale — evenement signature, x2 (n/15 = 2 et 3).
# ATTACK. SKILL. Cout 3, ressource [physical].
# Hero Action (attack): Deal 6 damage to an enemy. Choose for this attack to
#   gain either overkill or piercing.
#
# Cartes de reference :
#  - `01053` Relentless Assault pour l'evenement d'attaque qui porte un
#    mot-cle par `AttackProperty(...)` ;
#  - `hk003` / `08013` pour le choix a deux branches exclusives par
#    `ChooseAbilities` + deux `ForChoiceAbility`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « either ... or » : les deux branches sont EXCLUSIVES. L'attaque ne gagne
#    jamais les deux mots-cles a la fois, et le choix revient au joueur — d'ou
#    deux `ForChoiceAbility` dans un seul `ChooseAbilities` plutot qu'un
#    `AttackProperty(overkill=True, piercing=True)`.
#  - Le CHOIX se fait avant de connaitre le resultat : on ne peut pas
#    « regarder » les degats puis decider. C'est le comportement du moteur, et
#    c'est celui de la carte.
#  - « to AN ENEMY » : vilain ou sbire, la cible est choisie sur l'abilite.
#  - Les 6 degats sont UNE attaque : une Riposte se declenche une fois, un
#    Tenace absorbe le tout.
#  - Aucun autre mot-cle imprime : ni ranged, ni degat supplementaire.
#  - Le libelle `(attack)` alimente Sonne.


def GetAbilities() -> Sequence['Ability']:

    def impale(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        def frapper(overkill: bool, piercing: bool) -> None:
            this.DealDamage(effect.targets, 6, effect,
                            property=AttackProperty(overkill=overkill,
                                                    piercing=piercing))

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "This attack gains overkill",
                lambda cibles: frapper(True, False),
            ),
            AbilityFactory.ForChoiceAbility(
                "This attack gains piercing",
                lambda cibles: frapper(False, True),
            ),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            impale,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
