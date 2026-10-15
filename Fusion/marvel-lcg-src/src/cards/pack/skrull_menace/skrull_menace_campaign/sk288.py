from . import *

# * Sy-Torak Gem — AMELIORATION de campagne (Aggression / Campaign, n° 288). Cout 2. ARTIFACT.
# Play under any player's control.
# You get +3 hit points.
# Your hero gets +1 ATK.
# Forced Interrupt: When your deck empties, spend [energy] resource. If you cannot, discard Sy-Torak Gem.
#
# Cartes de reference :
#  - **`cw/56013`** Aggressive Conditioning : le MEME texte « Play under any player's control / You get +3 hit
#    points / your hero gets +1 ATK » = `CanPlayThisUpgradeCard("Players")` + `GiveKeywordToAttached("You",
#    health=3)` + `GiveKeywordToAttached(Hero, attack=1)`.
#  - **`aa012`** Regained Youth : « after your deck runs out of cards » = `AfterDeckRunOut(..., deck_du_joueur, ...)`
#    (message `AfterDeckRunOut`, card.py:526 : le DERNIER tirage du deck) ; le moteur n'a pas de message « when »
#    (TODO « Pre message », sender_deck.py:40) : la fenetre est « after ».
#  - **`fne/60127`** Tug of War : « You may spend X resources. Otherwise ... » = `ChooseAbilities(
#    ForChoiceAbilityWithCost(cout, nom, op, conditions=[payable]), Otherwise(op2))` + `PeutCouvrirLeCout`
#    (la branche payante n'est offerte que si le cout est couvrable).
#
# ⚠ Mots-pieges :
#  - « spend [energy] resource » : UNE ressource [energy] (une carte [energy] de la main ou de la reserve) ; wild
#    et [energy] imprimees comptent (`PeutCouvrirLeCout`) ; « If you CANNOT, discard » : la defausse est la branche
#    « Otherwise », jamais offerte quand le joueur peut payer ;
#  - « YOUR deck » (le deck du porteur) ; « YOUR HERO gets +1 ATK » : heros seulement (contre-cas alter ego) ;
#  - Forced Interrupt : obligatoire (mais le moteur le declenche apres le dernier tirage).


def GetAbilities() -> Sequence['Ability']:

    def mon_deck(effect: 'Effect') -> 'Deck':
        return effect.this.GetControlByPlayer().player_deck

    def deck_vide(effect: 'Effect', message: 'Message.AfterDeckRunOut') -> None:
        this = effect.this.CastTo(Upgrade)
        joueur = this.GetControlByPlayer()

        def peut_payer(effet_choix: 'Effect', message_choix: 'Message.WhenPlayerChooseAbility') -> bool:
            return PeutCouvrirLeCout(joueur, effet_choix, Cost("Y"))

        def garder(targets: Sequence['CardFace'], res: 'Resources') -> None:
            Unused(targets, res)

        def defausser(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            Faces.DiscardAll([this], effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbilityWithCost(
                Cost("Y"),
                "Spend [energy]: keep Sy-Torak Gem",
                garder,
                conditions=[peut_payer],
            ),
            AbilityFactory.Otherwise(defausser),
        )

    return [
        AbilityFactory.CanPlayThisUpgradeCard("Players"),
        *AbilityFactory.GiveKeywordToAttached("You", health=3),
        *AbilityFactory.GiveKeywordToAttached(Hero, attack=1),
        AbilityFactory.AfterDeckRunOut(
            AbilityType.ForcedInterrupt,
            mon_deck,
            deck_vide,
        ),
    ]
