from . import *

# Pride — amelioration d'aspect BASIC (n° 30). CONDITION. SUPERPOWER.
# Cout 2 [wild]. Max 1 per player.
# Action: Exhaust Pride → discard the top card of your deck. If that card is an
#   identity-specific card, add it to your hand.
#
# Cartes de reference :
#  - **`09004`** Magic Blast / `01050` Hulk : `initiator.DiscardDeckTopCard(effect)`.
#  - **`26007`** Density Control : `card_class="IdentitySpecific"`, le filtre
#    moteur des cartes propres a une identite.
#  - `16033` Salvage / `40037b` pour `GainCard` (remettre en main).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **identity-specific** card » : carte signature (classe Hero) de
#    N'IMPORTE quel heros — en pratique les tiennes, puisqu'elles seules sont
#    dans ton deck.
#  - « add **it** to your hand » : la carte defaussee, depuis la defausse.
#  - Sinon la carte RESTE defaussee (pas de « otherwise »).
#  - « Max 1 per player » : desc.MaxPerUnit (convention 01018, 01063).
#  - « Action » nue, cout « exhaust → », pas de limite (l'inclinaison suffit).


def GetAbilities() -> Sequence['Ability']:

    def fierte(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        joueur = effect.GetInitiator()
        face = joueur.DiscardDeckTopCard(effect)
        if face is None:
            return
        if CardFinder(card_class="IdentitySpecific").Check(face):
            joueur.GainCard(face, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            fierte,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
