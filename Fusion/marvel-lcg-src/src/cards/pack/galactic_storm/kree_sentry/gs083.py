from . import *

# Optic Blast Cannon — ATTACHEMENT (Kree Sentry). WEAPON. Badge +1[star] ATK. 1 icone de boost.
# Attach to Kree Sentry.
# [star] Kree Sentry's attacks gain piercing and ranged.
# Hero Action: Spend [physical][physical] resources → discard this card.
# [star] Boost: If this activation is an attack, it gains piercing and ranged.
#
# Cartes de reference :
#  - badge « +1 ATK » : BASE AUTOMATIQUE `desc.ATK+` (l'etoile renvoie au texte, convention Skrull Menace), comme gs129.
#  - « Attach to Kree Sentry » : `AttachToFaceWhenPutIntoPlay(CardFinder(name=..))`, modele gs129.
#  - « Kree Sentry's attacks gain piercing and ranged » : `UnitAttackGainKeyword("AttachedCharacter", ..)`, modele OFFICIEL 27147
#    Arm Cannon (repris par gs129). Les attaques de Kree Sentry contre un sbire ou un allie (briques communes) le lisent
#    aussi : meme chemin `AttackProperty`.
#  - Boost : `message.would_atk_message.Gain...`, modele OFFICIEL 50160 Supersonic, sous `getattr(.., None)` (pas d'attaque
#    en cours = activation de manigance, rien).
#  - « Hero Action: Spend [physical][physical] resources → discard this card » : `PlayerActionToDiscardThis(HeroAction)`
#    + `SetCost(Cost("RR"))`, modele OFFICIEL 01118 Sonic Converter ; icones de ressource (deux poings) = [physical],
#    verifiees par decoupe contre sk148 / sk152 (ressource R declaree), gabarit KREE-SENTRY-GABARITS.md.
#
# ⚠ Mots-pieges : « IF this activation is an attack » (rien sur une manigance) ; le boost ne donne QUE piercing and ranged ;
# « Kree Sentry's attacks » = les attaques de CE mechant, pas celles d'un sbire.


def GetAbilities() -> Sequence['Ability']:

    def booster(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        attaque = getattr(message, "would_atk_message", None)
        if attaque is not None:
            attaque.GainPiercing(effect)
            attaque.GainRanged(effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name=SENTRY, card_type=Villain)),
        AbilityFactory.UnitAttackGainKeyword("AttachedCharacter", piercing=True, ranged=True),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction).SetCost(Cost("RR")),
        AbilityFactory.WhenCardBecomeBoost("This", booster),
    ]
