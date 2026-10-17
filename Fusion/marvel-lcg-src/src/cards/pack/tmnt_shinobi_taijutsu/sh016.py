from . import *

# * Jō — AMELIORATION unique 2 [energy], Taijutsu (TMNT Shinobi, Inkwire). NINJA. WEAPON.
# Restricted. Uses (3 cudgel counters).
# Response: After you play a Taijutsu event, place 1 cudgel counter here.
# Hero Response: After you damage an enemy, remove 2 cudgel counters from this card → daze that enemy.
#
# Mots-cles (fiches lues AVANT le code) : Uses (uses.md ; `desc.Uses = "3,cudgel"`, compteur `cudgel` ajoute a
# `CardFace.COUNTER`) ; Restricted (natif, `desc.Restricted`) ; Dazed (dazed.md) ; Shinobi (shinobi.md).
#
# Cartes de reference :
#  - « place 1 X counter here » apres une carte jouee : `61017` / `tmnt_aspect_justice` (`PlaceCountersInternal(n,
#    '<compteur>', effect, maximum=...)`), ici SANS maximum ; declencheur « After you play ... » : `18010` Gamora's
#    Sword (`AfterPlayerPlayedCard(Response, "You", finder, op)`) ;
#  - « After you deal damage to an enemy ... remove N counters → ... that enemy » : `tmnt_aspect_aggression/ua033`
#    Pete (`AfterYouDealDamage(Response, Enemy, op)` + `CostFunc.Counter("This", n, '<compteur>')`, cible
#    `message.who_took_damage`) ; portee Q-T4 resolue le 17/10/2026 (identite + cartes jouees, lecture confirmee).
#
# TEXTE CONTRE CODE
#  ⚠ « a TAIJUTSU event » : un EVENEMENT de classe Taijutsu (CardFinder card_classes=["Taijutsu"]) ; « place 1 counter
#    here » : AUCUN plafond imprime, les compteurs peuvent depasser 3 (Uses ne fixe que le nombre d'entree).
#  ⚠ « remove 2 cudgel counters FROM THIS CARD → daze » : cout de 2 compteurs (impossible avec 1) ; si ce cout vide
#    la carte (`Uses`) elle part SANS effet de plus : le sort est quand meme resolu (le cout est paye avant).
#  ⚠ « After YOU damage an enemy » : portee de « you » : voir Q-T4. « THAT enemy » : celui qui vient de prendre des
#    degats.
#  ⚠ Hero Response : forme heros seulement ; Response nue : tout joueur forme.


def GetAbilities() -> Sequence['Ability']:

    def jo_poser(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        this.PlaceCountersInternal(1, 'cudgel', effect)

    def jo_hebeter(effect: 'Effect', message: 'Message.AfterFaceDealDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        cibles = [x for x in (message.who_took_damage or []) if Enemy.IsType(x) and x.IsInPlay()]
        if cibles:
            ShinobiDaze(effect, cibles[:1])

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            CardFinder(card_type=Event, card_classes=["Taijutsu"]),  # type: ignore
            jo_poser,
        ),
        AbilityFactory.AfterYouDealDamage(
            AbilityType.HeroResponse,
            Enemy,
            jo_hebeter,
        ).SetCostFunc(CostFunc.Counter("This", 2, 'cudgel')),
    ]
