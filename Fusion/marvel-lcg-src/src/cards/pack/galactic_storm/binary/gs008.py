from . import *

# White Hole — SOUTIEN, cout 2, [physical]. LOCATION. Binary 11/15.
# Hero Action: Exhaust White Hole → discard cards from the top of your deck
#   until you discard a card with a printed [energy] resource. Add that card to
#   your hand.
#
# Cartes de reference :
#  - **`iron_fist/64002`** Deep Breathing : « discard ... until you discard X.
#    Add that card to your hand » = `joueur.DiscardDeckUntil(effect, <filtre>)`
#    puis `Faces.AddToHand([face], joueur, effect)`.
#  - filtre de ressource imprimee : `CardFinder(has_printed_res="Y")` (`checker.py`
#    : `HasOneOfColor(..., convert_green_res=False)`, le wild ne compte pas).
#  - **`core/01091`** pour « Exhaust X → » sur un soutien.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « HERO Action » : forme heros seulement (contre-cas en alter ego).
#  - « a card with a PRINTED [energy] resource » : la ressource imprimee de la
#    carte DANS LE DECK (Energy Conversion ne vise que la main) ; Energy Torrent
#    (YY) et Energy (YY) comptent, Solar Flare (Y) aussi ; un wild seul non.
#  - « ADD THAT card to your hand » : la carte trouvee seulement, les autres
#    restent dans la defausse.
#  - Aucune carte [energy] dans le deck : tout le deck est defausse (regle du
#    deck epuise du moteur), rien n'est ajoute.
#  ⚠ `Deck.DiscardUntil` rend None quand il VIDE le deck, meme si la derniere
#    carte defaussee est la cherchee (piege RECETTES §7unvicies, `deck.py`).
#    On repere donc la carte visee AVANT la defausse, et on la rend si le
#    moteur l'a perdue de vue (cas « l'Energy est la derniere carte du deck »).


def GetAbilities() -> Sequence['Ability']:

    def trou_blanc(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        visee = None
        for carte in joueur.player_deck.Get(True):
            if CardFinder(has_printed_res="Y").Check(carte):
                visee = carte
                break
        face = joueur.DiscardDeckUntil(effect, has_printed_res="Y")
        if face is None and visee is not None and not visee.IsInPlay() \
                and visee not in joueur.hand_cards.Get():
            face = visee
        if face is not None:
            Faces.AddToHand([face], joueur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            trou_blanc,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
