from . import *

# History with the Hand — AMELIORATION, cout 0, [mental]. CONDITION. x1 (Elektra 14/15).
# Prerequisite (hero form).
# You get +1 hand size.
# Forced Response: After you change form, discard this card.
#
# CARTES DE REFERENCE
#  - Prerequisite : fiche `mots-cles/prerequisite.md` (lecture codee : la carte ne se JOUE qu'en forme heros) ; `CanPlayThisUpgradeCard
#    (conditions=[...])` (play.py:76).
#  - « +1 hand size » sur l'amelioration : `mister_fantastic/mf005` (`GiveKeywordToAttached(CardFinder(name=..., card_type=Hero),
#    hand_size=1)`).
#  - « After you change form, discard this card » : `AfterUnitChangeForm(ForcedResponse, "You", op)` (form.py:81), `Faces.DiscardAll`.
#
# TEXTE CONTRE CODE
#  ⚠ « Prerequisite (hero form) » : une condition de JEU, pas de maintien : en alter-ego la carte ne se joue pas ; une fois posee, c'est la
#    Reponse forcee qui la retire au premier changement de forme.
#  ⚠ « After you change form » : n'importe quel changement (heros -> alter-ego ou l'inverse), c'est une Reponse FORCEE, donc obligatoire.
#  ⚠ « +1 hand size » : la taille de main du JOUEUR (5 en forme heros -> 6), via le mot-cle `hand_size` de l'identite.
#  Chiffres : cout 0, +1 taille de main.


def GetAbilities() -> Sequence['Ability']:

    def en_forme_heros(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        return joueur is not None and joueur.IsHero()

    def defausser(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        Unused(message)
        Faces.DiscardAll([effect.this], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(conditions=[en_forme_heros]),
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Elektra", card_type=Hero),
            hand_size=1,
        ),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.ForcedResponse,
            "You",
            defausser,
        ),
    ]
