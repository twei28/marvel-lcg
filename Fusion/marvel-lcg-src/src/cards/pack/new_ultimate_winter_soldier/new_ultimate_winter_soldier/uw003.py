from . import *

# * Phoenix (Jean Grey) — allie EARTH-6160. Cout 3, PV 3, ATK 1*, THW 2*, [physical].
# Hero Interrupt: When Phoenix is discarded from your hand at random, put her into play under your control.
#
# Cartes de reference : `ap101` / `27087b` (« When you would discard this card from your deck » : une Interruption
# sur `WhenCardWouldDiscard` posee sur la carte elle-meme, `NoOutOfPlayLimit` + `NoGameAreaLimit` parce qu'elle est
# EN MAIN) ; `27040` / `27018` (`face.PutIntoPlay(joueur, effect)` pour un allie).
#
# Mots-pieges : « discarded from your hand AT RANDOM » (une defausse CHOISIE ne declenche rien : la marque
# `world.defausses_au_hasard` posee par `DiscardRandomHandCards`) ; « Hero Interrupt » (forme heros seulement) ;
# « put her into play » : a la place de la defausse (`SetBeInstead`). Son cout imprime (3) compte quand meme comme
# « that card » pour le X de la carte qui l'a tiree.


def GetAbilities() -> Sequence['Ability']:

    def phoenix(effect: 'Effect', message: 'Message.WhenCardWouldDiscard') -> None:
        this = effect.this.CastTo(Ally)
        joueur = this.GetOwnerPlayer()
        message.SetBeInstead(effect)
        this.PutIntoPlay(joueur, effect)

    return [
        AbilityFactory.WhenCardWouldDiscard(
            AbilityType.HeroInterrupt,
            "This",
            phoenix,
            conditions=[lambda effect, message: DefausseAuHasard(message)],
        ).NoOutOfPlayLimit().NoGameAreaLimit(),
    ]
