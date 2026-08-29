from . import *

# * Klaw
# ELITE. MASTERS OF EVIL.
# Villainous.
# Forced Response: After Klaw attacks and damages a character, stun that
#   character.
#
# Le Klaw OFFICIEL a exactement cette clause, portee par son Sonic Converter
# (01118) : meme fabrique `AfterUnitAttackAndDamageUnit`, meme
# `Faces.GiveStatus([message.attacked], "Stunned")`, meme `target_in_play`.
# On reprend son squelette au mot pres, en remplacant l'attaquant cherche par
# nom par « This » — ici la capacite est imprimee sur Klaw lui-meme.
#
# « Villainous » est porte par le desc (`"Villainous": "1"`), pas par le code :
# le moteur lit le desc, jamais le texte.


def GetAbilities() -> Sequence['Ability']:

    def klaw(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        Faces.GiveStatus([message.attacked], "Stunned", effect)

    return [
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.ForcedResponse,
            "This",
            "Character",
            klaw,
            target_in_play=True,
        ),
    ]
