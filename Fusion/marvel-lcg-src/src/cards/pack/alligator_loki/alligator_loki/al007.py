from . import *

# "See You Later!" — evenement signature, x2 (al007 et al008, toutes deux R).
# THWART. Cout 1.
# Hero Action (thwart): Remove 3 threat from a scheme. Change to alter-ego
#   form. You may shuffle Throg from your discard pile into your deck.
#
# ⚠ al008 n'a PAS de module : `ability_link` vers al007 (database.py:124).
#
# Cartes de reference :
#  - 01085 Chase Them Down : evenement de contre, `SetPlay().SetLabel('thwart')
#    .SetTarget(Scheme2)` et `this.RemoveThreatFromSchemes(effect.targets, N,
#    effect)` ;
#  - ag005 Parting Shots : « change to alter-ego form » ->
#    `joueur.GetIdentity().ChangeToForm(AlterEgo, effect)` ;
#  - al001b (Setup) pour la recherche de Throg par `card_ids`.
#
# ⚠ ORDRE DES TROIS PHRASES, respecte a la lettre. La bascule en alter-ego
# declenche Nap Time (al001b), donc le detachement et la recuperation
# facultative, AVANT qu'on propose le melange de Throg. C'est l'ordre imprime.
#
# ⚠ « Throg » -> al002, le sbire de JOUEUR (le seul qui puisse etre dans TA
# defausse). al019 est une carte de rencontre. Recherche par `card_ids`.
# ⚠ « YOU MAY shuffle » -> facultatif : `MayChooseOneAbility`. Et si Throg
# n'est pas dans la defausse, rien n'est propose.
# ⚠ « Change to alter-ego form » sans « you may » : obligatoire, meme si le
# joueur prefererait rester heros. Deja en alter-ego (impossible pour une
# Hero Action, mais on se protege) : `ChangeToForm` ne fait rien.

def GetAbilities() -> Sequence['Ability']:

    def see_you_later(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        this.RemoveThreatFromSchemes(effect.targets, 3, effect)

        identite = joueur.GetIdentity()
        if identite is not None and joueur.IsHero():
            identite.ChangeToForm(AlterEgo, effect)

        throgs = CardFinder(card_ids=["al002"]).Checks(joueur.discard_pile.Get(True))
        if not throgs:
            return

        def melanger(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            Faces.ShuffleAllTo(throgs[:1], joueur.player_deck, effect)

        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Shuffle Throg from your discard pile into your deck",
                melanger,
            ),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            see_you_later,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
