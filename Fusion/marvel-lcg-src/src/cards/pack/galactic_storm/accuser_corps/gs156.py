from . import *

# * The Accused — ATTACHEMENT (Accuser Corps), unique. CONDITION. 1 etoile + 1 icone de boost.
# Attach to your identity.
# Forced Interrupt: When an enemy initiates an attack against the attached identity, that enemy gets
#   +1 ATK for that attack.
# Forced Response: After an ACCUSER CORPS enemy is defeated, discard this card.
# [star] Boost: Attach to your identity.
#
# Cartes de reference :
#  - « Attach to your identity » : `AttachToFaceWhenPutIntoPlay("YourIdentity")`, modele baxter_stockman
#    tx018 In the Crosshairs (sic, Intruder Alert!).
#  - « When an enemy initiates an attack against X, that enemy gets +1 ATK for that attack » :
#    `WhenUnitWouldAttack` + `message.GainATKForThisAttack(1, effect)`, modele OFFICIEL cw 56017 Savage
#    Strike / aoa 45041, restreint au joueur attache via `message.against_player`.
#  - « After an ACCUSER CORPS enemy is defeated, discard this card » : `WhenUnitBeDefeated(ForcedResponse,
#    CardFinder(trait="ACCUSER CORPS"), ...)` + `Faces.DiscardAll([effect.this], effect)`.
#  - « Boost: Attach to your identity » : `AttachTo2` depuis un handler `WhenCardBecomeBoost`, modele
#    gs144 (meme pack Galactic Storm, meme idee d'attache au moment du Boost).
#
# ⚠ Mots-pieges : « the ATTACHED identity » (le joueur sur qui est posee CETTE copie, pas n'importe quel
# joueur) ; « ACCUSER CORPS enemy » = trait, pas nom de carte precis (vise aussi bien Kree Accuser que tout
# futur ennemi du trait) ; le Forced Response se declenche meme si la carte n'a jamais ete utilisee.


def GetAbilities() -> Sequence['Ability']:

    def interrupt_attaque(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        attache = getattr(effect.this, 'bind_face', None)
        joueur = attache.GetControlByPlayer() if attache is not None else None
        if joueur is not None and message.against_player is joueur:
            message.GainATKForThisAttack(1, effect)

    def accuser_corps_vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Unused(message)
        Faces.DiscardAll([effect.this], effect)

    def booster(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = JoueurVise(effect, message)
        if joueur is not None:
            effect.this.CastTo(Attachment).AttachTo2(joueur.GetIdentity(), effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, Enemy, interrupt_attaque),
        AbilityFactory.WhenUnitBeDefeated(AbilityType.ForcedResponse, CardFinder(trait="ACCUSER CORPS"), accuser_corps_vaincu),
        AbilityFactory.WhenCardBecomeBoost("This", booster),
    ]
