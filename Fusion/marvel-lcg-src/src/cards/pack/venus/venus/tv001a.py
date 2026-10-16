from . import *

# * Venus (face heros) — NINJA. TEMPORAL. TURTLE. PV 10, ATQ 1, CTR 2, DEF 2, main 4.
# Action: Place 1 dredge counter on Venus for each [[ELEMENT]] upgrade you control
#   (to a maximum of 6). (Limit once per round.)
#
# CARTES DE REFERENCE
#  - `tr001a` / `tr009` (pack raphael) : compteur maison pose sur l'IDENTITE par
#    `Faces.PlaceCountersOn([identite], n, 'rage', effect, maximum=3)`. Ici `dredge`.
#  - `ra001a` (pack rainy) : `WhenInYourPlayTurn(Action/HeroAction, op).LimitOncePerRound()`.
#
# TEXTE CONTRE CODE
#  ⚠ « for EACH [[ELEMENT]] upgrade YOU CONTROL » -> `ElementsControles(joueur)` : les
#    ameliorations ELEMENT du joueur seulement (trait, pas nom), zero = zero compteur.
#  ⚠ « (to a MAXIMUM of 6) » -> DECISION UTILISATEUR (16/10/2026, Q1) :
#    lecture CONFIRMEE = PLAFOND DU STOCK (Venus ne porte jamais plus de
#    6 compteurs de dragage, comme le plafond « to a maximum of 3 » de la rage de
#    Raphael, `maximum=6`). Autre lecture : plafonner seulement le nombre pose par
#    activation (aucun effet pratique : il n'existe que 6 ameliorations ELEMENT).
#  ⚠ « Limit once per round » -> `LimitOncePerRound()`, temoin d'epuisement dans les cas.
#  Pas de nom d'action imprime : aucun `SetName`.


def GetAbilities() -> Sequence['Ability']:

    def draguer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        n = len(ElementsControles(joueur))
        # DECISION UTILISATEUR Q1 : plafond du stock (6), voir l'en-tete.
        PlacerDragage(effect, n, joueur, maximum=PLAFOND_DREDGE)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            draguer,
        ).LimitOncePerRound(),
    ]
