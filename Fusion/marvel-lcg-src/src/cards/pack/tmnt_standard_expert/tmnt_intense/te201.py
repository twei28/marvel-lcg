from . import *

# Intense Combatants (TMNT Intense 1/1, Inkwire) — ENVIRONNEMENT optionnel.
#
# « TMNT Standard and Expert only. (This is an optional environment for those
#   wanting additional hijinx.)
#   Permanent. Setup.
#   Forced Interrupt: When a status card would be placed on a character, if that
#   character already has 1 copy of that status card on them, intensify them
#   instead. »
#
# « intensify X » = donner une carte d'etat Intensified a X (decision de
# l'utilisateur, Q2 de .planning/tmnt/shredder-questions.md ; fiches
# mots-cles/intensify.md et intensified.md).
#
# CARTES DE REFERENCE
#  - 56175 Contaminant Immunity / ah006 Gamma Barrier : Interrupt « when ... would
#    be stunned » -> `SetBeInstead` sur la pose, puis un autre effet a la place.
#    Ici la fenetre est `WhenStatusWouldCardPlaceOnAgain` (meme forme, mais
#    ouverte AVANT les plafonds : un second Sonne est refuse par `CanbeStunned`
#    avant `WhenStatusWouldCardPlaceOn`, te201 ne le verrait jamais).
#  - Permanent / Setup : lus dans `desc` par le moteur, aucun code.
#
# TEXTE CONTRE CODE
#  « a status card would be placed on A CHARACTER » : tout personnage (heros,
#    allie, vilain, sbire), ami ou ennemi -> `CardFinder()`.
#  « already has 1 copy of that status card » : au moins un exemplaire du MEME
#    nom (`HasStatus(name)`, teste par le moteur avant d'envoyer la fenetre).
#  « intensify THEM INSTEAD » : la pose est annulee (`SetBeInstead`) et le
#    personnage recoit une Intensified a la place.
#  ⚠ Une Intensified posee sur un porteur qui en a deja une n'est pas
#    « intensifiee » (le moteur n'envoie pas la fenetre pour elle), sans quoi la
#    seconde Intensified boucle sur elle-meme.


def GetAbilities() -> Sequence['Ability']:

    def intensifier(effect: 'Effect', message: 'Message.WhenStatusWouldCardPlaceOnAgain') -> None:
        message.SetBeInstead(effect)
        Intensify(effect, message.trigger)

    return [
        AbilityFactory.WhenUnitWouldBeStatusAgain(
            AbilityType.ForcedInterrupt,
            CardFinder(),
            intensifier,
        ),
    ]
