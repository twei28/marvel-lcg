from . import *

# Rise of the Horde! — TREACHERY (set partage « The Hunger Core », carte 2/5 de hg046-hg050). Pas de trait
# imprime. Boost 3.
# When Revealed: If there are fewer than 3 Metazombies in play, put one into play. Otherwise, this card gains
# Surge.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - [[surge]] (mots-cles/surge.md) : « this card gains Surge » -> `ThisCardGainSurge(effect, message)`
#   (helper `cards/pack/__init__.py:111`), modele EXACT `hg023` Hunger Protocol (meme paire if/else, meme
#   branche « rien ne s'est passe -> Surge »).
# - [[horde-metazombies]] (mots-cles/horde-metazombies.md, deja ouverte au portage de hg004a/hg005b/hg015) :
#   « put one into play » = `commun.MettreUnMetazombieEnJeu`, qui prend le DESSUS du Horde deck courant
#   (remelange avec sa defausse si besoin, rend `None` si les deux sont vides) et replafonne lui-meme a
#   `MAX_METAZOMBIES_EN_JEU` en interne.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « If there are fewer than 3 Metazombies in play, put one into play. Otherwise, this card gains Surge » :
#   clause MOT POUR MOT deja anticipee par le commentaire de `hg015` Zombie Magik (« Portal to Limbo »), qui
#   cite EXPLICITEMENT cette carte comme destinataire des deux helpers `NbMetazombiesEnJeu` et
#   `MettreUnMetazombieEnJeu` de `commun.py`. Meme structure if/else que `hg023` Hunger Protocol : la branche
#   qui reussit (« put one into play ») n'a pas de clause d'echec propre, la branche qui echoue
#   (« otherwise ») est celle qui gagne Surge.
# - « there are FEWER THAN 3 Metazombies in play » : identique au mot pres a la condition de hg015
#   (`NbMetazombiesEnJeu(effect) < MAX_METAZOMBIES_EN_JEU`), relue au moment de la resolution, pas figee a
#   l'entree de l'ability.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « When Revealed » -> `AbilityFactory.WhenThisRevealed`, declencheur a la revelation de CETTE carte (pas de
#   ciblage sur un joueur precis, le texte ne dit « against you » ni « to you »).
# « IF there are fewer than 3 Metazombies in play » -> `NbMetazombiesEnJeu(effect) < MAX_METAZOMBIES_EN_JEU`,
#   verifie EN PREMIER, avant toute action.
# « put ONE into play » (indefini, pas « the next one » ni un Metazombie nomme) -> un seul appel a
#   `MettreUnMetazombieEnJeu(effect, joueur)`, qui prend toujours le dessus du Horde deck courant.
# « OTHERWISE, this card gains Surge » -> branche mutuellement exclusive (if/else strict) : seul le cas « 3
#   Metazombies deja en jeu » declenche `ThisCardGainSurge`. Si `MettreUnMetazombieEnJeu` rendait `None` alors
#   que la condition `< 3` etait vraie (Horde deck ET sa defausse tous deux vides — cas limite non couvert par
#   le texte imprime, qui ne distingue pas « aucun Metazombie disponible » de « 3 deja en jeu »), on reste
#   dans la lecture la plus proche du texte : la garde imprimee porte sur le NOMBRE en jeu, pas sur le
#   resultat de la pose ; aucune branche Surge n'est declenchee dans ce cas (meme lecture que la garde
#   defensive de hg023, mais ici le texte ne laisse pas de place a un troisieme cas -- marque ci-dessous
#   A CONFIRMER).
#
# ⚠ Mot-piege A CONFIRMER : le texte imprime n'envisage que deux cas (« fewer than 3 » / sinon Surge), alors
# que le moteur permet un troisieme etat theorique (moins de 3 Metazombies en jeu, mais Horde deck ET defausse
# tous deux vides -- improbable avec 9 Metazombies au total pour un plafond de 3, jamais vu dans les decks de
# ce scenario, mais pas structurellement impossible si une autre carte retirait des Metazombies DU JEU sans
# repasser par la defausse du Horde deck). Choix retenu : ne pas donner Surge dans ce cas (le texte imprime ne
# le demande pas, seul le cas « 3 ou plus en jeu » le declenche) -- a confirmer en partie reelle si ce
# troisieme cas devient un jour atteignable.
#
# Pas de choix de cible pour le joueur, aucune valeur numerique dans ce script au-dela de celles deja
# centralisees dans `commun.py` (`MAX_METAZOMBIES_EN_JEU = 3`, identique au « 3 » imprime ici ET sur hg015).


def GetAbilities() -> Sequence['Ability']:

    def rise_of_the_horde(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        if NbMetazombiesEnJeu(effect) < MAX_METAZOMBIES_EN_JEU:
            joueur = message.GetToPlayer()
            MettreUnMetazombieEnJeu(effect, joueur)
        else:
            ThisCardGainSurge(effect, message)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            rise_of_the_horde,
        ),
    ]
