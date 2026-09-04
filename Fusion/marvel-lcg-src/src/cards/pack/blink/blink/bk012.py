from . import *

# * Mimic (Calvin Rankin) — ALLIE BASIC, cout 3, PV 3. X-MEN.
# [star] Action: Choose a character in play -> until the end of the round,
#   Mimic's THW is equal to that character's printed THW (SCH instead if you
#   choose an enemy) and his ATK is equal to that character's printed ATK.
#
# ⚠ CTR ET ATQ IMPRIMEES « ★ », SANS VALEUR FIXE. Le PROCESSUS-CARTE cite
# exactement ce cas (l'ATQ ★ de l'Homme-Pourpre) comme devant declencher une
# QUESTION. Arbitrage de l'utilisateur du 04/09/2026 : encodee 0/0 dans
# `cards.json`, l'Action posant les valeurs copiees. Consequence assumee et
# fidele au texte : sans Action, Mimic ne fait rien.
#
# TEXTE CONTRE CODE
#  « that character's PRINTED THW » -> la valeur IMPRIMEE, donc `printed_*` :
#    les bonus en cours sur la cible ne se copient PAS.
#  « SCH INSTEAD if you choose an ENEMY » -> les ennemis n'ont pas de CTR,
#    c'est leur SCH qu'on lit. Mot-piege « instead ».
#  « UNTIL THE END OF THE ROUND » -> `GainUntilRoundEnd`, pas un bonus
#    permanent.


def GetAbilities() -> Sequence['Ability']:

    def copier(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        cibles = list(effect.targets)
        if not cibles:
            return
        modele = cibles[0]

        if Enemy.IsType(modele):
            contre = int(getattr(modele, "printed_scheme", 0) or 0)
        else:
            contre = int(getattr(modele, "printed_thwart", 0) or 0)
        attaque = int(getattr(modele, "printed_attack", 0) or 0)

        this.GainUntilRoundEnd(effect, thwart=contre, attack=attaque)

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            copier,
        ).SetTarget(Unit2),
    ]
