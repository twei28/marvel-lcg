from . import *

# * Fifty-One — ALLIE MENEUR, cout 2, PV 2, CTR 1* / ATQ 2*. AERIAL. RANGER.
#   [energy].
# Response: After Fifty-One is defeated by taking consequential damage, choose
#   an ally, that ally gets +1 THW and +1 ATK until the end of the phase.
#
# CARTES DE REFERENCE
#  - `bk014` Proper Funeral : `AfterUnitBeDefeated`, et `message.trigger` pour
#    le vaincu.
#  - `dt035` Gladiator : les degats CONSEQUENTS cotes moteur.
#
# TEXTE CONTRE CODE
#  « by taking CONSEQUENTIAL damage » -> la mort doit venir de SES PROPRES
#    pouvoirs de base, pas d'une attaque du vilain. Sans ce filtre, l'allie
#    donnerait son bonus a chaque fois qu'il tombe, ce qui est deux fois plus
#    souvent. Le message porte `killer` : quand Fifty-One se tue lui-meme en
#    contrant ou en attaquant, c'est LUI le tueur.
#  « choose AN ALLY » -> un seul, et un allie : pas l'identite, pas plusieurs.
#  « until the end of the PHASE » -> `GainUntilPhaseEnd`, pas le round.
#  ⚠ Fifty-One est DEJA VAINCU quand la Reponse resout : il ne peut pas se
#    choisir lui-meme, et le moteur l'exclut de fait puisqu'il n'est plus en
#    jeu.


def GetAbilities() -> Sequence['Ability']:

    def mort_utile(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this, message)
        for face in effect.targets:
            face.GainUntilPhaseEnd(effect, thwart=1, attack=1)

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.Response,
            "This",
            mort_utile,
            # ⚠ `by_consequential=True` EST DEJA DANS LA FABRIQUE
            # (defeated.py:345). Une premiere version reecrivait la condition a
            # la main en comparant `message.killer` a `effect.this` : c'est
            # exactement ce que le moteur fait deja, en mieux. Chercher le
            # parametre AVANT d'ecrire le garde.
            by_consequential=True,
        ).SetTarget(Ally)
        # ⚠ SANS CECI LA CAPACITE NE PART JAMAIS. Au moment ou la Reponse
        # resout, Fifty-One est DEJA dans la defausse : le controle de zone
        # generique (`CheckNotOutOfPlay`, effect_checker.py) refuse toute
        # capacite portee par une carte hors jeu. C'est le cas de TOUTE
        # capacite « After this card is defeated » imprimee sur la carte
        # elle-meme — d'ou `NoOutOfPlayLimit`, l'idiome du depot (`aa002`,
        # `dz014`, `09032`). Mesure : le journal montrait bien « was defeated »
        # puis plus rien, sans la moindre erreur.
        .NoOutOfPlayLimit(),
    ]
