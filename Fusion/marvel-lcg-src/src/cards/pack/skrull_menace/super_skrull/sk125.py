from . import *

# Rock Mimicry — ATTACHEMENT (paquet SUPERPOWER). SUPERPOWER. Badge ATK ★ seul.
# Attach to Super-Skrull.
# ★ Forced Interrupt: When Super-Skrull attacks, give him 1 additional boost
#   card for this activation.
# ★ Super-Skrull's attacks gain overkill.
#
# Cartes de reference :
#  - **`60079`** Electric Charge (pack fne) : `WhenUnitWouldAttack(ForcedInterrupt,
#    CardFinder(name=...), op)` + `message.GiveAdditionalBoostCardForThisActivation(1,
#    effect)` (aussi 02020 Hysteria, 60093) ; la meme carte ajoute overkill.
#  - **`50107b`** M.O.D.O.K. / fiche overkill.md : « attacks gain overkill » =
#    `UnitAttackGainKeyword(..., overkill=True)`.
#
# ⚠ Mots-pieges : « When Super-Skrull ATTACKS » (ses attaques, pas ses manigances) ;
# « 1 ADDITIONAL boost card FOR THIS ACTIVATION » ; Interruption obligatoire.
# Le badge ATK a etoile seule est un marqueur « voir le texte », sans valeur
# chiffree (decision utilisateur du 15/10/2026) : AUCUNE cle `ATK+` dans desc.


def GetAbilities() -> Sequence['Ability']:
    mechant = CardFinder(name=NOM_MECHANT, card_type=Villain)

    def boost_en_plus(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.GiveAdditionalBoostCardForThisActivation(1, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(mechant),
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, mechant, boost_en_plus),
        AbilityFactory.UnitAttackGainKeyword(mechant, overkill=True),
    ]
