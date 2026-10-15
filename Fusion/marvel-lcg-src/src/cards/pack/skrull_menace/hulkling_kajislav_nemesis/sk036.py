from . import *

# Swapping Roles — TRAITRISE nemesis de Hulkling (n° 36, 5/5). 1 icone boost
# + ★ (capacite de Boost).
# When Revealed: Exhaust each card you control that shares a [[TRAIT]] with
#   your identity (including your identity).
# ★ Boost: Exhaust each card you control that shares a [[TRAIT]] with your
#   identity (except for your identity).
#
# Cartes de reference :
#  - `39014b` pour `WhenThisRevealed(None, op)`.
#  - **`mf016`** / `27080` Lashing Out : la capacite ★ Boost =
#    `WhenCardBecomeBoost("This", op)`, joueur par `message.GetToPlayer()`.
#  - `40160` Manufactured Drama pour `Faces.ExhaustAll(...)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « each card **you control** » : allies, ameliorations, soutiens, identite
#    (`GetControlCards`, sans les attachements rencontre).
#  - « shares **a** TRAIT with your identity » : un trait commun avec
#    l'identite ACTUELLE.
#  - Revelation : identite COMPRISE ; Boost : identite EXCLUE. Seule
#    difference entre les deux textes.
#  - L'identite partage forcement un trait avec elle-meme : en revelation elle
#    est toujours inclinee.


def _incliner(effect: 'Effect', joueur: 'Player', avec_identite: bool) -> None:
    identite = joueur.GetIdentity()
    cartes = [
        f for f in joueur.GetControlCards()
        if f is not None and identite is not None and identite.ShareTrait(f)
        and (avec_identite or f != identite)
    ]
    if avec_identite and identite is not None and identite not in cartes:
        cartes.append(identite)
    Faces.ExhaustAll(cartes, effect)


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        _incliner(effect, message.GetToPlayer(), avec_identite=True)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        _incliner(effect, message.GetToPlayer(), avec_identite=False)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost,
        ),
    ]
