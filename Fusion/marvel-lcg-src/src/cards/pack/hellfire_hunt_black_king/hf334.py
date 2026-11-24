from . import *

# Energy Counterattack (x2, hf334-hf335). Attachement SUPERPOWER. « Max 1 per character. Attach to Sebastian Shaw. Otherwise, attach to the villain.
# Forced Interrupt : When a character attacks the attached character, the attached character attacks that character. (Resolve the attached character's
# attack first). Set aside this card. »
# Cartes de reference : hf107 (WQ : `WhenUnitBeingAttack(ForcedInterrupt, ..., None, op)`), `CanAttack.BasicAttack(units, effect)` (can_attack.py:1146).
# ⚠ « When a character attacks » : un PERSONNAGE (heros / allie), pas un sbire ; l'attaque du porteur est resolue AVANT celle qui la declenche
# (Interruption) ; la carte part de cote ensuite.


def GetAbilities() -> Sequence['Ability']:
    def contre_attaque(effect: 'Effect', message: 'Message.WhenUnitBeingAttack') -> None:
        this = effect.this
        porteur = message.trigger
        attaquant = message.attacker
        Faces.SetAside([this], effect)
        if attaquant is not None and attaquant.IsInPlay():
            porteur.BasicAttack([attaquant], effect)

    return [
        AttacherAShawOuAuVilain(),
        AbilityFactory.WhenUnitBeingAttack(AbilityType.ForcedInterrupt, "AttachedEnemy", CardFinder(card_type=Hero | AlterEgo | Ally), contre_attaque),
    ]
