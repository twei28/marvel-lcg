from . import *

# Disabled — TRAITRISE NEMESIS, boost ETOILE.
# When Revealed: Exhaust each [[HACKED]] upgrade under your control. If you
#   cannot, search the encounter deck and discard pile for the Rogue Asset side
#   scheme and put it into play. If Rogue Asset is already in play, stun your
#   identity.
# [star] Boost: Stun your identity.
#
# Cartes de reference :
#  - `01095` Rhino : `Search.EncounterCard(..., include_discard_pile=True,
#    name=..., card_type=SchemeSide2)`. Rhino REVELE la manigance ; ici on la
#    MET EN JEU, ce qui n'est pas la meme chose (pas de « When Revealed »).
#  - `05029` Harvest : incliner toutes les cartes d'une famille d'un coup.
#  - `wd014` Get Shocked! : `Faces.GiveStatus([identite], "Stunned", effect)`
#    et la forme `WhenCardBecomeBoost` pour le boost etoile.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **If you cannot** » : le repli ne se declenche que si AUCUNE
#    amelioration HACKED n'a pu etre inclinee. Une seule qui s'incline suffit a
#    fermer la porte, meme si les autres etaient deja inclinees.
#  - Les ameliorations HACKED n'existent QUE si Rogue Asset (`st016`) est en
#    jeu. Cette carte est donc, la plupart du temps, une carte qui POSE Rogue
#    Asset — et qui devient punitive une fois qu'elle y est.
#  - « **under your control** » : le joueur qui revele, pas tous les joueurs.
#  - Le boost est ETOILE : pas de valeur numerique dans `desc`, une capacite
#    `WhenCardBecomeBoost` a la place (verifie contre `01144a`).


def GetAbilities() -> Sequence['Ability']:

    def assommer(joueur: 'Player', effect: 'Effect') -> None:
        Faces.GiveStatus([joueur.GetIdentity()], "Stunned", effect)

    def disabled(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()
        if joueur is None:
            return

        piratees = [f for f in joueur.GetControlUpgrade()
                    if f.HasTrait(TRAIT_HACKED)]
        if Faces.ExhaustAll(piratees, effect):
            return

        deja_en_jeu = Worlds.FindCardOnField(
            effect, name=NOM_ROGUE_ASSET, card_type=SchemeSide2)
        if deja_en_jeu is not None:
            assommer(joueur, effect)
            return

        face = Search.EncounterCard(
            effect,
            include_discard_pile=True,
            name=NOM_ROGUE_ASSET,
            card_type=SchemeSide2,
        )
        if face:
            face.PutIntoPlay(joueur, effect)
        else:
            assommer(joueur, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        if joueur is not None:
            assommer(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            disabled,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost,
        ),
    ]
