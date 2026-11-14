from . import *

# Mark of the Wicked — ATTACHEMENT. SPELL. ATQ +2★, Boost 3.
# When Revealed : You may attach this card to your identity. If you do not, take 4 damage, stun your identity, remove 1 corruption counter from your Creeping Corruption, and discard
#   this card.
# [star] Forced Response : After attached hero makes a basic attack, place 1 corruption counter on your Creeping Corruption.
#
# Cartes de reference : hunting_season/trap `PiegeAttachement` (When Revealed « attachez-la a votre identite ou ... » : `ChooseAbilities` + `AttachTo2`), sm/shield_tech/27187a
# (`AfterUnitMakeBasicAttack`), sk153 (`identity.TakeDamage(this, n, effect)`, `GiveStatus`). `ATK+` est lu dans `desc` par `HasModify` (rien a coder).
# ⚠ Mots-pieges : « YOU MAY attach » : FACULTATIF, le joueur peut refuser (alors la branche « If you do not » : 4 degats, identite ETOURDIE, un jeton RETIRE, defausse) ; « stun YOUR IDENTITY » :
#  l'identite du joueur ; « remove 1 corruption counter » : RETIRE (pas pose) ; « attached HERO » : l'identite en forme de HEROS (une attaque de base) ; « BASIC attack » : seulement l'attaque
#  de base, pas un pouvoir ni un evenement ; « YOUR » Creeping Corruption : celle du joueur dont l'identite porte la carte.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.GetToPlayer()
        identite = joueur.GetIdentity()
        attachee = [False]

        def attacher(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            attachee[0] = this.AttachTo2(identite, effect)

        joueur.MayChooseOneAbility(effect, AbilityFactory.ForChoiceAbility("Attach this card to your identity", attacher))
        if attachee[0]:
            return
        identite.TakeDamage(this, 4, effect)
        Faces.GiveStatus([identite], "Stunned", effect)
        RetirerCorruption(effect, joueur)
        Faces.DiscardAll([this], effect)

    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        porteur = effect.this.CastTo(Attachment).bind_face
        joueur = porteur.GetControlByPlayer() if porteur is not None else None
        if joueur is not None:
            PlacerCorruption(effect, joueur)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.AfterUnitMakeBasicAttack(AbilityType.ForcedResponse, "AttachedHero", apres_attaque),
    ]
