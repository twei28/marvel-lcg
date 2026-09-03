from . import *

# * Iron Man (face heros) — AVENGER.
# CTR 2 / ATQ 2 / DEF 2 — HS 5 / PV 10
# Reactor Cores — Action: Spend X printed [energy] resources -> place X
#   reactor counters here.
#
# Cartes de reference :
#  - **`29038` Haywire** pour le selecteur : `SetTarget(has_printed_res="Y",
#    from_where=["YourHandCards"], ...)`. C'est le moteur qui sait deja lire
#    l'icone IMPRIMEE d'une carte, il n'y a rien a construire ;
#  - **`01174` Electromagnetic Backlash** et `23013` * Captain Marvel pour le
#    COMPTAGE : `FacesCounter.GetPrintedResourcesCount(faces, "Y")`. Les deux
#    chemins servent, et il faut les deux : le selecteur dit QUELLES cartes
#    sont depensees, le compteur dit COMBIEN de ressources elles valent ;
#  - `Faces.PlaceCountersOn` (faces.py:206) pour le compteur.
#
# ⚠ ARBITRAGE DE L'UTILISATEUR (03/09/2026) — « **printed** ». Lecture
# LITTERALE : seules les cartes dont l'icone IMPRIMEE est [energy] chargent le
# reacteur. Consequence directe et assumee : **im005 Stark Tower ne peut PAS
# charger le reacteur** (elle GENERE un wild), ni 01088 Energy (qui GENERE
# deux energies). Il faut depenser de vraies cartes energie de la main.
# C'est ce que dit la carte, et c'est ce qui borne la mecanique : sans cette
# lecture, un seul Stark Tower rechargerait indefiniment.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « Spend X » : X est choisi par le JOUEUR, de 1 a toute sa main. D'ou
#    `range=(1, "All")` — et surtout pas un cout X classique
#    (`effect.GetCostX()`), qui laisserait payer avec n'importe quelle
#    ressource, generee comprise.
#  - ⚠ **X COMPTE LES RESSOURCES, PAS LES CARTES.** « X printed [energy]
#    RESOURCES » : une carte qui porte DEUX icones energie imprimees en vaut
#    deux. `01088` Energy (RES = "YY") pose donc **2 compteurs a elle seule**.
#    Compter les cartes (`len(cartes)`) etait la premiere ecriture, et elle
#    aurait sous-paye le joueur en silence sur toutes les cartes a double
#    icone. D'ou `GetPrintedResourcesCount`, qui compte les ICONES.
#  - « place X reactor counters HERE » : sur CETTE face, l'identite. Pas sur
#    une amelioration, pas sur un allie.
#  - Le type imprime est **`Action` nu**, pas `Hero Action`. Sans consequence
#    ici — la carte EST la face heros — mais on ecrit ce qui est imprime,
#    meme lecture que l'`Action` de ls001b et l'`Interrupt` de hk001b.
#  - AUCUNE limite imprimee : l'action se reprend tant qu'il reste des cartes
#    energie en main et une activation disponible.
#  - `reactor` est un compteur MAISON, ajoute a l'enum `COUNTER` pour ce pack.
#    Sans lui, `IsCounter` refuse le nom et la carte tombe a la creation de la
#    partie, pas en jeu.


def GetAbilities() -> Sequence['Ability']:

    def reactor_cores(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Hero)
        Unused(message)

        cartes = [face for face in effect.targets if face is not None]
        if not cartes:
            return

        # « SPEND » : depenser une carte en ressource, c'est la defausser de
        # la main. On compte les ICONES imprimees, pas les cartes : 01088
        # Energy en porte deux et vaut donc deux compteurs.
        energie = FacesCounter.GetPrintedResourcesCount(cartes, "Y")
        if energie <= 0:
            return
        Faces.DiscardAll(cartes, effect)
        Faces.PlaceCountersOn([this], energie, 'reactor', effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            reactor_cores,
        ).SetName("Reactor Cores")
        .SetTarget(has_printed_res="Y", from_where=["YourHandCards"],
                   range=(1, "All"), canbe_discard=True),
    ]
