from . import *

# Natural Genius — RESSOURCE signature, x1 (n/15 = 10).
# Deux icones [mental] imprimees (RES = "BB").
# Spend this card only in alter-ego form.
#
# Carte de reference : **`10007` Limitless Strength**, la ressource du HULK
# OFFICIEL (src/cards/pack/hlk/hulk/10007.py), qui imprime la phrase MIROIR
# (« only in hero form ») et se rend par
# `CheckThisCanDropPay(Resources(...), spend_this_only_in_hero_form=True)`.
# Le drapeau alter-ego existe dans la meme signature
# (`resources.py:67`) : `spend_this_only_in_alter_ego_form`.
#
# ⚠ Piege de nom, a ne pas confondre : la carte hk012 de CE pack s'appelle
# aussi « Limitless Strength », mais c'est une AMELIORATION, pas la ressource
# officielle 10007. Deux cartes differentes, meme nom, deux sets.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « SPEND this card only in... » restreint la DEPENSE en ressource, pas la
#    possession : la carte se pioche et se garde en main dans les deux formes.
#  - Deux icones imprimees, donc `Resources("BB")` : la carte paie DEUX
#    ressources mentales, pas une.
#  - Aucune autre capacite imprimee : ce module ne porte que la restriction.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CheckThisCanDropPay(
            Resources("BB"),
            spend_this_only_in_alter_ego_form=True,
        ),
    ]
