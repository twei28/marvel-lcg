from . import *

# Glory — AMELIORATION OATH, classe Bushido (Inkwire, TMNT Shinobi). Cout 0, [mental]. Pas de citation.
# Max 1 per player.
# Hero Response: After your hero defeats a side scheme, discard this card -> place a total of 4 samurai counters among any
#   number of OATH upgrades you control.
#
# Mots-cles (fiches lues AVANT le code) : samurai counter / OATH (samurai-counter.md). « Max 1 per player » : base automatique
# (`desc.MaxPerUnit = "1"`, controle nomme dans `CanPlayThisUpgradeCard`). Pas de Uses : Glory ne porte aucun compteur elle-meme.
#
# Cartes de reference :
#  - « After you defeat a minion OR side scheme » : `tmnt_shinobi_paths/se008` Onigari (`AfterUnitDefeatedScheme(HeroResponse, "You",
#    SchemeSide2, op)`) ; le moteur n'a que cette fabrique pour « vaincre un complot » ;
#  - « discard this card -> » en cout : `CostFunc.Discard("This")` (modele `nebu/22014` Justice Served : Hero Response d'amelioration a cout « discard this card ») ;
#  - « place counters among any number of cards you control » : `PlacerUnCompteurSamurai` (helper du pack), un compteur a la fois
#    au choix du joueur, comme la repartition de `se003` (retrait un a un).
#
# TEXTE CONTRE CODE
#  ⚠ « After YOUR HERO defeats a SIDE scheme » : un complot ANNEXE (ni le complot principal, ni un sbire) ; vaincu par le heros,
#    pas par un allie ; la forme heros seule (Hero Response).
#  ⚠ « discard THIS card -> » est devant la FLECHE : c'est un COUT, paye avant l'effet ; Glory n'est donc PLUS une cible
#    possible pour ses propres compteurs (elle est partie).
#  ⚠ « a TOTAL of 4 ... among ANY NUMBER of OATH upgrades YOU control » : 4 compteurs en tout, repartis librement (tous sur une
#    seule amelioration ou un par carte) ; seulement des OATH SOUS SON CONTROLE ; sans amelioration OATH restante les compteurs
#    ne se placent pas (le cout est paye quand meme).
#  ⚠ Une amelioration OATH n'a pas de plafond de compteurs : on ne borne pas.


def GetAbilities() -> Sequence['Ability']:

    def glory(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        for _ in range(4):
            if not PlacerUnCompteurSamurai(effect, joueur):
                break

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterUnitDefeatedScheme(
            AbilityType.HeroResponse,
            "You",
            SchemeSide2,
            glory,
        ).SetCostFunc(CostFunc.Discard("This")),
    ]
