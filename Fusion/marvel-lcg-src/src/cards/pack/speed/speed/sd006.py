from . import *

# Kinetic Flurry (exemplaire 1/2) — EVENEMENT signature, custom « CptScorp »
# Cout X, [energy], classe Hero, traits ATTACK / SUPERPOWER.
# You can only spend [energy] resources to pay for this card. Choose an enemy
#   and perform the following attack X times:
#   Hero Action (attack): Deal 2 damage to that enemy (3 damage instead if
#   that enemy has an explosive counter on it).
#
# Exemplaire physique 1 de 2 (sd006, sd007). Commentaire complet ici, pointeur
# bref sur sd007.
#
# ---------------------------------------------------------------------------
# LE COUT X -> `desc.Cost = "X"` + `effect.GetCostX()` (effect.py:508 :
# « ressources payees - cout imprime »). Modele : `14006` Speed Cyclone,
# l'evenement a cout X de Quicksilver lui-meme, seul precedent exact du depot.
#
# ⚠ ECART ASSUME — LE MOTEUR NE SAIT PAS RESTREINDRE LA COULEUR D'UN COUT X.
# Le litteral de `Cost` (element/cost.py:38-42) enumere "R", "B", "Y", "RR",
# ... "0".."4" : il n'existe aucun « XY ». La seule carte officielle qui
# imprime « you can only spend [physical] resources to pay for this card »
# (10002 Crushing Blow) contourne le probleme en ayant un cout FIXE, encode
# `Cost: "R"` — impossible ici, ou le cout est justement variable.
#
# Repli retenu, plus SEVERE que la carte et jamais plus permissif : on ne
# compte que l'energie reellement payee, `paye.GetColor("Y")` (rbyg.py:57-67,
# qui ajoute le wild a la couleur demandee, exactement comme
# `OnlyHasColor("Y")` du heros). Une ressource physique ou mentale glissee
# dans le paiement n'achete donc AUCUNE attaque supplementaire : elle est
# perdue. Le joueur ne peut pas gagner d'attaque avec une couleur interdite,
# ce que la carte veut ; il peut seulement gaspiller, ce que la carte lui
# epargnerait. Ecart repris dans docs/speed_cartes.md.
#
# ---------------------------------------------------------------------------
# « CHOOSE AN ENEMY and perform the following attack X TIMES » ->
# `.SetTarget(Enemy)` (portee par defaut (1, 1)) : l'ennemi est choisi UNE
# SEULE FOIS, et toutes les iterations tapent « THAT enemy ». Puis une boucle
# `for _ in range(x)` de X `DealDamage` SEPARES — pas un seul paquet de 2X.
# La difference est observable : chaque salve est une attaque distincte, donc
# une riposte (Retaliate) mord X fois, et tout effet « apres que cet ennemi
# subit des degats » part X fois. (Dans ce moteur `DealDamage` declenche bien
# la riposte : c'est ce que prouve le cas wc005 contre M.O.D.O.K.)
#
# La boucle s'arrete des que la cible quitte le jeu ou est vaincue : inutile
# de continuer a taper une carte qui n'est plus la, et `DealDamage` sur une
# face hors jeu n'a pas de sens.
#
# ---------------------------------------------------------------------------
# « 3 DAMAGE INSTEAD IF THAT ENEMY HAS AN EXPLOSIVE COUNTER ON IT » : la
# condition est REEVALUEE A CHAQUE ITERATION (le test est dans la boucle). Le
# compteur pourrait disparaitre en cours de route (une carte qui le retire, un
# effet declenche par les degats) ; le texte parle bien de l'etat de l'ennemi
# au moment de CHAQUE attaque.
#
# SYNERGIE VOULUE : payee uniquement en energie, la carte declenche d'abord
# Hyperkinetic Fuel (Interrupt, AVANT la resolution) ; si le joueur pose le
# compteur sur la cible visee, les X attaques font 3 au lieu de 2.


def GetAbilities() -> Sequence['Ability']:

    def kinetic_flurry(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        if not effect.targets:
            return
        cible = effect.targets[0]

        # Voir l'ecart assume ci-dessus : X = energie (+ wild) reellement
        # payee, et non `effect.GetCostX()`, qui compterait aussi les couleurs
        # que la carte interdit.
        nombre_d_attaques = effect.GetPaidResources().GetColor("Y")

        for _ in range(nombre_d_attaques):
            if not cible.IsInPlay() or cible.IsDefeated():
                break
            degats = 3 if PorteUnCompteurExplosif(cible) else 2
            this.DealDamage([cible], degats, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            kinetic_flurry,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
