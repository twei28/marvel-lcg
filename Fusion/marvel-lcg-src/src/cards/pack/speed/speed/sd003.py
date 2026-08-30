from . import *

# Blasting Velocity (exemplaire 1/2) — EVENEMENT signature, custom « CptScorp »
# Cout 2, [energy], classe Hero, traits SUPERPOWER / THWART.
# Hero Action (thwart): Remove 3 threat from a scheme. Make a basic attack
#   against an enemy with an explosive counter on it without exhausting.
#
# Exemplaire physique 1 de 2 (sd003, sd004). Commentaire complet ici, pointeur
# bref sur sd004.
#
# ⚠ NE PAS COPIER CE FICHIER SUR sd008 Swift Strikes, ni l'inverse : les deux
# cartes sont des MIROIRS, pas des jumelles. Ici : menace d'abord (3 retirees
# d'une manigance), ATTAQUE de base ensuite, sur un ENNEMI marque. La-bas :
# degats d'abord (3 a un ennemi), CONTRE de base ensuite, sur une MANIGANCE
# marquee. Deux exemplaires ici, trois la-bas.
#
# ---------------------------------------------------------------------------
# « Remove 3 threat from A SCHEME » -> `.SetTarget(Scheme2)` : n'importe
# quelle manigance, JAMAIS `MainScheme` seul (le texte ne dit pas « the main
# scheme »). Modele : 10004 Sub-Orbital Leap, meme `.SetLabel('thwart')` +
# `.SetTarget(Scheme2)` + `this.RemoveThreatFromSchemes(effect.targets, N,
# effect)`.
#
# ---------------------------------------------------------------------------
# « Make a basic attack against an enemy with an explosive counter on it
# without exhausting » :
#
# - `heros.BasicAttack(cibles, effect)` (can_attack.py:633). C'est bien
#   « without exhausting » : `BasicAttack` resout l'attaque de base et
#   n'incline RIEN — c'est l'ACTION de base du joueur qui incline d'ordinaire,
#   pas l'attaque elle-meme. Meme lecture que bw024 Strong as Silk, qui
#   imprime la meme tournure. Et `IsCanAttack` (can_attack.py:691) ne teste
#   PAS l'inclinaison : l'attaque part meme si Speed est deja incline, ce qui
#   est tout l'interet de la carte.
#
# - Le ciblage est RESTREINT aux ennemis portant un compteur explosif :
#   `has_counter=COMPTEUR_EXPLOSIF`, filtre de premier niveau de `CardFinder`
#   (card_finder/checker.py:346-350), expose par `SetTarget`
#   (ability.py:702). On ne peut donc pas designer un ennemi non marque.
#
# - S'il n'y a AUCUN ennemi marque : rien ne se passe, sans erreur. La garde
#   est explicite (`if not cibles: return`) parce qu'un `ChooseAbilities` avec
#   un selecteur obligatoire et zero cible legale poserait une question vide.
#
# - Le choix passe par un `ChooseAbilities` imbrique et NON par `.SetTarget2` :
#   c'est la lecon hd009 (Quack and Burn) — `effect.targets2` n'est pas
#   alimente par le pilote generique de `tools/test_capacites.py`, la seconde
#   moitie de la carte ne serait jamais exercee et rien ne le signalerait.
#
# - L'attaque part du HEROS, pas de l'evenement (`joueur.GetHero()`) : c'est
#   une attaque DE BASE, elle doit employer l'ATQ de Speed et se declarer comme
#   une attaque du heros (modele 01053 Relentless Assault, qui fait aussi
#   partir ses degats de `initiator.GetHero()`).
#
# SYNERGIE VOULUE : payee uniquement en energie, la carte declenche d'abord
# Hyperkinetic Fuel (Interrupt, AVANT la resolution), qui pose le compteur ;
# l'attaque de base trouve alors une cible legale. Sans compteur prealable,
# la carte se resume a son retrait de menace.


def GetAbilities() -> Sequence['Ability']:

    def blasting_velocity(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        this.RemoveThreatFromSchemes(effect.targets, 3, effect)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        heros = joueur.GetHero()
        if heros is None:
            return

        cibles = [face for face in FacesAvecUnCompteurExplosif(effect)
                  if Enemy.IsType(face)]
        if not cibles:
            return

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Make a basic attack against an enemy with an explosive counter on it, without exhausting",
                lambda targets:
                    heros.BasicAttack(list(targets), effect),
            ).SetTarget(Enemy, has_counter=COMPTEUR_EXPLOSIF, range=(1, 1)),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            blasting_velocity,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
