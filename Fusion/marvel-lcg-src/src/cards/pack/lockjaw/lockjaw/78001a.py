from . import *

# * Lockjaw (face héros) — custom « Nugget »
# Fetch! — Action: Exhaust Lockjaw and spend a [wild] resource → choose a
#   non-resource card in any players' discard pile and add it to their owner's
#   hand. (Limit once per round.)


def GetAbilities() -> Sequence['Ability']:

    def fetch(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        initiator = effect.GetInitiator()

        candidats: List['CardFace'] = []
        for joueur in Worlds.GetPlayers(effect):
            candidats += [
                x for x in joueur.discard_pile.Get()
                if not Resource.IsType(x)
            ]
        if not candidats:
            return

        def recuperer(targets: Sequence['CardFace']) -> None:
            from game.player import Player
            for face in targets:
                # CORRECTIF (4/8/2026) : `GetOwner` peut rendre le SCENARIO
                # (cartes cote Rencontre), pas un joueur. Le garde `hasattr`
                # laissait passer ce cas et la carte plantait sur
                # « 'Scenario' object has no attribute 'GainCard' ».
                proprietaire = face.GetOwner()
                if not isinstance(proprietaire, Player):
                    proprietaire = initiator
                proprietaire.GainCard(face, effect)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Add a non-resource card from a discard pile to its owner's hand",
                recuperer,
            # CORRECTIF (4/8/2026) : une liste de faces se passe par le
            # parametre nomme `faces`. En premier argument POSITIONNEL, elle
            # atterrit dans `target`, que le moteur utilise comme cle de
            # dictionnaire : « TypeError: unhashable type: 'list' » a chaque
            # usage de la capacite.
            ).SetTarget(Select.From(faces=candidats)),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            fetch,
        ).SetName("Fetch!")
        # CORRECTIF (9/8/2026) : l'icone du texte est une MENTALE, pas un wild.
        # Voir PayeAvecMental pour la verification sur les scans.
        .SetCost(Cost("B"))
        .SetCostFunc(CostFunc.Exhaust("This"))
        .LimitOncePerRound(),
    ]
