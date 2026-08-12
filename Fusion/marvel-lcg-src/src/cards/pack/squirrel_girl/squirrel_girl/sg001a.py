from . import *

# Squirrel Girl
# Unbeatable Army — Hero Response: After you spend a Squirrel, either deal
#   1 damage to an enemy or remove 1 threat from a scheme. Limit once per phase.
#
# Le declencheur est le message moteur WhenCardBeSpendAsResource, envoye juste
# apres la depense : c'est le seul moment ou « depenser un ecureuil » existe
# pour le moteur (voir CapaciteDepense dans __init__.py).

def GetAbilities() -> Sequence['Ability']:

    def unbeatable_army(effect: 'Effect', message: 'Message.WhenCardBeSpendAsResource') -> None:
        this = effect.this.CastTo(Hero)
        joueur = effect.GetInitiator()

        ennemis = list(Worlds.FindCardsOnField(effect, card_type=Enemy))
        manigances = list(Worlds.FindCardsOnField(effect, card_type=Scheme2))

        choix: List['Ability'] = []
        if ennemis:
            choix.append(
                AbilityFactory.ForChoiceAbility(
                    "Deal 1 damage to an enemy",
                    lambda targets: this.DealDamage(list(targets), 1, effect),
                ).SetTarget(Select.From(faces=ennemis), range=(1, 1)))
        if manigances:
            choix.append(
                AbilityFactory.ForChoiceAbility(
                    "Remove 1 threat from a scheme",
                    lambda targets: this.RemoveThreatFromSchemes(list(targets), 1, effect),
                ).SetTarget(Select.From(faces=manigances), range=(1, 1)))

        if choix:
            joueur.ChooseAbilities(effect, *choix)

    def est_une_depense_d_ecureuil(effect: 'Effect',
                                   message: 'Message.WhenCardBeSpendAsResource') -> bool:
        # La ressource est desormais generee par l'IDENTITE, dont le cout est
        # de defausser un ecureuil : le declencheur du message n'est donc plus
        # l'ecureuil lui-meme, c'est la marque de depense qui le designe.
        return EcureuilDepense(effect) is not None

    return [
        # « Squirrel Aid » : la source de paiement unique du set. Portee par les
        # DEUX faces d'identite, une seule etant en jeu a la fois.
        CapaciteDepenseIdentite(),
        (AbilityFactory.AfterGenerateResources(
            AbilityType.HeroResponse,
            "You",
            unbeatable_army,
            conditions=[est_une_depense_d_ecureuil],
        )
            .SetName("Unbeatable Army")
            .LimitOncePerPhase()),
    ]
