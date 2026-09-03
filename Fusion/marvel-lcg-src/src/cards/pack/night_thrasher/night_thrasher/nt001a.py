from . import *

# * Night Thrasher — face HEROS. PV 9, ATQ 1, CTR 1, DEF 1, main 5.
# AVENGER. NEW WARRIOR.
# Varial Heelflip — Response: After you play a [[SKILL]] card, flip the Battle
#   Board upgrade. (Limit once per phase.)
#
# Cartes de reference :
#  - **`as001b`** * Peter Parker (pack armored_spidey) : meme forme de
#    declencheur, `AfterPlayerPlayedCard(Response, "You", <filtre>, op)`, ou
#    `"You"` teste `message.to_player` — le destinataire de la carte jouee.
#  - `17022` * Knowhere pour le meme motif avec un filtre de trait.
#  - **`15001a`** * Scarlet Witch pour `.LimitOncePerPhase()`, rare dans le
#    depot : la plupart des cartes limitent au ROUND.
#  - `RetournerLaPlanche` (helper du set) pour le retournement lui-meme.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « After you play a [[SKILL]] card » : le TRAIT, pas le type. Un
#    evenement, une amelioration ou un allie SKILL declenchent tous. Dans ce
#    pack, cinq cartes signature portent SKILL (nt004, nt005, nt006, nt007,
#    nt011), plus les cartes d'aspect Justice du deck.
#  - « (Limit once per **phase**.) » : PAS par round. `LimitOncePerPhase()`,
#    et surtout pas `LimitOncePerRound()` — la difference se voit tout de
#    suite, la planche pouvant alors basculer plusieurs fois par round.
#  - « flip the Battle Board upgrade » : le retournement est l'EFFET, pas un
#    cout. Sans planche en jeu, la capacite resout sans rien faire — c'est le
#    seul cas ou elle peut etre inerte, et il ne se produit pas en partie
#    normale puisque `nt003a` porte `desc.Setup`.
#  - « Response » NUE, pas « Hero Response » : elle marche aussi en forme
#    civile... sauf que cette capacite est imprimee sur la face HEROS, donc
#    elle n'existe qu'en forme heros. Rien a conditionner en plus.
#  - Statistiques MINUSCULES (1/1/1) : c'est deliberé, la planche vaut la
#    moitie de la fiche du heros.


def GetAbilities() -> Sequence['Ability']:

    def varial_heelflip(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this, message)

        RetournerLaPlanche(effect)

    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            CardFinder(trait="SKILL"),
            varial_heelflip,
        ).SetName("Varial Heelflip")
        .LimitOncePerPhase(),
    ]
