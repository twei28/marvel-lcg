from . import *

# CORRECTIF (27/10/2026, passe de fusion hg028-hg076, cas `[hg] hg057` rouge : infection = 0) : une capacite
# `AfterUnitBeDefeated(..., "This", ...)` standard ne part JAMAIS pour la defaite de la carte elle-meme -- au moment
# du message « After », la carte a deja quitte le jeu et la limite « hors jeu » ecarte sa capacite (piege deja
# documente sur `gs229`). Remede : `.NoOutOfPlayLimit()`, exactement comme `alien_vs_predator/xenomorph_deck`
# (`AfterUnitBeDefeated(NonKeyword, "This", apres_defaite).NoOutOfPlayLimit()`). Le filtre `"This"` garde la
# portee : seule la defaite de CETTE carte declenche la reponse.
#
# Bloated Zombie — SBIRE (set partage « Hungry Horde », module du scenario « The Hunger Core »). Trait ZOMBIE
# (PAS METAZOMBIE : verifie dans data/cards_custom.json, "traits": ["ZOMBIE"], meme constat que hg056).
# SCH 0. ATK 1. PV 5. Guard 1. [star] Boost: 2.
# Guard.
# Forced Response: After this minion is defeated, each player places 1 infection counter.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - [[guard]] (docs/reference/mots-cles/guard.md) : « Guard. » -> base automatique, `desc.Guard` deja a "1"
#   dans cards_custom.json. Aucun script pour ce mot-cle (seule la Reponse Forcee ci-dessous a besoin d'un
#   module).
# - « infection counter » : PAS une fiche `mots-cles/` dediee -- tranche definitivement par hg037 Widow's Bite
#   (meme pack, commentaire detaille) et reconduit sans nouvelle question par hg002/hg003 : c'est un compteur
#   de carte/scenario ordinaire (meme famille que les compteurs `flame`/`rage`/`web` deja cites en tete de
#   mots-cles/README.md comme « compteurs de carte, pas un mot-cle »). Mecanisme documente dans le docstring
#   de `commun.PoserInfection` (pose sur l'identite du joueur, seconde jauge de vie du livret TTS).
# - [star] Boost (icone) : badge natif, aucun script (meme raisonnement que hg056).
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « Guard. » seul : meme lecture que hg056 (ce pack) / `01101` Hydra Mercenary -- aucune ligne de script
#   pour ce mot-cle precis.
# - « Forced Response: After THIS minion is defeated, <effet> » (auto-declencheur sur la DEFAITE DE LA CARTE
#   ELLE-MEME, quelle qu'en soit la cause -- texte different de « after A minion is defeated ») : modele
#   officiel `next_evol/stryfe/40168a.py` Stryfe's Grasp, qui utilise EXACTEMENT
#   `AbilityFactory.AfterUnitBeDefeated(AbilityType.ForcedResponse, CardFinder(name="Stryfe"), ...)` pour un
#   auto-declencheur de ce type ; la fabrique elle-meme (`game/ability/factory/defeated.py`,
#   `AfterUnitBeDefeated`) accepte directement le litteral `"This"` comme `who_be_defeated` (vu aussi dans
#   `next_evol/stryfe/40168a.py` ligne `AfterUnitBeDefeated(AbilityType.NonKeyword, "This", apres_defaite)`
#   pour un AUTRE declencheur de la meme carte) : `"This"` est donc une valeur de parametre valide et deja
#   utilisee dans ce sens exact ailleurs dans le depot.
# - « each player places 1 infection counter » : boucle `Worlds.GetPlayers(effect)` + `PoserInfection(effect,
#   joueur, 1)`, modele MOT POUR MOT hg002/hg003 (« When Revealed: Each player places 1 infection counter »,
#   seul le declencheur differe -- When Revealed vs Forced Response After this minion is defeated -- l'action
#   posee sur chaque joueur est identique).
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE (etape 5)
#
# « Guard. » -> base automatique (desc.Guard), aucune ligne de script.
# « Forced Response » -> `AbilityType.ForcedResponse`, resout APRES l'evenement de defaite (par opposition a
#   un Forced INTERRUPT, qui resoudrait AVANT -- mot-piege liste a l'etape 5 de PROCESSUS-CARTE.md : cette
#   carte dit bien « Response », jamais « Interrupt »).
# « AFTER this minion is defeated » -> `AbilityFactory.AfterUnitBeDefeated(AbilityType.ForcedResponse, "This",
#   ...)`. La defaite peut venir d'une attaque de joueur, d'un degat direct, ou de toute autre source : le
#   texte imprime NE restreint PAS la cause (pas de « ... is defeated BY an attack », contrairement a
#   d'autres cartes de ce pack comme hg010 « deals damage to a hero »), donc aucun filtre `by_attack=...`
#   n'est passe (laisse a `None`, c'est-a-dire aucune condition sur la cause de la defaite).
# « EACH player » -> `Worlds.GetPlayers(effect)`, boucle sur TOUS les joueurs de la partie, jamais un seul
#   joueur designe : contrairement a un « When Revealed » qui porte un `message.GetToPlayer()` precis, un
#   `AfterUnitBeDefeated` ne vise structurellement personne -- le texte dit explicitement « each player »,
#   donc la boucle est la lecture directe du mot-piege « each »/« for each » de l'etape 5, pas une
#   substitution de declencheur.
# « places 1 infection counter » -> `PoserInfection(effect, joueur, 1)`, valeur 1 explicite.
# Pas de choix de cible pour le joueur dans CETTE capacite, aucune Defense a proposer dans le script lui-meme
#   (la Reponse Forcee ne declenche aucun `DoActivate`) -- en TEST, en revanche, si la defaite de ce sbire est
#   provoquee par une vraie attaque/activation de joueur, le harnais exige l'option "passer_sur_option":
#   "Defense" (piege hg017, a ne pas repeter) ; le cas suggere ci-dessous l'evite en provoquant la defaite par
#   degat direct (`Puzzle.Damage`), ce qui suffit a declencher `AfterUnitBeDefeated` quelle que soit la cause.
#
# ---------------------------------------------------------------------------
# NOMBRES TEXTE <-> CODE (etape 6)
#
# cards_custom.json hg057 : {"SCH": "0", "ATK": "1", "HP": "5", "Guard": "1", "Boost": "2"} -- toutes natives,
# non reecrites ici.
# « 1 infection counter » -> `PoserInfection(effect, joueur, 1)`, `n=1` explicite (meme choix de style que
# hg037, qui precise `n=1` malgre la valeur par defaut du helper, pour que la valeur imprimee reste visible a
# la lecture).
#
# ---------------------------------------------------------------------------
# A CONFIRMER
#
# Aucun point laisse en suspens sur cette carte : la Reponse Forcee est une lecture directe du texte imprime,
# sans mot-cle maison non defini et sans valeur numerique ambigue. Seul point theorique, non observable avec
# les regles de ce scenario : si un effet futur empechait `AfterUnitBeDefeated` de partir pour une cause de
# defaite tres particuliere (aucune carte connue de ce pack ne le fait), cela resterait a verifier a ce
# moment-la -- rien dans le texte de Bloated Zombie ne le laisse envisager.


def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        Unused(message)
        for joueur in Worlds.GetPlayers(effect):
            PoserInfection(effect, joueur, 1)

    return [
        # `.NoOutOfPlayLimit()` : voir CORRECTIF en tete (sinon jamais declenchee pour sa propre defaite).
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.ForcedResponse,
            "This",
            vaincu,
        ).NoOutOfPlayLimit(),
    ]
