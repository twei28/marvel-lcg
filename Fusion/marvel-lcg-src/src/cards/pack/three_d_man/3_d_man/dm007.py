from . import *

# 3-D Man's Suit (Upgrade)
#
# Interrupt: When this card enters play from your hand, heal 1 damage from your identity.
# Hero Interrupt: When you play an event, discard 3-D Man's Suit -> reduce the cost of that event by 3.
#
# CARTES DE REFERENCE
#  - `il002` Stature (pack iron_lad) : "Response: After <this ally> enters play, heal 1 damage from your identity" ->
#    `this.HealthUnits([identity], N, effect)`. Difference : dm007 est un "Interrupt: When this enters play" (pas
#    "Response: After"), donc `AbilityFactory.WhenCardEnterPlay` (pas `AfterCardEnterPlay`), modele `hp011` Size
#    Manipulation (pack wasp_hank_pym) : `WhenCardEnterPlay(Interrupt, "This", op)`.
#  - `bg012` Utility Belt (Batgirl, OFFICIELLE) : TEXTE DE MEME FAMILLE ("When you would play an event, exhaust
#    this card -> reduce the cost of that event by 1"), corrigee par le FAQ RR en Hero ACTION qui arme la
#    reduction sur le PROCHAIN evenement joue ce tour (`Worlds.UpdateNextCardPlayCost(joueur, -N, effect,
#    finder=CardFinder(card_type=Event), in_this="Turn")`), parce que `WhenPlayerWouldPlayCard` arrive APRES le
#    paiement des ressources : impossible d'y reduire un cout en reaction. ARBITRAGE UTILISATEUR (04/11/2026,
#    meme blocage moteur rencontre sur bg012) : meme solution pour dm007 -> `AbilityType.HeroAction` au lieu du
#    "Hero Interrupt" imprime, qui arme la reduction en defaussant 3-D Man's Suit, a utiliser AVANT de jouer
#    l'evenement vise (comme Batgirl), plutot qu'au moment ou on le joue.
#  - `an006` Angelic Ribbons (Angela) : "discard this card" est un COUT, `CostFunc.Discard("This")`.
#
# TEXTE CONTRE CODE
#  "from your hand" : aucune autre carte du pack ne peut mettre 3-D Man's Suit en jeu autrement qu'en le jouant
#    depuis la main (pas de recherche/mise en jeu directe dans ce kit) -> pas de condition de provenance a coder,
#    `WhenCardEnterPlay` suffit (modele hp011, qui ne filtre pas non plus la provenance).
#  "that event" -> `finder=CardFinder(card_type=Event)` (modele bg012) : seulement un evenement, pas une
#    amelioration/allie/soutien.
#  "by 3" -> -3 (valeur NEGATIVE, la fabrique ne descend jamais sous 0).
#
# Chiffres : heal 1 ; reduction -3, "Turn" (meme portee que bg012).

def GetAbilities() -> Sequence['Ability']:

    def suit_entree_en_jeu(effect: 'Effect', message: 'Message.WhenCardEnterPlay') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        this.HealthUnits([identite], 1, effect)

    def armer_reduction_prochain_evenement(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        joueur = effect.GetInitiator()
        Worlds.UpdateNextCardPlayCost(
            joueur, -3, effect,
            finder=CardFinder(card_type=Event),
            in_this="Turn",
        )

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenCardEnterPlay(
            AbilityType.Interrupt,
            "This",
            suit_entree_en_jeu,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            armer_reduction_prochain_evenement,
        ).SetCostFunc(CostFunc.Discard("This")),
    ]
