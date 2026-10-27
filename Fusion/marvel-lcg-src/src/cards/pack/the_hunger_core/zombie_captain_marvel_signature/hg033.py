from . import *

# VERIFIE (27/10/2026, passe de fusion hg028-hg076) : `commun.DECKS_SIGNATURE["Zombie Captain Marvel"]` =
# [hg030, hg031, hg032, hg033, hg033, hg033] N'EST PAS une erreur de recopie. Le livret (p. 4, repris en tete
# de `DECKS_SIGNATURE` dans commun.py) dit « 3 cards; 5 for Zombie Iron Man and 6 for Zombie Captain Marvel »,
# et `data/encounter_sets/the_hunger_core_sig_zombie_captain_marvel.json` liste hg033 en TROIS exemplaires :
# 4 cartes distinctes, 6 cartes au total. Liste laissee telle quelle.
#
# Energy Hunger — TRAITRISE (deck signature de Zombie Captain Marvel, carte 4/4, derniere du set). Trait
# COSMIC.
# When Revealed: Place 2 energy counters on Zombie Captain Marvel (max. 5).
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - « energy counter » n'est PAS un mot-cle maison/officiel a fiche dediee (absent de
#   `docs/reference/mots-cles/README.md` comme entree a part) : le compteur 'energy' existe DEJA nativement
#   (`CardFace.COUNTER`), deja pose cote Metazombie par `hg011` Zombie Captain Marvel elle-meme (« Absorption »,
#   Forced Response, max. 5) et deja lu par ses +1 ATK par compteur. Cette carte ne fait qu'ajouter des
#   compteurs supplementaires sur la MEME jauge, par un canal different (une revelation de son propre deck
#   signature, pas une attaque subie) -- aucune fiche a ouvrir, aucun ajout a `card_face.py`.
# - [[horde-metazombies]] (mots-cles/horde-metazombies.md) : cette carte est elle-meme une carte du deck
#   signature de Zombie Captain Marvel (`commun.DECKS_SIGNATURE["Zombie Captain Marvel"]` contient `hg033`,
#   TROIS fois, comme le veut le livret « 6 for Zombie Captain Marvel » : 4 cartes distinctes, 6 au total) ;
#   elle n'est
#   revelee QUE lorsque son propre deck signature est consulte (`commun.RevelerLeDessusDuDeckSignature`,
#   appelee sur `LeMetazombieActif(effect)`), ce qui implique que Zombie Captain Marvel EST en jeu au moment
#   ou cette carte se revele (son deck signature n'existe que lie a sa propre `Card`,
#   `commun._DeckSignatureAttr`). Garde defensive conservee malgre tout (meme lecture que `hg023` Hunger
#   Protocol) : aucune regle du livret ne garantit formellement ce lien pour une revelation future hors de ce
#   chemin (ex. un effet qui piocherait une signature card au hasard) -- ici, a defaut, rien ne se passe (pas
#   de clause « if you cannot » imprimee sur cette carte, a la difference de hg023).
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « Place 2 energy counters on Zombie Captain Marvel (max. 5) » : modele EXACT `hg011` Zombie Captain Marvel
#   elle-meme (« place 1 energy counter on this card (max. 5) ») -> `Faces.PlaceCountersOn([cible], 2,
#   'energy', effect, maximum=5)`. Seule difference : la cible n'est pas `this` (hg033 n'est pas le Metazombie,
#   c'est une carte de traitrise de son deck signature) mais le Metazombie identifie par son NOM -- modele
#   `hg023` Hunger Protocol (« If Zombie Iron Man has 2 or more attachments ») : `v.IsName("Zombie Captain
#   Marvel")` parmi `Metazombies(effect)` (liste deja filtree sur le trait METAZOMBIE et sur « vivant/en
#   jeu »).
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE (etape 5, mots-pieges)
#
# « When Revealed » -> `AbilityFactory.WhenThisRevealed`, declencheur a la revelation de CETTE carte
#   (`Condition2.ThisIsTrigger` deja integre a la fabrique, aucune garde a ajouter).
# « Place 2 energy counters ON ZOMBIE CAPTAIN MARVEL » -> identification par NOM parmi `Metazombies(effect)`,
#   jamais `LeMetazombieActif(effect)` (qui pourrait, en theorie, designer un AUTRE Metazombie si le jeton a
#   bouge entre la pose en jeu et la consultation du deck signature -- aucun cas connu du scenario ne le fait,
#   mais le texte imprime NOMME explicitement « Zombie Captain Marvel », pas « the active Metazombie »,
#   contrairement a `hg017` ou au mecanisme generique du jeton).
# « (max. 5) » -> parametre `maximum=5` de `Faces.PlaceCountersOn`, qui clampe le TOTAL apres pose (si elle
#   porte deja des compteurs 'energy' au moment de cette revelation -- par exemple via sa propre Absorption,
#   `hg011` -- la pose est reduite d'autant, jamais au-dela du plafond) : comportement natif de
#   `CanPlaceCounter.PlaceCountersInternal` (`src/game/card/face/attribute/can_place_counter.py:58-60`), pas
#   une borne a recoder a la main.
# Pas d'activation, pas d'attaque, pas de degats sur cette carte : aucune Defense a proposer (contrairement au
#   piege hg017 sur les activations reelles).
#
# ---------------------------------------------------------------------------
# NOMBRES TEXTE <-> CODE (etape 6)
#
# « 2 energy counters » (texte imprime, `data/cards_custom.json` hg033) <-> `Faces.PlaceCountersOn([...], 2,
#   'energy', effect, maximum=5)`.
# « max. 5 » <-> `maximum=5`.
# Deux valeurs numeriques sur cette carte, les deux verifiees, OK.
#
# ---------------------------------------------------------------------------
# A CONFIRMER
#
# Aucun point laisse en suspens sur le TEXTE de cette carte (pas de mot-cle maison, pas de limite imprimee,
# pas de choix pour le joueur, pas de plateau a dessiner au-dela de la jauge de compteurs deja existante sur
# le Metazombie). Les trois exemplaires de cette carte dans le deck signature sont voulus (voir l'en-tete).


def GetAbilities() -> Sequence['Ability']:

    def faim_energetique(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        captain_marvel = next((v for v in Metazombies(effect) if v.IsName("Zombie Captain Marvel")), None)
        if captain_marvel is None:
            # Garde defensive (voir fiche horde-metazombies ci-dessus) : ne devrait pas arriver en pratique.
            return
        Faces.PlaceCountersOn([captain_marvel], 2, 'energy', effect, maximum=5)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            faim_energetique,
        ),
    ]
