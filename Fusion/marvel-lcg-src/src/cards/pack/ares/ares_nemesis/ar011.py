from . import *

# Athena's Guidance — MANIGANCE ANNEXE nemesis. Menace 3 par joueur. 2 boost.
# Minions gain quickstrike and toughness.
# [star] Boost: Give the activating enemy an additional boost card.
#
# CARTES DE REFERENCE
#  - `40101` Mutant Slayers : `*GiveKeywordToInPlayWhenApplyThis(
#    CardFinder2(..., Minion), quickstrike=1)`, le bonus continu sur tous les
#    sbires tant que la manigance est en jeu. `environment_helper.py:41`
#    accepte `toughness=` de la meme facon.
#  - `01164` Titania's Fury : `WhenCardBecomeBoost("This", op)` +
#    `message.GiveBoostCardForThisActivation(<face>, 1, effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « MINIONS gain quickstrike and toughness » -> tous les sbires, quel que
#    soit leur joueur, pas le vilain. `toughness` par le mot-cle : un sbire qui
#    ENTRE en jeu recoit sa carte Tenace ; un sbire deja en jeu ne recoit pas
#    de Tenace retroactif, c'est la regle officielle du mot-cle (fiche
#    toughness.md).
#  ⚠ « Give the ACTIVATING enemy an additional boost card » -> la face
#    `message.activating_enemy` (sender_card.py:686), pas le vilain : un sbire
#    qui active avec cette carte en boost recoit la carte, pas Rhino.
#  ⚠ `StartingThreat = "3*"` : par joueur (GUIDE §2), desc, aucun code.


def GetAbilities() -> Sequence['Ability']:

    def carte_de_bonus_en_plus(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)
        ennemi = getattr(message, "activating_enemy", None)
        if ennemi is not None:
            message.GiveBoostCardForThisActivation(ennemi, 1, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(card_type=Minion),
            quickstrike=1,
            toughness=1,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            carte_de_bonus_en_plus,
        ),
    ]
