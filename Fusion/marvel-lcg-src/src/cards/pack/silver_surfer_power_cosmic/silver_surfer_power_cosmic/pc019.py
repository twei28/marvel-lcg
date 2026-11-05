from . import *

# * Terrax — SBIRE NEMESIS (1/5). ELITE. HERALD. POWER COSMIC. SCH 2, ATK 2,
# HP 7. [star]Villainous. Toughness.
#
# Texte imprime :
#  « Terrax cannot arrive at or depart a PLANET. »
#  « When Revealed: Find Terrax's Axe and attach it to Terrax. If the Herald
#    of Galactus side scheme is not in play, find it and reveal it. »
#
# CARTES DE REFERENCE
#  - `pc021` Terrax's Axe porte sa PROPRE regle d'attache
#    (`AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name="Terrax"),
#    otherwise_attach_to="EnemyLeader")`, modele `57024` Taskmaster/`56161`
#    Namor) : il suffit de la METTRE EN JEU ici (`Find.FindAndReveal`), elle
#    s'attache TOUTE SEULE a la bonne cible -- pas besoin de choisir
#    Terrax ou le mechant a cet endroit.
#  - `Find.FindAndReveal` (find.py:52) : « find X and attach it to Terrax »
#    ET « find it and reveal it » (complot annexe) partagent le MEME verbe
#    moteur (« find+put into play »), seul le type de carte cherchee change.
#  - « Villainous »/« Toughness » : `desc.Villainous`/`desc.Toughness`
#    (bases automatiques, RECETTES §3, aucun script).
#  - « cannot arrive at or depart a PLANET » : `NePeutPasAllerÀUnePlanète`
#    (__init__.py du pack, ajoutee pour CETTE carte) -- `ArriverA`/`Departir`
#    sont des FONCTIONS directes (pas des messages WOULD interceptables
#    dans ce mot-cle maison), donc impossibles a bloquer par interruption
#    comme l'attaque/la manigance. `pc016` Black Hole (« the villain and
#    each minion engaged with that player arrive here ») POURRAIT sinon
#    envoyer Terrax a une planete sans que son immunite imprimee ne
#    s'applique -- poser le marqueur a l'entree en jeu le rend reellement
#    inerte a VIE, pas seulement « jamais cible » par coincidence.
#
# ⚠ PIEGE TROUVE le 05/11/2026 : `desc.set_name` DOIT correspondre, une fois
# nettoye par `FileManager.CleanName`, au NOM REEL du dossier qui contient
# ce fichier (`silver_surfer_power_cosmic`), PAS a un nom descriptif comme
# « Silver Surfer Nemesis » (nettoye en `silver_surfer_nemesis`, dossier
# INEXISTANT). `CardsDB.FindAbilities` (database.py:202-208) avale l'echec
# d'import SILENCIEUSEMENT (`except: pass`) et pose `ability_cache[...] =
# []` sans la moindre erreur : la carte compile, se fabrique, se revele,
# gagne Tough -- tout marche SAUF qu'aucune capacite ne se declenche jamais.
# Les cinq cartes nemesis du pack (pc019-pc023) avaient toutes ce mauvais
# `set_name` ; corrige dans `data/cards.json` en reprenant EXACTEMENT celui
# des autres cartes du pack, « Silver Surfer (Power Cosmic) ».
#
# TEXTE CONTRE CODE
#  « Find Terrax's Axe and attach it to Terrax » : toujours Terrax (This),
#    jamais le mechant (c'est `pc021` Terrax's Axe elle-meme qui gere le
#    repli « if Terrax is not in play, attach to the villain instead »).
#  « If the Herald of Galactus side scheme is NOT in play » : condition
#    verifiee avant de chercher, pour ne pas en reveler un second exemplaire.


def GetAbilities() -> Sequence['Ability']:

    def entree_en_jeu(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        Unused(message)
        NePeutPasAllerÀUnePlanète(effect.this)

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Find.FindAndReveal(
            effect, message.GetToPlayer(),
            name="Terrax's Axe",
            card_type=Attachment,
        )
        deja_en_jeu = Worlds.FindCardOnField(effect, name="Herald of Galactus", card_type=EncounterSideScheme)
        if deja_en_jeu is None:
            Find.FindAndReveal(
                effect, message.GetToPlayer(),
                name="Herald of Galactus",
                card_type=EncounterSideScheme,
            )

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            entree_en_jeu,
        ),
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
