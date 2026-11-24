from . import *

# Forced Leave — Obligation (set « U.S. Agent »), Boost 1, « Give to the John Walker player ».
# Flip to alter-ego form. Choose:
#  • Exhaust John Walker and discard U.S. Agent's Shield → remove this obligation from the game.
#  • Discard 1 card from your hand at random → discard this obligation.
#
# Cartes de reference :
#  - `th011` Annual Shedding (meme auteur) : « Flip to alter-ego form. » SANS « may » =
#    `if joueur.IsHero(): identite.ChangeToForm(AlterEgo, effect)` (le helper `YouMayFlipToYourAlterEgoForm` est reserve aux
#    obligations qui disent « You MAY flip »).
#  - `ch018` Family Ties (meme auteur) : `WhenThisObligationGiveToYou` + `joueur.ChooseAbilities` avec `condition=` par
#    branche, et les DEUX sorties differentes (retirer de la partie / defausser).
#  - `Player.DiscardRandomHandCards(n, effect)` : « discard N cards from your hand at random ».
#
# ⚠ Mots-pieges :
#  - « Flip » obligatoire : si on est deja alter ego, rien ne bouge ; apres la bascule le choix se fait EN alter ego, donc
#    l'identite est John Walker et peut s'incliner.
#  - 1re branche : COUT = incliner John Walker (doit etre PRET) ET defausser le bouclier EN JEU (sans bouclier ou sans
#    John Walker pret, la branche n'est pas offerte) ; sortie « REMOVE FROM THE GAME ».
#  - 2e branche : defausse AU HASARD de 1 carte (sans carte en main, defausse a vide) ; sortie « DISCARD this obligation » :
#    l'obligation retourne dans le deck de rencontre (hc013 : elle reste en jeu tant qu'on ne la deplace pas).
def GetAbilities() -> Sequence['Ability']:

    def forced_leave(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetGaveToPlayer()
        if joueur is None:
            return
        if joueur.IsHero():
            joueur.GetIdentity().ChangeToForm(AlterEgo, effect)
        identite = joueur.GetIdentity()

        def partir_en_conge(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            Faces.RemoveAllFromGame([this], effect)

        def defausser_au_hasard(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            joueur.DiscardRandomHandCards(1, effect)
            Faces.DiscardAll([this], effect)

        bouclier = Worlds.FindCardsOnField(effect, name=NOM_BOUCLIER, card_type=Upgrade)
        bouclier_a_soi = [b for b in bouclier if b.GetControlBy() == joueur]
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust John Walker and discard U.S. Agent's Shield → remove this obligation from the game",
                partir_en_conge,
                condition=(joueur.IsAlterEgo() and identite is not None and identite.CanExhaust()
                           and len(bouclier_a_soi) > 0),
            ).SetCostFunc(CostFunc.Exhaust("YourIdentity"))
            .SetCostFunc(CostFunc.Discard("YouControlCards", name=NOM_BOUCLIER, card_type=Upgrade)),
            AbilityFactory.ForChoiceAbility(
                "Discard 1 card from your hand at random → discard this obligation",
                defausser_au_hasard,
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            forced_leave,
        ),
    ]
