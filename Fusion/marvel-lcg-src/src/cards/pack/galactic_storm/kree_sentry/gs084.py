from . import *

# Repulsor Blast Unit — ATTACHEMENT (Kree Sentry). WEAPON. Badge +1[star] ATK. 1 icone de boost.
# Attach to Kree Sentry.
# [star] Kree Sentry's attacks gain overkill and ranged.
# [star] Boost: If this activation is an attack, it gains overkill.
# Forced Interrupt: When Sentry's Grasp would be set aside, if there is 5 or more damage on it, discard Repulsor
#   Blast Unit.
#
# Cartes de reference :
#  - badge « +1 ATK » : BASE AUTOMATIQUE `desc.ATK+` (l'etoile renvoie au texte, convention Skrull Menace), comme gs129.
#  - « Attach to Kree Sentry » : `AttachToFaceWhenPutIntoPlay(CardFinder(name=..))`, modele gs129.
#  - « Kree Sentry's attacks gain overkill and ranged » : `UnitAttackGainKeyword("AttachedCharacter", ..)`, modele OFFICIEL 27147
#    Arm Cannon (repris par gs129). Les attaques de Kree Sentry contre un sbire ou un allie (briques communes) le lisent
#    aussi : meme chemin `AttackProperty`.
#  - Boost : `message.would_atk_message.Gain...`, modele OFFICIEL 50160 Supersonic, sous `getattr(.., None)` (pas d'attaque
#    en cours = activation de manigance, rien).
#  - Forced Interrupt « When Sentry's Grasp would be set aside, if there is 5 or more damage on it » : le moteur n'a
#    pas de message « mis de cote » ; une Poigne qui est mise de cote QUITTE LE JEU, on ecoute donc
#    `WhenCardWouldLeavePlay` de la Poigne (modele gs082 pour l'interruption de depart) avec la condition « 5 degats
#    ou plus sur elle » ; la defausse de Repulsor = `Faces.DiscardAll([this])`.
#
# ⚠ Mots-pieges : « IF this activation is an attack » (rien sur une manigance) ; le boost ne donne QUE overkill ;
# « Kree Sentry's attacks » = les attaques de CE mechant, pas celles d'un sbire.


def GetAbilities() -> Sequence['Ability']:

    def booster(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        attaque = getattr(message, "would_atk_message", None)
        if attaque is not None:
            attaque.GainOverKill(effect)

    def poigne_a_cinq_degats(effect: 'Effect', message: 'Message.WhenCardWouldLeavePlay') -> bool:
        return message.trigger.IsInPlay() and message.trigger.GetCounters('damage') >= 5

    def defausser(effect: 'Effect', message: 'Message.WhenCardWouldLeavePlay') -> None:
        Unused(message)
        Faces.DiscardAll([effect.this], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name=SENTRY, card_type=Villain)),
        AbilityFactory.UnitAttackGainKeyword("AttachedCharacter", overkill=True, ranged=True),
        AbilityFactory.WhenCardWouldLeavePlay(
            AbilityType.ForcedInterrupt,
            CardFinder(name=GRASP, card_type=Attachment),
            defausser,
            conditions=[poigne_a_cinq_degats],
        ),
        AbilityFactory.WhenCardBecomeBoost("This", booster),
    ]
