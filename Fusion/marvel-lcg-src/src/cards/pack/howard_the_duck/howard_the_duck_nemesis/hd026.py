from . import *

# A Fowl Plot — manigance annexe nemesis, menace 2*, Boost 3, ACCELERATION 1
# When Revealed: Discard an upgrade you control. If no cards were discarded
#   this way, place 1 threat on the main scheme and take 1 damage.
#
# ACCELERATION est un mot-cle AUTOMATIQUE lu dans `desc.Acceleration`
# (has_acceleration_icon.py) : aucun code. L'icone imprimee a ete verifiee par
# decoupe d'image (pointe + BARRE DE SOULIGNEMENT, temoin `ag011`) — voir
# l'encadre de `docs/reference/mots-cles/acceleration.md`. Ne pas la confondre
# avec l'icone HAZARD de hd022 (carte penchee nue, sans barre).
#
# « Discard an UPGRADE you control » : `player.GetControlCardsByType
# (CardFinder(canbe_discard=True), upgrade=True)` (player_get.py:107-143),
# meme montage que hd023 pour « ally or support » — piege `you control` du
# tableau.
#
# CORRECTIF (30/08/2026, trouve par autoplay, partie 1/8) : sans
# `canbe_discard=True`, la carte proposait hd017 Nexus of all Realities —
# une amelioration PERMANENTE, qui ne peut pas quitter le jeu. Le moteur
# plantait alors sur `assert controller.is_eliminated`
# (card_face.py:463-473), AssertionError en pleine partie. Le filtre
# `canbe_discard` (checker.py:169-171) ecarte exactement les cartes
# permanentes et les identites — donc, ici, la seule amelioration permanente
# du kit. C'est aussi la regle : une carte permanente ne se defausse pas, et
# la branche « If no cards were discarded this way » doit s'appliquer si
# c'est la seule amelioration en jeu.
# « If NO CARDS were discarded this way » : la condition porte sur la
# defausse REELLEMENT effectuee (`Faces.DiscardAll` rend la liste des cartes
# effectivement parties, faces.py:8-20), pas sur le simple fait qu'il y avait
# une amelioration en jeu — une amelioration indefaussable laisserait bien la
# branche de repli s'appliquer.
# Repli : DEUX operations dans la meme branche (piege `and remove` du tableau,
# « aucune partie oubliee ») — `this.PlaceThreatOnSchemes("MainScheme", 1,
# effect)` (card_face.py:574, litteral "MainScheme" prevu) ET
# `identite.TakeDamage(this, 1, effect)` (« take 1 damage » = l'identite du
# joueur vise subit le degat, modele core/01061.py Great Responsibility).


def GetAbilities() -> Sequence['Ability']:

    def a_fowl_plot(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)

        player = message.GetToPlayer()
        if player is None:
            return

        defaussees: List['CardFace'] = []
        upgrades = player.GetControlCardsByType(
            CardFinder(canbe_discard=True), upgrade=True,
        )
        if upgrades:
            cible = upgrades[0] if len(upgrades) == 1 else player.AskChooseFace(upgrades, effect)
            if cible is not None:
                defaussees = Faces.DiscardAll([cible], effect)

        if not defaussees:
            this.PlaceThreatOnSchemes("MainScheme", 1, effect)
            player.GetIdentity().TakeDamage(this, 1, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            a_fowl_plot,
        ),
    ]
