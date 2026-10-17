from . import *

# Integrity — AMELIORATION OATH, classe Bushido (Inkwire, TMNT Shinobi). Cout 2, [physical].
# Response: After you play an OATH upgrade, exhaust this card -> place 1 samurai counter on an OATH upgrade you control.
# « Actions speak louder than words. » —Odyn
#
# Mots-cles (fiches lues AVANT le code) : samurai counter / OATH (samurai-counter.md). Pas de Uses : Integrity ne porte pas de
# compteur elle-meme (elle est OATH, donc cible possible de son propre effet).
#
# Cartes de reference :
#  - « After you play a <filtre> » : `jennika/tj008` Jennika's Bow / `michelangelo/tm011` (`AfterPlayerPlayedCard(Response, "You",
#    CardFinder(card_type=..., trait=...), op)`), cout `CostFunc.Exhaust("This")` ;
#  - poser un compteur sur UNE carte choisie : `PlacerUnCompteurSamurai` (helper du pack, `ChooseAbilities` + `SetTarget`).
#
# TEXTE CONTRE CODE
#  ⚠ « After YOU play an OATH UPGRADE » : une AMELIORATION portant le trait OATH, JOUEE par le joueur (pas mise en jeu par un
#    effet, pas une autre sorte de carte). Integrity est elle-meme une amelioration OATH : le moteur envoie le message apres
#    SA propre mise en jeu, donc elle peut repondre a sa propre pose (cas dedie).
#  ⚠ « exhaust this card -> » : COUT ; une seule reponse par redressement (deux OATH jouees d'affilee : la 2e ne declenche rien).
#  ⚠ « 1 samurai counter on AN OATH upgrade YOU control » : UN compteur, sur une amelioration OATH SOUS SON CONTROLE, au choix
#    du joueur ; Integrity (OATH) peut se choisir elle-meme (aucune restriction imprimee), meme sans Uses.


def GetAbilities() -> Sequence['Ability']:

    def integrity(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        PlacerUnCompteurSamurai(effect, effect.GetInitiator())

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            CardFinder(card_type=Upgrade, trait="OATH"),
            integrity,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
