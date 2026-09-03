from . import *

# Kickflip — evenement signature, x4 (n/16 = 5 a 8), le plus nombreux du deck.
# ATTACK. SKILL. Cout 1, ressource [physical].
# If the last card you played this round was a Night Thrasher event, reduce
#   the cost to play this card by 1.
# Hero Action (attack): Flip the Battle Board upgrade and deal 1 damage to an
#   enemy. Draw 1 card.
#
# Cartes de reference :
#  - `05015` Tackle / `im002` pour l'evenement d'attaque a libelle.
#  - **`ReduceCostToPlayThis(1, conditions=[...])`** (resources.py:586) pour la
#    reduction conditionnelle, modele `16024` Deft Focus.
#  - **`player.stat.this_round_played_cards`** (player_stat.py:8) : le moteur
#    tient DEJA la liste des cartes jouees ce round, dans l'ordre. C'est la
#    seule source pour « the LAST card you played this round », et elle evite
#    d'ajouter un compteur maison.
#  - `RetournerLaPlanche` (helper du set), `bt023` pour `DrawUp`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « the **LAST** card you played this round » : la DERNIERE, pas « une
#    quelconque ». D'ou `[-1]` sur la liste, jamais un `any(...)`.
#  - « a **Night Thrasher** event » : un evenement de CE set (`set_name`),
#    pas n'importe quel evenement, et pas une carte d'aspect. Les quatre
#    candidats sont nt002 Disaster, nt004 Drop In, nt006 Melon Grab et
#    nt007 Tailblock — et Kickflip elle-meme, ce qui en fait une chaine.
#  - « this **round** » : au round, pas au tour. La liste
#    `this_round_played_cards` est la bonne des deux (`this_turn_played_cards`
#    existe aussi juste a cote, et serait plus restrictive).
#  - ⚠ La reduction est evaluee au moment du CALCUL DU COUT, avant que
#    Kickflip elle-meme ne rejoigne la liste : c'est bien la carte
#    PRECEDENTE qui est lue. Un cas de test qui joue deux evenements a la
#    suite est le seul moyen de le prouver.
#  - « Flip the Battle Board upgrade **and** deal 1 damage » : les deux, sans
#    condition sur la face. Kickflip est la seule carte du pack qui retourne
#    la planche SANS rien lire dessus.
#  - « Draw 1 card » : la pioche tombe de toute facon, meme sans planche.


def GetAbilities() -> Sequence['Ability']:

    def evenement_du_pack_juste_avant(effect: 'Effect', message: 'Message2') -> bool:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return False
        # ⚠ KICKFLIP EST DEJA DANS LA LISTE quand son cout se calcule : le
        # moteur enregistre la carte jouee AVANT `WhenCalculateEffectCost`. Sans
        # ce filtre, Kickflip se voit ELLE-MEME comme « la derniere carte jouee
        # ce round », la condition est toujours vraie, et la reduction devient
        # PERMANENTE — la carte coute 0 des le premier exemplaire. Mesure : le
        # journal du cas montrait « would play Kickflip with () » sur la
        # PREMIERE copie (03/09/2026).
        jouees = [f for f in joueur.stat.this_round_played_cards if f is not effect.this]
        if not jouees:
            return False
        derniere = jouees[-1]
        return Event.IsType(derniere) and derniere.paper.set_name == "Night Thrasher"

    def kickflip(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        RetournerLaPlanche(effect)
        this.DealDamage(effect.targets, 1, effect)

        initiator = effect.GetInitiator()
        if initiator is not None:
            initiator.DrawUp(1, effect)

    return [
        AbilityFactory.ReduceCostToPlayThis(
            1,
            conditions=[evenement_du_pack_juste_avant],
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            kickflip,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
