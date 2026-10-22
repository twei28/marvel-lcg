from . import *

# Pull of Power — ATTACHEMENT. SPELL. CTR +2★, Boost 2.
# When Revealed : You may attach this card to your identity. If you do not, take 4 damage, confuse your identity, remove 1 corruption counter from your Creeping Corruption, and discard
#   this card.
# [star] Forced Response : After attached hero makes a basic thwart, place 1 corruption counter on your Creeping Corruption.
#
# Cartes de reference : sl064 (meme structure, face au contrat sl064), sm/shield_tech (`AfterUnitMakeThwart(.., is_basic_thwart=True)` : voir l'usage dans thwart.py), sl011 (`GiveStatus(.., "Confused")`).
# ⚠ Mots-pieges : « CONFUSE » (pas « stun ») ; « basic THWART » : le pouvoir de base de contre, pas une capacite ni un evenement ; reste identique a sl064.


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
        Faces.GiveStatus([identite], "Confused", effect)
        RetirerCorruption(effect, joueur)
        Faces.DiscardAll([this], effect)

    def apres_contre(effect: 'Effect', message: 'Message.AfterUnitThwartEnd') -> None:
        porteur = effect.this.CastTo(Attachment).bind_face
        joueur = porteur.GetControlByPlayer() if porteur is not None else None
        if joueur is not None:
            PlacerCorruption(effect, joueur)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.AfterUnitMakeThwart(AbilityType.ForcedResponse, "AttachedHero", apres_contre, is_basic_thwart=True),
    ]
