from . import *

# Superhuman Registration Act — MANIGANCE de nemesis (2/5). 3 menaces PAR
# JOUEUR, boost 2, PERMANENTE.
# Permanent.
# While there is at least 1 threat here, this scheme gains a hazard icon
#   ([hazard]).
#
# ⚠ PERMANENT est une BASE AUTOMATIQUE (`desc.Permanent`, lu par
# `has_permanent.py`) : ne JAMAIS recoder le blocage de sortie de jeu ici.
# Fiche lue : `mots-cles/permanent.md`.
#
# ⚠ L'ICONE D'ALEA n'est PAS imprimee sur cette carte : elle est GAGNEE tant
# qu'il y a de la menace. `desc` ne porte donc pas de clef `Hazard`, et c'est
# volontaire. Fiche lue : `mots-cles/hazard.md`.
#
# CARTE DE REFERENCE
#  - `gp011` Rules of the Universe (Gwenpool) : L'INVERSE EXACT, mot pour mot
#    (« While there is no threat here, this scheme LOSES the [hazard] icon »),
#    et deja une manigance nemesis PERMANENTE. Elle porte meme le correctif
#    dont on a besoin, en commentaire : sans `change_on_event`, la condition
#    n'est evaluee QU'A L'ENTREE EN JEU, et une manigance permanente garde
#    alors son icone figee pour toute la partie. `OnEvent.Threat("This")`
#    reevalue a chaque variation de menace.
#
# TEXTE CONTRE CODE
#  ⚠ « AT LEAST 1 threat » : 1 icone, pas une par menace. Le multiplicateur
#    rendu par la fonction est donc 0 ou 1, jamais `this.threat`.
#  ⚠ Une manigance a 3 menaces PAR JOUEUR entre en jeu chargee : l'icone est
#    donc allumee des le depart, et ne s'eteint que si la table la vide
#    entierement. Elle ne peut pas quitter le jeu (Permanent) : la seule sortie
#    est de la ramener a zero.


def GetAbilities() -> Sequence['Ability']:

    def au_moins_une_menace(effect: 'Effect', ui: 'List[CardFace]') -> int:
        Unused(ui)
        this = effect.this.CastTo(EncounterSideScheme)
        return 1 if this.threat >= 1 else 0

    return [
        AbilityFactory.ThisGainKeyword(
            au_moins_une_menace,
            hazard=1,
            change_on_event=OnEvent.Threat("This"),
        ),
    ]
