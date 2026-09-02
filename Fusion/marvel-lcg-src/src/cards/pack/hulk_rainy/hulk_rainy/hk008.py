from . import *

# Unnatural Strength — RESSOURCE signature, x1 (n/15 = 11).
# Deux icones [physical] imprimees (RES = "RR").
# Spend this card only in hero form.
#
# Carte de reference : **`10007` Limitless Strength** (Hulk officiel), qui
# imprime la MEME phrase au mot pres et se rend par
# `CheckThisCanDropPay(Resources("RRR"), spend_this_only_in_hero_form=True)`.
# Seul le nombre d'icones differe : trois la-bas, DEUX ici — releve sur le
# scan, coin inferieur gauche, deux poings rouges.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « SPEND ... only in hero form » : restriction de DEPENSE, pas de pioche.
#  - Cette carte est la jumelle de hk007 (mentale, alter-ego) : les deux
#    ensemble forcent le joueur a changer de forme pour depenser sa main, ce
#    qui alimente hk009 The Other Guy. C'est le coeur du pack.
#  - Aucune autre capacite imprimee.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CheckThisCanDropPay(
            Resources("RR"),
            spend_this_only_in_hero_form=True,
        ),
    ]
