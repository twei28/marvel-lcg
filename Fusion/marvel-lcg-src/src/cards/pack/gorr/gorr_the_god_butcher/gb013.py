from . import *

# Umbral Wings — ATTACHEMENT NECROVERSE. 3 icones de boost.
#
# Attach to Gorr the God Butcher.
# Forced Interrupt: When Gorr the God Butcher is dealt damage, reduce that
#   damage by 1.
# Hero Action: Discard 2 cards from your hand and the top 2 cards of your deck
#   → discard this card.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - Reduction de degats : 26015 (Victor Mancha, pack vision) — fabrique
#   `WhenUnitWouldTakeDamage` puis `message.ReduceDamage(1, effect)`. Victor
#   se protege lui-meme (`"This"`) et seulement contre les attaques
#   (`is_from_attack=True`) ; ici on protege une AUTRE unite, nommee, contre
#   TOUS les degats : `CardFinder(name=...)` et pas de `is_from_attack`.
# - Attachement pose sur un ennemi nomme et action qui le defausse : 07020
#   (Ball and Chain), meme squelette qu'en gb012.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « IS DEALT damage » -> tous les degats, d'ou qu'ils viennent (attaque,
#   evenement, degats indirects), pas seulement les attaques.
# « REDUCE that damage BY 1 » -> reduction, pas annulation : 1 degat devient
#   0, 3 deviennent 2.
# « Discard 2 cards FROM YOUR HAND AND the top 2 cards of YOUR DECK » -> un
#   cout a DEUX parties, toutes deux obligatoires (piege « and remove »).
#   Contrairement a gb012 et gb014, la defausse de main n'est PAS aleatoire :
#   le joueur choisit ses deux cartes.


def GetAbilities() -> Sequence['Ability']:

    def ailes_d_ombre(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(this)

        message.ReduceDamage(1, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(name=NOM_GORR)
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt,
            CardFinder(name=NOM_GORR),
            ailes_d_ombre,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCostFunc(CostFunc.Discard("YourHandCards", range=(2, 2)))
        .SetCostFunc(CostFunc.DiscardDeckTopCards("YourDeck", 2)),
    ]
