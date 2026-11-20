from . import *

# * Carnage (face HEROS) : AVENGER. SYMBIOTE. THW 1 / ATQ 2 / DEF 2, main 5, PV 12.
# Death-Dealer — Response: After you attack and defeat an enemy, heal 1 damage from Carnage for each point of excess damage dealt by that attack.
# Need to Kill — Forced Response: At the end of the round, if you did not defeat an enemy this round, take damage equal to your ATK.
#
# CARTES DE REFERENCE
#  - Death-Dealer : `ar005` (Ares' Battle Helm) : `AfterUnitDefeatedUnit(.., "You", Enemy, op, is_from_attack=True, has_excess_damage=True)` + `message.excess_damage` ;
#    soin : `HealthUnits([cible], n, effect)` (`my001b`).
#  - Need to Kill : `61040` (pack jj) `AfterRoundEnd(ForcedResponse)` pour « at the end of the round » ; `jj` `RecordSideSchemeDefeat` pour le marqueur « ce round » ;
#    `rz016` (Weighed Down) `this.DealDamage([joueur.GetIdentity()], n, effect)` pour « take N damage ».
#
# TEXTE CONTRE CODE
#  « After YOU attack AND defeat an enemy » : `"You"` + `is_from_attack=True` (une defaite par un allie ou par un effet sans attaque ne declenche pas). « an ENEMY » : le vilain compte.
#  « for each point of EXCESS damage » : `message.excess_damage` (avec `has_excess_damage=True` la Reponse n'est meme pas proposee quand l'exces vaut 0). « heal ... FROM CARNAGE » : l'identite.
#  « if YOU did not defeat an enemy THIS ROUND » : tout ennemi vaincu par le joueur (attaque ou effet) ce round annule la Reponse forcee. « damage equal to YOUR ATK » : l'ATK COURANTE de l'identite
#    (+1 de Frenzied Violence compris), lue au moment de la resolution.
#  Chiffres : PV 12, main 5, ATQ 2, CTR 1, DEF 2.


def GetAbilities() -> Sequence['Ability']:

    def mort_donnee(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        joueur = JoueurDeCetteCarte(effect)
        exces = int(getattr(message, "excess_damage", 0) or 0)
        if joueur is None or exces <= 0:
            return
        effect.this.HealthUnits([joueur.GetIdentity()], exces, effect)

    def besoin_de_tuer(effect: 'Effect', message: 'Message.AfterRoundEnd') -> None:
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        degats = int(identite.attack or 0)
        if degats > 0:
            effect.this.DealDamage([identite], degats, effect)

    def pas_de_victoire(effect: 'Effect', message: 'Message.AfterRoundEnd') -> bool:
        joueur = JoueurDeCetteCarte(effect)
        return joueur is not None and not AVaincuUnEnnemiCeRound(effect, joueur, message.round_id)

    return [
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.Response,
            "You",
            Enemy,
            mort_donnee,
            is_from_attack=True,
            has_excess_damage=True,
        ).SetName("Death-Dealer"),
        AbilityFactory.AfterRoundEnd(
            AbilityType.ForcedResponse,
            besoin_de_tuer,
            conditions=[pas_de_victoire],
        ).SetName("Need to Kill"),
        NoterVictoire(),
    ]
