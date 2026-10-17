from . import *

# Martial Skill — AMELIORATION 1 [energy], Taijutsu (TMNT Shinobi, Inkwire). SKILL.
# Max 1 per player. Uses (2 chi counters).
# Response: After you play an event, exhaust Martial Skill and remove 1 chi counter from it → draw 1 card.
#
# Mots-cles (fiches lues AVANT le code) : Uses (uses.md ; `desc.Uses = "2,chi"`, compteur `chi` deja connu) ; Shinobi.
#
# Cartes de reference :
#  - « After you play an event » : `28002` Ms. Marvel (`AfterPlayerPlayedCard(Response, "You", Event, op)`) ;
#  - deux couts « exhaust X and remove 1 <compteur> counter from it → ... » : `tmnt_aspect_aggression/ua033` Pete
#    (`SetCostFunc(CostFunc.Exhaust("This"))` + `SetCostFunc(CostFunc.Counter("This", 1, 'pistol'))`) ;
#  - pose sans cible imprimee : `core/01057` Combat Training (amelioration, `MaxPerUnit`, defaut = votre identite).
#
# TEXTE CONTRE CODE
#  ⚠ « Max 1 per player » = `desc.MaxPerUnit = "1"` (regle native du selecteur d'amelioration).
#  ⚠ « Uses (2 chi counters) » : natif (`desc.Uses`) ; la carte quitte le jeu au DERNIER compteur retire : ne PAS coder la
#    sortie de jeu. La flèche est un COUT double (incliner ET retirer 1 compteur) : les deux payes ou aucun.
#  ⚠ « Response » nu (pas « Hero Response ») : declenche aussi en alter-ego ; « After YOU play an event » : tout
#    evenement joue par vous, pas une autre carte.


def GetAbilities() -> Sequence['Ability']:

    def martial_skill(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is not None:
            joueur.DrawUp(1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            Event,
            martial_skill,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'chi')),
    ]
