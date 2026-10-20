from . import *

# Kree Soldier — SBIRE (Hala Ultimatum). KREE. SOLDIER. SCH 1, ATK 2, PV 5. 1 etoile, aucune icone de boost.
#   4 exemplaires.
# Guard.
# [star] Boost: If the activating enemy has a tough status card, put Kree Soldier into play engaged with you.
#
# Cartes de reference :
#  - Guard : natif (desc.Guard, fiche mots-cles/guard.md).
#  - « Boost: ... put X into play engaged with you » : `message.activating_enemy` + `Faces.HasStatus`
#    (modele gs147/gs148, meme pack) + `Minion.PutIntoPlay(joueur, effect)` (modele
#    `skrull_menace/secret_invasion/__init__.py`, `SbireImpostor`).
#
# ⚠ Mots-pieges : « engaged WITH YOU » (le joueur vise par l'activation en cours, pas le controleur d'un
# allie attaque) ; aucune icone de boost imprimee (Y rouge) sur cette carte : le Boost se resout seulement
# comme texte, sans bonus de boost chiffre.


def GetAbilities() -> Sequence['Ability']:

    def booster(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        if Faces.HasStatus([message.activating_enemy], "Tough") > 0:
            joueur = message.against_player or effect.GetInitiator()
            if joueur is not None:
                effect.this.CastTo(Minion).PutIntoPlay(joueur, effect)

    return [
        AbilityFactory.WhenCardBecomeBoost("This", booster),
    ]
