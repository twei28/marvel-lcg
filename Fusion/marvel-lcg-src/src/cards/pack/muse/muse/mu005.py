from . import *

# Grim Inspiration — TRAITRISE. Deferlement, 1 icone de boost.
# Surge.
# When Revealed: Each player chooses an identity-specific card in their discard
#   pile and places it on top of their deck. Give Muse and the villain a
#   facedown boost card.
#
# CARTES DE REFERENCE
#  - `vv001b` * Viv Vision : choisir une carte de SA défausse et la poser sur
#    le dessus du deck, `AskChooseFace` puis
#    `Faces.MoveAllToDeck([carte], joueur.player_deck, "Top", effect)`.
#  - `27086` * Mysterio pour `Players.ForEachPlayer`.
#  - `02007` Hired Gun pour `Faces.GiveFacedownBoostCards`.
#
# ⚠ C'EST CETTE CARTE QUI TRANCHE TOUT LE SET. L'auteur y ecrit noir sur blanc
# « an IDENTITY-SPECIFIC card », la ou les quatre autres disent « l'image de
# votre identite ». C'est ce qui a fait retenir la carte signature comme
# lecture des quatre (decision utilisateur du 13/09/2026).
#
# TEXTE CONTRE CODE
#  ⚠ « Surge » : BASE AUTOMATIQUE, `desc.Surge = "1"` comme `01191` Exhaustion
#    et `01193` Under Fire. AUCUN script : `ThisCardGainSurge` dans le corps
#    de la capacite l'aurait donne UNE SECONDE FOIS, et la traitrise aurait
#    revele deux cartes au lieu d'une. Defaut attrape par
#    `verifier_coherence_cartes.py`, qui a signale « Surge imprime, cle desc
#    absente ».
#  ⚠ « EACH player CHOOSES » : chaque joueur choisit lui-meme, ce n'est pas le
#    premier joueur qui decide pour tout le monde.
#  ⚠ Un joueur SANS carte signature en defausse ne fait rien : la carte ne dit
#    pas « si vous ne pouvez pas ». Aucun repli, aucune penalite.
#  ⚠ « Muse AND the villain » : les DEUX recoivent une carte de boost. Si Muse
#    n'est pas en jeu, le vilain recoit quand meme la sienne — la carte ne
#    conditionne pas l'un a l'autre.


def GetAbilities() -> Sequence['Ability']:

    def grim_inspiration(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(message, this)

        def remonter(joueur: 'Player') -> None:
            candidates = CartesSignatureDe(list(joueur.discard_pile.Get(True)))
            if not candidates:
                return
            choisie = joueur.AskChooseFace(
                candidates, effect, prompt="Place on top of your deck")
            if choisie is not None:
                Faces.MoveAllToDeck([choisie], joueur.player_deck, "Top", effect)

        Players.ForEachPlayer(effect, remonter)

        cibles: List['CardFace'] = []
        muse = TrouverMuse(effect)
        if muse is not None:
            cibles.append(muse)
        vilain = Worlds.FindVillain(effect)
        if vilain is not None:
            cibles.append(vilain)
        if cibles:
            Faces.GiveFacedownBoostCards(cibles, 1, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            grim_inspiration,
        ),
    ]
