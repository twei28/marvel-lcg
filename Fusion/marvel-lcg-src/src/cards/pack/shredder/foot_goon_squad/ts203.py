from . import *

# * Hun — SBIRE UNIQUE (Foot Goon Squad). BRUTE. FOOT CLAN.
# MNG 1 / ATQ 2 / PV 3, 1 icone de boost + etoile. Toughness.
# Forced Response: After Hun attacks and damages a character, stun that character.
# [star] Boost: If this activation deals damage to a character, stun that character.
#
# Cartes de reference : `gob 02038` Scorpion (le Response) ; `thor 06029` Frost
# Giant (boost « if this attack deals damage to a character, stun that character » ;
# ici `IfUnitTakeDamageFromThisAttack`, voir le commentaire dans le script).
#
# Mots-pieges : « IF THIS ACTIVATION deals damage » : une manigance n'en inflige
# pas (le boost ne fait alors rien) ; « a character » (identite ou allie,
# pas seulement vous) ; Toughness lu dans `desc`.


def GetAbilities() -> Sequence['Ability']:

    def blesse(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        Faces.GiveStatus([message.attacked], "Stunned", effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        # `IfUnitTakeDamageFromThisAttack` (degats REELLEMENT subis) et non
        # `IfThisAttackDealDamage` (modele thor 06029) : ce dernier lit les degats
        # CALCULES de l'attaque, y compris ceux qu'une carte Tenace absorbe, et
        # etourdissait malgre la Tenace (cas « ts203 Boost, TEMOIN »).
        message.would_atk_message.IfUnitTakeDamageFromThisAttack(
            lambda unites: Faces.GiveStatus(unites, "Stunned", effect),
            effect,
        )

    return [
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.ForcedResponse, "This", "Character", blesse, target_in_play=True,
        ),
        AbilityFactory.WhenCardBecomeBoost("This", boost, during_attack=True),
    ]
