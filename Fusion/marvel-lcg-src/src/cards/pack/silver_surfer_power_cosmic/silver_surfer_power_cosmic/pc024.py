from . import *

# Hunger of Galactus — OBLIGATION. Give to the Silver Surfer player.
#
# Texte imprime :
#  « Treat the text box of each PLANET environment as blank. »
#  « Alter-Ego Action: Exhaust Cosmic Surfboard and choose a PLANET -> remove
#    that PLANET from the game. Discard this card. »
#
# CARTES DE REFERENCE
#  - `32063b` Stalked by Sabretooth (mut_gen) : `*AbilityFactory.
#    GiveKeywordToInPlayWhenApplyThis(CardFinder(...), treat_as_blank=True)`
#    -- modele EXACT pour « treat the text box of X as blank », applique a
#    toutes les cartes trouvees EN JEU tant que CETTE carte y est.
#  - `CostFunc.Exhaust(name="Cosmic Surfboard")` (pc001b.py) : « Exhaust
#    Cosmic Surfboard », meme carte nommee que l'Action de pc001b.
#  - `Faces.RemoveAllFromGame` + `Faces.DiscardAll([this], effect)` :
#    « remove that PLANET from the game. Discard this card. »
#
# TEXTE CONTRE CODE
#  « each PLANET ENVIRONMENT » : toute carte EN JEU portant le trait PLANET
#    (Zenn-La, Sakaar, Newhaven, Xandar, Black Hole, meme Ego le sbire qui
#    porte aussi ce trait) -- pas seulement les Support, le trait seul
#    decide.
#  « ALTER-EGO Action » : forme alter-ego seulement (`AlterEgoAction`, pas
#    `Action`).
#  « choose a PLANET -> remove THAT PLANET » : une seule, choisie par le
#    joueur parmi toutes celles en jeu.
#  « DISCARD this card » : toujours, meme cout paye et PLANET retiree
#    (l'Action se consomme elle-meme).


def GetAbilities() -> Sequence['Ability']:

    def retirer_une_planete(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this
        Unused(message)
        if effect.targets:
            Faces.RemoveAllFromGame(effect.targets, effect)
        Faces.DiscardAll([this], effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            # `traits=[...]` (pluriel) et non `trait=...` (singulier) :
            # cette derniere forme oblige `card_finder.params` a compter
            # EXACTEMENT 2 cles (`environment.py:135`, assert) pour calculer
            # un `OnEvent.Trait` de reevaluation -- hors de portee ici
            # puisque PLANET couvre DEUX familles de types de carte
            # (`Support` ET `Minion`, aucune base commune etroite a leur
            # donner). `traits` pluriel evite cette branche entierement.
            CardFinder(traits=["PLANET"]),
            treat_as_blank=True,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            retirer_une_planete,
        ).SetCostFunc(CostFunc.Exhaust(name="Cosmic Surfboard"))
        .SetTarget(trait="PLANET")
        .SetName("Remove a PLANET"),
    ]
