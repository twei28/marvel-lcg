from . import *

# * Nekra — SBIRE NEMESIS. SCH 2 / ATQ 1 / PV 3. ELITE. LETHAL LEGION.
# Nekra gets +1 ATK and +1 HP for each hate counter on her.
# Forced Response: After Nekra attacks or takes damage, place 1 hate counter
#   on her (to a maximum of 5).
#
# ⚠ L'ETOILE IMPRIMEE N'EST PAS « PAR JOUEUR ». Les scans portent « 1* » en
# ATQ et « 3* » en PV : c'est le rappel que le TEXTE modifie ces valeurs. Les
# 41 sbires a etoile du depot sont, eux, des sbires de SCENARIO dont les PV se
# multiplient par le nombre de joueurs. Encodee « 3* », Nekra aurait 9 PV a
# trois joueurs. `cards.json` porte donc 3 et 1, et le bonus vit ici.
#
# TEXTE CONTRE CODE
#  « attacks OR takes damage » -> DEUX declencheurs distincts, donc deux
#    capacites : `AfterUnitAttackEnd` et `AfterUnitTookDamage`. Elle monte
#    donc plusieurs fois par round, ce qui justifie le plafond imprime.
#  « (to a maximum of 5) » -> plafond dans `AjouterUnPionDeHaine`, cote
#    helper : le moteur n'en sait rien.
#  « +1 ATK and +1 HP FOR EACH counter » -> valeur DYNAMIQUE, donc
#    `get_new_value`, pas un bonus fixe.


def GetAbilities() -> Sequence['Ability']:

    def par_pion_de_haine(effect: 'Effect', face: 'CardFace') -> int:
        Unused(face)
        return PionsDeHaine(effect.this)

    def monter_en_haine(effect: 'Effect', message: 'Message2') -> None:
        Unused(message)
        AjouterUnPionDeHaine(effect, effect.this)

    return [
        # ⚠ `change_on_event` EST OBLIGATOIRE avec `get_new_value` : sans
        # lui la valeur est calculee UNE FOIS et ne bouge plus, donc Nekra
        # resterait a son ATQ imprimee quel que soit le nombre de pions.
        # Modele `aoa/magik/45033`. Ici le declencheur de recalcul est la pose
        # ou le retrait d'un compteur SUR ELLE.
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Minion,
            get_new_value=par_pion_de_haine,
            attack=1,
            health=1,
            change_on_event=OnEvent.Counter("This", COMPTEUR_HAINE),
        ),
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.ForcedResponse,
            "This",
            monter_en_haine,
        ),
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.ForcedResponse,
            "This",
            monter_en_haine,
        ),
    ]
