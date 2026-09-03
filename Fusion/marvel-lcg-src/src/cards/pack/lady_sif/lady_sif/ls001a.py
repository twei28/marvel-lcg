from . import *

# * Lady Sif (face heros) — ASGARD. SOLDIER.
# CTR 1 / ATQ 2 / DEF 2 — HS 5 / PV 13
# Valiant Warrior — Response (thwart): After Lady Sif uses a basic power,
#   remove 1 threat from a scheme.
#
# Cartes de reference :
#  - `04032` * Captain Marvel (Carol Danvers), qui porte le declencheur exact
#    `AfterUnitUseBasicPower(Response, ..., op)` — chez elle « This » parce
#    que c'est une ALLIEE, « You » ici parce que c'est une IDENTITE ;
#  - `hk003` / `an004` pour la cible portee par L'ABILITE elle-meme
#    (`.SetTarget(Scheme2)`), et non par un `ChooseAbilities` imbrique.
#
# ⚠ LA CIBLE EST SUR L'ABILITE, ET C'EST UN CORRECTIF PAYE EN AUTOPLAY.
# La premiere version passait par `ChooseAbilities` + `ForChoiceAbility`
# (montage de hk010), ce qui fait DEUX questions au joueur pour un seul effet :
# « Valiant Warrior » puis « Remove 1 threat from a scheme ». Or le garde-fou
# anti-repetition du pilote (`MAX_REPETITIONS = 2`, autoplay.py:47) construit
# sa cle sur l'« id » LOCAL de l'option, qui recommence a 1 a chaque etape
# d'une capacite en plusieurs temps : les deux questions epuisaient le MEME
# compteur, et sur une Response qui part a CHAQUE pouvoir de base — deux a
# trois fois par round — le budget tombait des le 5e round. Mesure du
# 03/09/2026 : **5 parties bloquees sur 32** avec le montage a deux questions.
# C'est exactement le defaut decrit dans le commentaire d'autoplay.py a propos
# de Super Spy (ag001b). Une seule question, un seul compteur.
#
# ⚠ Le choix du joueur n'est PAS perdu au passage : `SetTarget` lui demande
# quand meme quelle manigance soulager. On supprime la question « veux-tu
# declencher », qui n'existait pas sur la carte imprimee — la Response est
# obligatoire.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « a basic power » : les TROIS pouvoirs de base — contrer, attaquer,
#    defendre. Le parametre `powers` de la fabrique reste donc a `None`. Une
#    attaque de base et une defense de base retirent de la menace elles aussi,
#    et c'est bien ce que la carte imprime.
#  - **AUCUNE limite imprimee.** Pas de « once per phase », pas de « once per
#    round » : la Response part a chaque pouvoir de base. C'est l'ecart avec
#    ls009 Sif's Crest, qui imprime « (Limit once per phase.) » sur un
#    declencheur presque identique. Les deux cartes du meme pack ne se
#    plafonnent donc PAS pareil.
#  - « remove 1 threat from A SCHEME » : au choix, principale ou annexe.
#  - Le libelle `(thwart)` alimente Desoriente : un heros desoriente ne
#    declenche pas Valiant Warrior.
#  - Pas de boucle : retirer de la menace n'est pas un pouvoir de base, la
#    Response ne peut pas se rappeler elle-meme.


def GetAbilities() -> Sequence['Ability']:

    def valiant_warrior(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Hero)
        Unused(message)

        this.RemoveThreatFromSchemes(effect.targets, 1, effect)

    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.Response,
            "You",
            valiant_warrior,
        ).SetName("Valiant Warrior")
        .SetLabel('thwart')
        .SetTarget(Scheme2, has_threat=True),
    ]
