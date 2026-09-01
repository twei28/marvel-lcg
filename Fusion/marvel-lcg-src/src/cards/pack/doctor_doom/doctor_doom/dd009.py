from . import *

# * Doom's Time Platform — amelioration signature. TECH. Cout 2.
# Hero Action: Exhaust Doom's Time Platform -> choose:
#  • Ready Doctor Doom.
#  • Shuffle 1 event or upgrade from your discard pile back into your deck.
#
# Cartes de reference :
#  - choix a deux branches : aa014 Chaotic Forces / an010,
#    `player.ChooseAbilities(effect, ForChoiceAbility(...), ForChoiceAbility(...))`
#    (recette moteur §2 : le pilote prend la PREMIERE branche) ;
#  - redressement de l'identite : an001a Frenzy, `Faces.ReadyAll` ;
#  - remise en deck depuis la defausse : `Faces.ShuffleAllTo(faces,
#    player.player_deck, effect)` (faces.py:48), comme bt001b.
#
# ⚠ « 1 event OR upgrade » : les deux types, d'ou le filtre `Event|Upgrade`.
# ⚠ La seconde branche n'est proposee que si la defausse contient vraiment une
# telle carte, sinon le joueur inclinerait le soutien pour rien.

def GetAbilities() -> Sequence['Ability']:

    def time_platform(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        def candidats() -> List['CardFace']:
            return [f for f in initiator.discard_pile.Get(True)
                    if Event.IsType(f) or Upgrade.IsType(f)]

        def redresser(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            hero = initiator.GetHero()
            if hero is not None:
                Faces.ReadyAll([hero], effect)

        def remelanger(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            faces = candidats()
            if not faces:
                return
            choisie = initiator.AskChooseFace(faces, effect)
            if choisie:
                Faces.ShuffleAllTo([choisie], initiator.player_deck, effect)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Ready Doctor Doom", redresser),
            AbilityFactory.ForChoiceAbility(
                "Shuffle 1 event or upgrade from your discard pile back into your deck",
                remelanger,
                condition=len(candidats()) > 0,
            ),
        )

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            time_platform,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
