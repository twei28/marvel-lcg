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

        # CORRECTIF : `ChooseAbilities` + `Select.From(faces=...)` ne
        # restreignait RIEN sur des cartes hors jeu : le choix tombait sur la
        # MANIGANCE PRINCIPALE, qui partait dans la main de Lockjaw puis dans
        # la defausse. Plus de manigance, donc IndexError a la fin de partie.
        choisie = initiator.AskChooseFace(
            candidats,
            effect,
            prompt="Add a non-resource card from a discard pile to its owner's hand",
        )
        if choisie is None:
            return

        from game.player import Player
        # CORRECTIF (4/8/2026) : `GetOwner` peut rendre le SCENARIO (cartes
        # cote Rencontre), pas un joueur.
        proprietaire = choisie.GetOwner()
        if not isinstance(proprietaire, Player):
            proprietaire = initiator
        proprietaire.GainCard(choisie, effect)

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
