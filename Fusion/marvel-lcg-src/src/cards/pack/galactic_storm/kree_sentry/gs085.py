from . import *

# Death Grip — MANIGANCE ANNEXE (Kree Sentry). Menace de depart 3[per_hero]. 1 icone de boost.
# Sentry's Grasp is set aside when there is 5 or more damage on it instead of 3.
#
# Cartes de reference :
#  - le seuil « 3 » est lu par la Poigne (gs082) dans `SeuilDeLaPoigne`, qui cherche une Death Grip EN JEU dont la
#    face porte `gs_seuil_poigne` ; cette carte POSE ce marquage a son entree en jeu (`AfterCardEnterPlay("This")`, modele
#    squirrel_girl `refuse_target_fn` pour un attribut pose sur la face) et le retire a sa sortie.
#  - « 3 or more damage here » est un etat, pas un declencheur : a la sortie de Death Grip, une Poigne qui porte deja 3 ou
#    4 degats doit etre remise de cote (`AfterCardLeavePlay("This")`, porte NoOutOfPlayLimit).
#
# ⚠ Mots-pieges : « INSTEAD of 3 » = remplace le seuil, ne s'ajoute pas ; « when there is 5 or MORE » ; « on it » = les
# degats de CHAQUE Poigne ; la Poigne a 3 ou 4 degats quand Death Grip s'en va tombe aussitot (lecture, question Q4).


def GetAbilities() -> Sequence['Ability']:

    def entree(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        Unused(message)
        effect.this.gs_seuil_poigne = 5

    def sortie(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> None:
        Unused(message)
        effect.this.gs_seuil_poigne = 3
        for poigne in PoignesEnJeu(effect):
            if poigne.GetCounters('damage') >= SeuilDeLaPoigne(effect):
                Faces.SetAside([poigne], effect)

    return [
        AbilityFactory.AfterCardEnterPlay(AbilityType.NonKeyword, "This", entree),
        AbilityFactory.AfterCardLeavePlay(AbilityType.NonKeyword, "This", sortie),
    ]
