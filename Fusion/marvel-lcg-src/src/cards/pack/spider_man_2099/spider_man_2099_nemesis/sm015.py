from . import *

# * Electro — SBIRE nemesis. 4 PV, SCH 2, ATQ 1. Boost 2. ANDROID.
# Quickstrike. Retaliate 1.
# [star] Forced Response: After Electro attacks you, discard the top 4 cards
#   of your deck. Take 1 indirect damage for each [energy] resource discarded
#   this way.
#
# CARTES DE REFERENCE
#  - `sm014` Containment Breach (meme set) : le meme decompte d'icones
#    energie sur des cartes defaussees, par l'helper commun `IconesEnergie`.
#  - `24027`, `40187` Reaper, `38031` Bonebreaker : « Forced Response: After
#    <ennemi> attacks you » — le declencheur est `AfterUnitAttackEnd` cote
#    ennemi, avec le joueur ATTAQUE lu sur le message, jamais devine.
#  - `al022` * Frogjolnir (pack alligator_loki) : LE calque. « Forced Response:
#    After <ennemi> attacks you, take N indirect damage » s'ecrit
#    `AfterUnitAttackYou(ForcedResponse, "This", op)` — la fabrique pose
#    elle-meme `against_who="You"` (do_attack.py:690) — et le joueur attaque se
#    lit par `message.GetAgainstPlayer()`, jamais par un `to_player` devine.
#    Les degats indirects passent par
#    `identite.TakeIndirectDamage(this, N, effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « After Electro attacks YOU » : « you » designe le joueur ATTAQUE, et
#    c'est lui qui defausse et encaisse — pas le premier joueur, pas le
#    proprietaire de la nemesis. En solo les deux coincident : l'ecart ne se
#    voit qu'a deux joueurs (`heros2`).
#    ⚠⚠ Une carte de rencontre EN JEU n'a PAS de controleur joueur : le joueur
#    se lit sur le MESSAGE (`GetAgainstPlayer`). C'est la lecon payee sur
#    `bl011` The Thirst le 07/09/2026 (« The Thirst activait sans rien
#    faire »), et `AfterUnitAttackYou` garantit en plus qu'un Electro qui
#    frappe un AUTRE joueur ne fait rien defausser a celui-ci.
#  ⚠ « FORCED Response » : pas de choix, la capacite part toute seule. Aucun
#    `conditions` a poser pour eviter une question — il n'y en a pas.
#  ⚠ « discard the top 4 cards » PUIS « for each [energy] resource discarded
#    THIS WAY » : on ne compte que ces 4 cartes-la, pas la defausse entiere.
#  ⚠ « INDIRECT damage » : c'est le joueur qui repartit les degats, pas un
#    ciblage. `Quickstrike` et `Retaliate 1` sont des BASES AUTOMATIQUES lues
#    dans `desc` (RECETTES §3) : aucun script pour elles.
#  ⚠ L'etoile imprimee a cote de « 1 ATK » n'est pas une valeur de jeu : chez
#    Rainy elle pointe la statistique visee par la capacite etoile de la carte
#    (ici l'attaque). Meme convention que `bl013` Dracula.
#  ⚠ Aucune limite imprimee : etape 7 bis sans objet.


def GetAbilities() -> Sequence['Ability']:

    def decharge(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Minion)

        joueur = message.GetAgainstPlayer()
        if joueur is None:
            return

        defaussees = joueur.DiscardDeckTopCards(4, effect)
        if not defaussees:
            return

        energie = IconesEnergie(defaussees)
        if energie <= 0:
            return

        identite = joueur.GetIdentity()
        if identite is not None:
            identite.TakeIndirectDamage(this, energie, effect)

    return [
        AbilityFactory.AfterUnitAttackYou(
            AbilityType.ForcedResponse,
            "This",
            decharge,
        ),
    ]
