from . import *

# Edges Syndrome — OBLIGATION, custom « jakxin »
# `desc.Boost = "1"`, `desc.GiveTo = "America Chavez"`.
#
# Give to the America Chavez player.
# Your identity gets -1 to each of its basic powers.
# Action: Take 2 damage → discard this card.
# Action: Take 4 damage → remove this card from the game.
# ---
# [star] Boost: Reveal this card.
#
# ---------------------------------------------------------------------------
# CARTE DE REFERENCE — `04166` Anti-Hero Propaganda
#
# Meme famille exacte : une obligation qui RESTE EN JEU, impose un malus
# continu aux pouvoirs de base et offre une Action pour s'en debarrasser.
# Elle s'ecrit `*AbilityFactory.GiveKeywordToInPlayWhenApplyThis(Hero,
# thwart=-1, attack=-1, defense=-1)` +
# `AbilityFactory.PlayerActionToDiscardThis(...).SetCostFunc(
# CostFunc.TakeDamage(2, "YourIdentity"))`. `28021` Weight of the World
# confirme qu'une obligation reste en jeu quand elle porte un effet continu.
#
# ⚠ Le fait que la carte RESTE EN JEU est ce qui donne son sens aux deux
# Actions : sans cela il n'y aurait rien a defausser ni a retirer du jeu.
#
# ---------------------------------------------------------------------------
# « YOUR IDENTITY GETS -1 TO EACH OF ITS BASIC POWERS »
#
# « IDENTITY », pas « hero » : le malus vaut sur LES DEUX FACES, d'ou
# `Identity` comme filtre et non `Hero` (`04166` dit « your HERO gets » et
# emploie `Hero` — deux textes differents, on ne recopie pas).
#
# « EACH of its basic powers » -> les quatre pouvoirs de base du jeu : ATQ,
# CTR, DEF et REC. `unit.Gain` n'applique un attribut que si la face le
# POSSEDE (face_gain.py:120-125 et suivants) : la face heros perd donc ATQ,
# CTR et DEF, la face civile perd REC. Rien a trier a la main.
#
# « YOUR identity » -> `control_by="You"` (environment_helper.py:177-179,
# `Select.GetYou(effect)` contre `face.GetControlBy()`). Sans lui, en
# multijoueur, le malus frapperait TOUTES les identites en jeu. `04166` ne le
# pose pas ; on ne recopie pas son omission.
#
# ---------------------------------------------------------------------------
# LES DEUX ACTIONS — LA FLECHE EST UN COUT DANS LES DEUX
#
# `CostFunc.TakeDamage(N, "YourIdentity")` (cost_func.py:408-437), porte par
# la capacite : le moteur ne propose pas l'action quand les degats ne peuvent
# pas etre encaisses.
#
# « Action » NU, pas « Alter-Ego Action » : `AbilityType.Action`, disponible
# dans LES DEUX formes. `04166` dit « Alter-Ego Action » et emploie
# `AbilityType.AlterEgoAction` — encore une fois, deux textes differents.
#
# ⚠ Le pilote du harnais prend TOUJOURS la premiere action offerte : la
# seconde branche (4 degats, retrait du jeu) s'exerce avec le 3e argument de
# `Puzzle.Action('ma017', 'Action', 1)`, ou avec la cle `preferer_option`.
#
# ⚠ Aucun code pour la capacite Boost (« [star] Boost: Reveal this card. ») :
# c'est le comportement par defaut d'une obligation dans le paquet de bonus,
# `desc.Boost` est lu nativement. Coder une capacite fantome serait une faute.


MALUS = -1
DEGATS_POUR_DEFAUSSER = 2
DEGATS_POUR_RETIRER = 4


def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Identity,
            control_by="You",
            attack=MALUS,
            thwart=MALUS,
            defense=MALUS,
            recover=MALUS,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.Action,
        ).SetCostFunc(CostFunc.TakeDamage(DEGATS_POUR_DEFAUSSER, "YourIdentity")),
        AbilityFactory.PlayerActionToRemoveThisFromGame(
            AbilityType.Action,
        ).SetCostFunc(CostFunc.TakeDamage(DEGATS_POUR_RETIRER, "YourIdentity")),
    ]
