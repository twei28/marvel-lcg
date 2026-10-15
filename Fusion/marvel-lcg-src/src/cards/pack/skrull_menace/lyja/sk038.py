from . import *

# * Human Torch (Johnny Storm) — ALLIE FANTASTIC FOUR. Cout 3, THW 1★, ATK 2★, 3 PV.
# Response: After Human Torch leaves play, search the encounter deck for a TREACHERY
#   card, shuffle the encounter deck, and place that card on the top of the encounter
#   deck.
#
# Cartes de reference :
#  - **`27023`** Web of Life and Destiny : `AfterCardLeavePlay(Response, ...)`, la
#    Reponse a la sortie de jeu d'une carte.
#  - **`sf009`** Burning : la fabrique accepte "This" ; pour "This" elle pose
#    elle-meme `NoOutOfPlayLimit` (card_move.py:252) : la Reponse part alors que
#    l'allie est deja en defausse.
#  - sk037a (meme dossier) : la recherche + la pose sur le dessus du deck rencontre.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « AFTER Human Torch leaves play » : Reponse (apres), pas une Interruption.
#  - « leaves play » : defaite, defausse, retour en main... toute sortie de jeu.
#  - THW 1★ / ATK 2★ : l'etoile = degats consequentiels (desc « 1* » / « 2* »).


def GetAbilities() -> Sequence['Ability']:

    def apres_depart(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this, message)

        joueur = effect.GetInitiator()
        trouvees = ChercherTraitrisesRencontre(effect, joueur, 1)
        PoserSurLeDeckRencontre(effect, joueur, trouvees)

    return [
        AbilityFactory.AfterCardLeavePlay(
            AbilityType.Response,
            "This",
            apres_depart,
        ),
    ]
