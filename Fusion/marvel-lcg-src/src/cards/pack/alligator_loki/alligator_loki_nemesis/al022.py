from . import *

# * Frogjolnir — attachement nemesis. WEAPON. Boost 3, SCH+1, ATK+1 (`desc`).
# Mis de cote a la mise en place, melange dans le deck de rencontre par
# Time Out (al017).
# If Throg is not in play, find him and reveal him. Attach this card to Throg.
#   Then, Throg activates against you.
# Throg gains the [[AERIAL]] trait.
# [star] Forced Response: After Throg attacks you, take 1 indirect damage.
#
# Cartes de reference :
#  - 42027 * Harpoon's Harpoon (nemesis d'Angel) : le calque exact.
#    `AttachToFaceWhenPutIntoPlay(CardFinder(...), if_cannot_operation=)` :
#    Throg en jeu -> le moteur attache tout seul ; sinon la branche
#    `if_cannot_operation` va le chercher, le revele et attache a la main.
#    Et `AfterUnitAttackYou(ForcedResponse, ..., op)` +
#    `identity.TakeIndirectDamage(this, N, effect)` pour la reponse forcee ;
#  - 45164 Agent of Apocalypse : « activates against you » ->
#    `minion.DoActivate(player, effect)` ;
#  - « find him » -> `Find.Find` (find.py:97), la regle officielle du « find »
#    (toutes les zones sauf le tableau des victoires et le hors-jeu) ;
#  - `GiveKeywordToAttached(Minion, trait="AERIAL")` pour le trait.
#
# ORDRE D'EXECUTION (attachment.py:14-22) : a la revelation, le moteur
# appelle d'abord `PutIntoPlay` (donc l'attache, ou `if_cannot_operation`),
# PUIS les « When Revealed » de la carte. « Then, Throg activates against
# you » est donc porte par un `WhenThisRevealed`, qui recoit le joueur cible
# (`message.GetToPlayer()`) et tourne apres l'attache, dans les deux
# branches. Si l'attache a echoue, la carte est deja defaussee et
# `WhenThisRevealed` ne tourne pas (attachment.py:19-20) : pas d'activation.
#
# ⚠ « THROG » = al019, le sbire nemesis, par `card_ids` partout : le Throg
# de joueur al002 est un sbire AMI, Frogjolnir ne s'y attache pas (l'auteur
# donne le marteau au Throg ennemi ; et al019 chasse al002 en entrant).
# ⚠ Throg introuvable (hors jeu) : la carte ne fait rien et part a la
# defausse, regle generale des attachements sans cible. Pas de Surge ici.
# ⚠ La Forced Response vise Throg « attacks YOU » : un Throg qui attaque un
# autre joueur ne blesse pas celui-ci. `AfterUnitAttackYou` le garantit.

THROG_NEMESIS = ["al019"]


def GetAbilities() -> Sequence['Ability']:

    def trouver_et_attacher(effect: 'Effect', joueur: 'Player') -> None:
        this = effect.this.CastTo(Attachment)
        throg = Find.Find(effect, card_ids=THROG_NEMESIS, card_type=Minion)
        if throg is None:
            return
        if not throg.IsInPlay():
            throg.Reveal(joueur, effect)
        if throg.card.IsOnField():
            this.AttachTo2(throg, effect)

    def throg_active(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.GetToPlayer()
        throg = this.bind_face
        if joueur is None or throg is None or not throg.card.IsOnField():
            return
        if Minion.IsType(throg):
            throg.CastTo(Minion).DoActivate(joueur, effect)

    def frogjolnir(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.GetAgainstPlayer()
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is not None:
            identite.TakeIndirectDamage(this, 1, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(card_ids=THROG_NEMESIS),
            if_cannot_operation=trouver_et_attacher,
        ),
        AbilityFactory.WhenThisRevealed(
            None,
            throg_active,
        ),
        *AbilityFactory.GiveKeywordToAttached(
            Minion,
            trait="AERIAL",
        ),
        AbilityFactory.AfterUnitAttackYou(
            AbilityType.ForcedResponse,
            "AttachedMinion",
            frogjolnir,
        ),
    ]
