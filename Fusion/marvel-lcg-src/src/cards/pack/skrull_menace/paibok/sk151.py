from . import *

# Metallic Skin — ATTACHEMENT (Paibok). POWER SKRULL. ATQ +1, boost 1 + etoile.
# Attach to Paibok.
# Forced Response: After Paibok takes damage, give him a tough status card.
# Hero Action: Spend [energy][mental] resources → discard this card.
# [star] Boost: Give Paibok a tough status card.
#
# Cartes de reference :
#  - Reponse apres degats : `AbilityFactory.AfterUnitTookDamage` (damage.py:91 ; condition native
#    `took_damage > 0` = « takes damage ») ; statut : `Faces.GiveStatus([unit], "Tough", effect)`
#    (recette « Etourdir / robuste », 05015/01083).
#  - Attache + defausse : `01100` ; Boost : `WhenCardBecomeBoost("This", ...)` (`04136`).
#
# ⚠ Mots-pieges : « After PAIBOK takes damage » (l'hote, tout degat : attaque ou non) ; un Paibok deja
# Robuste n'en recoit pas un second (un seul statut Robuste par personnage) ; « give HIM » = Paibok,
# pas le joueur ; cout `[energy][mental]` = `YB` (verifie contre sk044 / sk057, meme auteur).


def GetAbilities() -> Sequence['Ability']:

    def robuste(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        Faces.GiveStatus([message.trigger], "Tough", effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Unused(message)
        paibok = PaibokEnJeu(effect)
        if paibok is not None:
            Faces.GiveStatus([paibok], "Tough", effect)

    return [
        AttacherAPaibok(),
        AbilityFactory.AfterUnitTookDamage(AbilityType.ForcedResponse, "AttachedEnemy", robuste),
        ActionDefausserPouvoir(Cost("YB")),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
