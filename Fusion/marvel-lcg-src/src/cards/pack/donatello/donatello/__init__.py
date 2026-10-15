from cards.pack import *

# ===========================================================================
# Helpers partages du set « Donatello » (Inkwire, TMNT Heroes, prefixe `td`).
#
# ⚠ HOMONYMES verifies avant montage (aucun dans cards.json ni
# cards_custom.json) : Donatello, Donnie, Metalhead, Bo Tobu, Chudan-Ura-Uke,
# Improvised Tactics, Singularity, Inspired Brilliance, Donnie's Lab,
# Anti-Gravity Gauntlet, Truevision Goggles, Donatello's Bo / Shell, Broken
# Shell, Extermination!, Baxter Stockman (« Baxter Building » mf004 n'est pas un
# homonyme), Plague of M.O.U.S.E.R.s, Flight of Flyborgs.
#
# ⚠ LES NOMS UNIQUES S'ECRIVENT SANS L'ETOILE dans `CardFinder(name=...)`
# (RECETTES-MOTEUR §6). Et le « o » MACRON de « Donatello's Bō » est un
# caractere non ASCII : on cherche donc ces deux cartes par `card_ids`, jamais
# par nom.
# ===========================================================================

ID_GANTELET = "td009"   # Anti-Gravity Gauntlet
ID_BO = "td011"         # Donatello's Bō
ID_CARAPACE = "td012"   # Donatello's Shell
NOM_CARAPACE = "Donatello's Shell"   # ASCII pur : « discard Donatello's Shell from play »


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit (modele sunfire).

    ⚠ NE PAS se rabattre sur `effect.GetInitiator()` en premier : il leve un
    assert quand l'initiateur n'est pas un joueur, et le moteur AVALE
    l'exception.
    """
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if Player.IsType(controleur):
            return controleur
    initiateur = getattr(effect, "initiator", None)
    if initiateur is not None and Player.IsType(initiateur):
        return initiateur
    return None


STATUTS = ("Stunned", "Confused", "Tough")


def StatutsPresents(face: 'CardFace') -> List[str]:
    return [nom for nom in STATUTS if face.HasStatus(nom)]


def RetirerUneCarteDeStatut(effect: 'Effect', joueur: 'Player', face: 'CardFace') -> bool:
    """« Discard a status card from an enemy » : UNE carte de statut, au choix
    du joueur quand l'ennemi en porte plusieurs.

    ⚠ `Faces.RemoveStatus` N'EXISTE PAS (dazzler/__init__.py:262) : le retrait
    est une methode de la FACE, `DiscardStunned/Confused/Tough(effect, rule=1)`.
    """
    presents = StatutsPresents(face)
    if not presents:
        return False
    methodes = {"Stunned": face.DiscardStunned,
                "Confused": face.DiscardConfused,
                "Tough": face.DiscardTough}
    if len(presents) == 1:
        methodes[presents[0]](effect, rule=1)
        return True
    joueur.ChooseAbilities(
        effect,
        *[AbilityFactory.ForChoiceAbility(
            "Discard a %s status card" % nom,
            lambda cibles, nom=nom: methodes[nom](effect, rule=1))
          for nom in presents])
    return True
