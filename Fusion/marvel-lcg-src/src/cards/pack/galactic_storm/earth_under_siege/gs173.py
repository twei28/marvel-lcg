from . import *

# Atlantean Battle Gear — ATTACHEMENT (ensemble Attuma). ARMOR. ATLANTIS. Badge +1 ATK.
# Attach to an ATLANTIS enemy. Otherwise, attach to the villain.
# Reduce the damage attached enemy takes from each attack by 1.
# Hero Action: Spend [mental][physical] resources → discard this card.
#
# Cartes de reference :
#  - « Attach to an ATLANTIS enemy. Otherwise, attach to the villain » : identique a gs172.
#  - « Reduce the damage attached enemy takes from each attack by 1 » : `AbilityFactory.GiveKeywordToAttached`
#    n'a pas de parametre dedie a une REDUCTION de degats recus ; modele direct :
#    `WhenFaceWouldDealDamage`-style interrupt qui `message.ReduceDamage(1, effect)` sur l'hote attache,
#    modele `62010 Metal Bracer` (cite dans damage.py, ReduceDamage).
#
# ⚠ Mots-pieges : « EACH attack » (pas seulement l'attaque du mechant : tout attaquant) ; « reduce ... by
# 1 » plancher a 0 (natif, `ReduceDamage`) ; icones de ressource DECISION UTILISATEUR (20/10/2026) : grappe
# de 3 disques = mentale, forme arrondie = physique -> Cost("BR").


def GetAbilities() -> Sequence['Ability']:

    def reduire(effect: 'Effect', message: 'Message.WhenFaceWouldDealDamage') -> None:
        message.ReduceDamage(1, effect)

    def sur_lhote(effect: 'Effect', message: 'Message.WhenFaceWouldDealDamage') -> bool:
        return message.target is getattr(effect.this, 'bind_face', None)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(trait="ATLANTIS", card_type=Enemy),
            otherwise_attach_to=Villain,
        ),
        AbilityFactory.WhenDamageWouldBeDealtTo(
            AbilityType.ForcedInterrupt,
            Enemy,
            reduire,
            conditions=[sur_lhote],
        ),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction).SetCost(Cost("BR")),
    ]
