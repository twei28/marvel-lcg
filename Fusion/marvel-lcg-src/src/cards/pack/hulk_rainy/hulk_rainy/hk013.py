from . import *

# Inner Conflict — OBLIGATION du pack, x1.
# Give to the Bruce Banner player.
# Change form (flip your identity). Then:
# • If you are Bruce Banner, discard 1 random card from your hand. Discard
#   this obligation.
# • If you are Hulk, exhaust your hero. Discard this obligation.
#
# Carte de reference : `10025` Inner Demons, l'obligation du HULK OFFICIEL,
# au mot pres a deux details : elle defausse 2 cartes CHOISIES la, 1 carte au
# HASARD ici.
#
# ⚠ LE PIEGE, ET IL A SES DEUX CAS DE TEST : relire la face APRES
# `ChangeToOtherIdentityForm`. `identity.card.face` avant la bascule rend la
# face de DEPART, et les deux branches testeraient alors le nom d'AVANT —
# c'est-a-dire exactement l'inverse de ce que la carte demande. On repart
# donc de `identity.card.face` une fois la bascule faite, comme 10025.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « Change form » est INCONDITIONNEL et vient EN PREMIER : la bascule
#    n'est pas un choix, et c'est elle qui decide de la branche.
#  - Cette bascule declenche hk009 The Other Guy, qui recompense chaque
#    changement de forme : l'obligation donne donc quelque chose au joueur
#    qui a pose son soutien.
#  - « 1 RANDOM card » : `DiscardRandomHandCards(1, effect)`, pas
#    `DiscardHandCards`, qui laisserait le joueur choisir.
#  - « exhaust your HERO » : la face heros seule, pas les allies.
#  - Les deux branches defaussent l'obligation. Aucune ne la remet en jeu.
#  - En civil, la main est deja de 6 cartes : la defausse aleatoire tombe
#    apres la bascule, donc sur la main du moment.


def GetAbilities() -> Sequence['Ability']:

    def inner_conflict(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        player = message.GetGaveToPlayer()
        if player is None:
            return

        identity = player.GetIdentity()
        identity.ChangeToOtherIdentityForm(effect)

        # ⚠ Relecture APRES la bascule : c'est la face d'ARRIVEE qui decide.
        face = identity.card.face

        if face.IsName("Bruce Banner"):
            player.DiscardRandomHandCards(1, effect)
            Faces.DiscardAll([this], effect)
        elif face.IsName("Hulk"):
            Faces.ExhaustAll([face], effect)
            Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            inner_conflict
        ),
    ]
