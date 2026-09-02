from . import *

# Computer Mind — AMELIORATION signature, x1 (n/15 = 13).
# CONDITION. SUPERPOWER. Cout 1, ressource [mental].
# Response: After you play a card that has the requirement keyword, exhaust
#   Computer Mind -> draw 1 card for each required resource on that card.
#
# Cartes de reference :
#  - la fabrique « After you play a card » est
#    `AbilityFactory.AfterPlayerPlayedCard(<type>, "You", <filtre carte>, op)`
#    (play.py:310), dont le message expose `played_face`. Modele de forme :
#    ho006 (pack harry_osborn) pour la famille « reagir a la carte que tu
#    viens de jouer » — ho006 est sur `WhenPlayerPlayCard` (interruption), ici
#    c'est bien la version APRES ;
#  - 61023 / mots-cles/requirement.md pour la lecture du mot-cle : la valeur
#    vit dans `face.requirement`, un `Cost` rempli par
#    `HasCost.RegisterAttribute("Requirement", parse2)` (has_cost.py:23).
#
# ⚠ IL N'Y A AUCUNE AUTRE CARTE DU DEPOT QUI LISE LE MOT-CLE `Requirement`.
# Les 5 647 cartes l'IMPRIMENT (une trentaine) mais aucune ne compte les
# ressources exigees par une autre carte : Computer Mind est la premiere.
# D'ou la lecture directe de `face.requirement.val` plutot qu'un helper
# existant — il n'y en a pas.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « a card that HAS THE REQUIREMENT KEYWORD » : la carte doit porter le
#    mot-cle, pas seulement coûter des ressources. `face.requirement.val > 0`
#    est le seul test juste : `requirement` vaut `Cost("0")` par defaut, donc
#    une carte sans le mot-cle rend 0 et ne declenche rien.
#  - « for each REQUIRED RESOURCE on that card » : le nombre d'icones EXIGEES
#    (`Requirement` = "YB" -> 2 cartes piochees), et surtout PAS le cout de la
#    carte. Rappel de la fiche du mot-cle : « Requirement ([mental]) » sur une
#    carte a 2 veut dire « 2, dont au moins 1 mental », pas « 2 + 1 ».
#    Concretement pour le kit de Viv : vv002 Hologram Projection (`"YB"`)
#    pioche 2, vv004 / vv005 / vv009 (`"Y"`) piochent 1.
#  - « that card » : la carte qui vient d'etre jouee (`message.played_face`),
#    pas une autre.
#  - « AFTER you play » : `AfterPlayerPlayedCard`, jamais `WhenPlayerPlayCard`
#    qui est la fenetre AVANT (piege « Response/Interrupt + After » de
#    l'etape 5).
#  - « YOU play » : le filtre joueur est `"You"`, donc une carte jouee par un
#    autre joueur en multi ne declenche rien.
#  - « exhaust Computer Mind -> » : la fleche fait de l'epuisement un COUT,
#    donc une seule fois par round sans redressement.
#  - Le texte imprime dit `Response` nu, pas `Hero Response` : la capacite
#    joue donc aussi en forme alter-ego. Ne pas « corriger » en HeroResponse.


def GetAbilities() -> Sequence['Ability']:

    def carte_a_requirement(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> bool:
        Unused(effect)
        face = message.played_face
        if face is None or not HasCost.IsType(face):
            return False
        return face.requirement.val > 0

    def computer_mind(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        joueur = effect.GetInitiator()
        if joueur is None:
            return

        combien = message.played_face.requirement.val
        if combien <= 0:
            return
        joueur.DrawUp(combien, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            None,
            computer_mind,
            conditions=[carte_a_requirement],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
