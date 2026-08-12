from . import *

# * Cho's Lab — custom « Rainy »
# Hero Response: After you change form, exhaust Cho's Lab → put the bottom card
#   of your deck into your reserve.
# Alter-Ego Action: Exhaust Cho's Lab → shuffle a Brawn card from your discard
#   pile into your deck.
#
# « After you change form » se lit sur AfterUnitChangeForm, et la clause
# « Hero » impose que la forme d'ARRIVEE soit le heros : c'est le passage en
# heros qui alimente la reserve, pas le retour en alter-ego.

def GetAbilities() -> Sequence['Ability']:

    def carte_du_dessous_en_reserve(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        joueur = effect.GetInitiator()
        dessous = joueur.player_deck.GetBottom()
        if dessous is None:
            return
        MettreEnReserve([dessous], joueur, effect)

    def remelanger_une_carte_brawn(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        joueur = effect.GetInitiator()
        candidates = CardFinder(set_name="Brawn").Checks(joueur.discard_pile.Get())
        if not candidates:
            return

        choisie = joueur.AskChooseFace(candidates, effect, not_move=True)
        if choisie is None:
            return
        Faces.ShuffleAllTo([choisie], joueur.player_deck, effect)

    return [
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.HeroResponse,
            "You",
            carte_du_dessous_en_reserve,
            to_form=Hero,
        ).SetCostFunc(CostFunc.Exhaust("This")),

        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            remelanger_une_carte_brawn,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
