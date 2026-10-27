from . import *

# CORRECTIF (27/10/2026, passe de fusion hg028-hg076) : « put one into play WITH damage equal to half its hit
# points » decrit l'ETAT dans lequel la carte entre en jeu, pas des degats INFLIGES par une source. L'ancien
# `metazombie.DealDamage([metazombie], degats, effect)` passait par `TakeDamage` : Zombie Captain America (hg007,
# « Shield : the first time each phase he would take damage, reduce that damage by 2 ») ou un Metazombie Tenace
# absorbaient une partie de ces degats, et le resultat dependait du Metazombie tire au hasard du Horde deck.
# Remplace par `metazombie.SetHealth(max_health - degats, effect)` (PV courants regles directement, modele
# `03008`/`62014` qui posent aussi un etat de PV sans infliger de degats). Arrondi inchange : `// 2` (vers le bas).
#
# Half-Eaten — TREACHERY (set partage « The Hunger Core », carte 3/5 de hg046-hg050). Pas de trait imprime.
# Boost 2.
# When Revealed: If there are fewer than 3 Metazombies in play, put one into play with damage equal to half
# its hit points. Otherwise, this card gains Surge.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - [[surge]] (mots-cles/surge.md) : « this card gains Surge » -> `ThisCardGainSurge(effect, message)`
#   (helper `cards/pack/__init__.py:111`), meme modele que `hg046`/`hg047`.
# - [[horde-metazombies]] (mots-cles/horde-metazombies.md) : « put one into play » = `commun.
#   MettreUnMetazombieEnJeu`, qui prend le DESSUS du Horde deck courant (remelange avec sa defausse si
#   besoin, rend `None` si les deux sont vides) et replafonne lui-meme a `MAX_METAZOMBIES_EN_JEU` en interne.
#   Rend le `Villain` pose (ou `None`), ce qui permet d'enchainer les degats sur la MEME instance.
# - « with damage equal to half its hit points » : AUCUNE fiche mots-cles/ dediee -- ce n'est pas un mot-cle
#   nomme en gras dans le texte imprime (contrairement a « Surge »), seulement une clause de degats directs
#   accolee a une mise en jeu, deja couverte par le gabarit generique des degats directs (hg016/hg025/hg030 :
#   `cible.DealDamage([cible], N, effect)` sur une Unit2 deja en jeu). Rien a ouvrir.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - Structure if/else identique MOT POUR MOT a `hg047` Rise of the Horde! (meme condition « fewer than 3 »,
#   meme branche Surge en « otherwise ») : seule la branche « put one into play » gagne une clause
#   supplementaire ici (les degats).
# - « ... with damage equal to half its hit points » (du Metazombie qu'on vient de poser, pas d'un autre) :
#   modele de degats directs sur une Unit2 juste entree en jeu, `villain.DealDamage([villain], degats,
#   effect)`, meme appel que `coeur.DealDamage([coeur], ..., effect)` dans `the_hunger_core/__init__.py`
#   (Rupture X). « ITS hit points » = les PV MAXIMUM du Metazombie qu'on vient de poser (`villain.max_health`,
#   proprete deja fiable des la sortie de `MettreUnMetazombieEnJeu` : `Unit2.__init__` appelle `ResetHealth`
#   a la CONSTRUCTION de la face via `CardFactory.GenerateCard`, donc `max_health` est deja correctement
#   positionne -- y compris une eventuelle mise a l'echelle `[per_hero]` -- avant meme que la carte ne soit
#   mise en jeu). PAS `.health` (les PV RESTANTS, qui valent encore `max_health` a cet instant puisque rien
#   ne l'a encore blesse -- utiliser `.health` ou `.max_health` donnerait donc le MEME nombre ici, mais le
#   texte dit « hit points », pas « hit points remaining » comme `nv003` : `.max_health` est la lecture la
#   plus proche du texte).
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE (etape 5, mots-pieges)
#
# « When Revealed » -> `AbilityFactory.WhenThisRevealed`, declencheur a la revelation de CETTE carte (pas de
#   ciblage sur un joueur precis, le texte ne dit « against you » ni « to you »).
# « IF there are fewer than 3 Metazombies in play » -> `NbMetazombiesEnJeu(effect) < MAX_METAZOMBIES_EN_JEU`,
#   verifie EN PREMIER, avant toute action (meme lecture que hg047).
# « put ONE into play » (indefini) -> un seul appel a `MettreUnMetazombieEnJeu(effect, joueur)`, qui prend
#   toujours le dessus du Horde deck courant.
# « WITH DAMAGE equal to half its hit points » -> degats appliques SEULEMENT si la pose a reussi (`villain`
#   non None) ; le Metazombie entre en jeu DEJA blesse, aucune attaque ni activation n'est impliquee (pas de
#   `DoActivate`, donc le piege hg017 de la Defense ne s'applique pas ici).
# « half its hit points » -> arrondi NON precise par le texte imprime : retenu a l'ARRONDI VERS LE BAS (regle
#   par defaut du jeu en l'absence d'indication contraire, meme lecture que `03026` Captain America, « half
#   of the cards in your hand, rounded down »), `degats = metazombie.max_health // 2`. Marque A CONFIRMER
#   ci-dessous (le livret/FAQ officiel de ce scenario fan-made ne tranche pas explicitement).
# « OTHERWISE, this card gains Surge » -> branche mutuellement exclusive avec la pose + les degats (if/else
#   strict), identique a hg047.
#
# ⚠ Mot-piege A CONFIRMER : sens de l'arrondi de « half its hit points » (retenu : vers le bas, `// 2`,
# meme defaut que `03026`). Verifie dans `data/cards_custom.json` : PLUSIEURS des 9 Metazombies ont des PV
# imprimes IMPAIRS (hg008 Zombie Iron Man "11*", hg009 Zombie Hulk "15*", hg010 Zombie Spider-Man "9*",
# hg012 Zombie Thor "13*", hg013 Zombie Black Widow "9*" -- le "*" = mise a l'echelle par joueur, deja
# resolue dans `max_health` au moment ou cette carte le lit). L'arrondi choisi change donc REELEMENT le
# nombre de degats dans ce scenario (ex. Zombie Iron Man pose a 2 joueurs, 22 PV -> 11 degats pile ; a 3
# joueurs, 33 PV -> 16 au lieu de 17 si l'arrondi etait vers le haut) : a confirmer en partie reelle si le
# livret officiel (pages 3-6, rien trouve de plus precis) ou une FAQ tranche dans l'autre sens.
#
# ⚠ Mot-piege A CONFIRMER (identique a hg047) : le texte imprime n'envisage que deux cas (« fewer than 3 » /
# sinon Surge). Si `MettreUnMetazombieEnJeu` rendait `None` alors que la condition `< 3` etait vraie (Horde
# deck ET sa defausse tous deux vides, cas limite non atteignable avec 9 Metazombies au total pour un
# plafond de 3), aucun degat n'est applique (rien a blesser) et aucune branche Surge n'est declenchee non
# plus (meme lecture defensive que hg047 : la garde imprimee porte sur le NOMBRE en jeu, pas sur le resultat
# de la pose).
#
# ---------------------------------------------------------------------------
# NOMBRES TEXTE <-> CODE (etape 6)
#
# « Boost: 2 » (texte imprime, `data/cards_custom.json` hg048 : `"desc": {"Boost": "2"}`) : badge natif,
#   rien a coder.
# « fewer than 3 Metazombies » -> `MAX_METAZOMBIES_EN_JEU` (deja = 3 dans `commun.py`, identique au « 3 »
#   imprime ici, sur hg015 et sur hg047).
# « half » -> `// 2` (arrondi vers le bas, voir mot-piege ci-dessus). Pas d'autre valeur numerique imprimee.
# « Surge » gagne dynamiquement n'a pas de chiffre imprime sur CETTE carte : `ThisCardGainSurge` pose
#   toujours 1 Surge (`this.GainSurge(1, by_effect)`), coherent avec hg046/hg047.


def GetAbilities() -> Sequence['Ability']:

    def half_eaten(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        if NbMetazombiesEnJeu(effect) < MAX_METAZOMBIES_EN_JEU:
            joueur = message.GetToPlayer()
            metazombie = MettreUnMetazombieEnJeu(effect, joueur)
            if metazombie is not None:
                degats = metazombie.max_health // 2
                if degats > 0:
                    # « put into play WITH damage » : degats POSES, pas infliges (voir CORRECTIF en tete).
                    metazombie.SetHealth(metazombie.max_health - degats, effect)
        else:
            ThisCardGainSurge(effect, message)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            half_eaten,
        ),
    ]
