from . import *

# * Living Lightning (MIGUEL SANTOS) — ALLIE de campagne (Identity-Specific / Campaign, n° 233). Cout 2.
# THW 2 / ATK 2, 2 PV. AERIAL.
# Honorary.
# Response: After Living Lightning leaves play, discard the top 2 cards of your deck. For each printed
#   [energy] resource discarded this way, ready a card you control.
#
# Cartes de reference :
#  - **`game/ability/factory/card_move.py`** `AbilityFactory.AfterCardLeavePlay` : trigger natif « After
#    X leaves play ».
#  - **`core/spider_man/01002`** Black Cat : `initiator.DiscardDeckTopCards(2, effect)` + filtrage
#    `CardFinder(has_printed_res=...)`.
#  - **`falcon/falcon/53012`** Talon Line : `for _ in range(value): initiator.ChooseAbilities(effect,
#    AbilityFactory.ForChoiceAbility("Ready ...", lambda targets: Faces.ReadyAll(targets, effect))
#    .SetTarget(..., canbe_ready=True))` — repeter un choix « redresser 1 carte » autant de fois que le
#    compte calcule (ici 0, 1 ou 2, jamais plus que les 2 cartes defaussees).
#
# ⚠ Mots-pieges :
#  - « leaves play » : toute sortie (defaite, discard, retour en main...), pas seulement « defeated » ;
#  - « PRINTED [energy] resource » : l'icone IMPRIMEE des cartes defaussees, pas une ressource generee ;
#  - « a CARD you control » : n'importe quel type de carte en jeu sous son controle, pas seulement un
#    personnage (different de Talon Line qui visait des unites).
# ⚠ Étape 8 bis : redresser une carte change son etat visible : cas plateau a prevoir.


def GetAbilities() -> Sequence['Ability']:

    def living_lightning(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> None:
        Unused(message)
        joueur = effect.this.GetControlByPlayer()
        defaussees = joueur.DiscardDeckTopCards(2, effect)
        nombre = len(CardFinder(has_printed_res="Y").Checks(defaussees))
        for _ in range(nombre):
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Redresser une carte que vous controlez",
                    lambda targets: Faces.ReadyAll(targets, effect),
                ).SetTarget(CardFace, canbe_ready=True, from_where=["YouControlCards"]),
            )

    return [
        AbilityFactory.AfterCardLeavePlay(
            AbilityType.Response,
            "This",
            living_lightning,
        ),
    ]
