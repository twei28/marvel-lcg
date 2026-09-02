from . import *

# * Viv Vision (face alter-ego) — ANDROID.
# REC 3 — HS 6 / PV 10
# Recharge — Action: Choose a card with a printed [energy] resource in your
#   discard pile and place it on top of your deck. (Limit once per round.)
#
# Cartes de reference :
#  - ag001b * Sharon Carter (« Super Spy », meme auteur Rainy) : meme forme
#    exacte — une Action d'identite limitee une fois par round, qui CHOISIT
#    une carte dans une pile et la remet SUR un deck. Meme squelette
#    `AskChooseFace` + `Faces.MoveAllToDeck(..., "Top", effect)`, et meme
#    garde « pile vide -> on ne propose rien » ;
#  - al007 « See You Later! » pour la lecture de SA PROPRE defausse :
#    `joueur.discard_pile.Get(True)` puis filtrage par `CardFinder` ;
#  - le filtre de couleur IMPRIMEE vient de la famille 21006 / ho009
#    (`FacesCounter.GetPrintedResources`), mais ici il n'y a rien a compter :
#    `CardFinder(has_printed_res="Y")` suffit, et c'est le meme predicat que
#    le moteur applique dans `checker.py:424`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « a PRINTED [energy] resource » : la ressource IMPRIMEE sur la carte, pas
#    celle qu'on pourrait en tirer. Le checker du moteur lit
#    `face.printed_resource.HasOneOfColor([...], convert_green_res=False)` :
#    une carte a ressource WILD ne compte donc PAS comme energie, ce qui est
#    la lecture litterale du texte. Consequence concrete : vv007 Sparky the
#    Dog (wild) n'est jamais repechable, vv004/vv005/vv009/vv010 (energie) le
#    sont.
#  - « in YOUR discard pile » : la defausse du joueur, jamais celle de
#    rencontre. C'est l'ecart avec ag001b, qui vise la defausse de RENCONTRE.
#  - « place it ON TOP of your deck » : la position est un ARGUMENT
#    POSITIONNEL de `MoveAllToDeck`, pas un `to_top=` (piege §2 de
#    RECETTES-MOTEUR).
#  - « Choose » sans « you may » : le choix est obligatoire des qu'un
#    candidat existe. Aucun candidat -> l'action ne fait rien, comme la garde
#    de defausse vide d'ag001b.
#  - « (Limit once per round.) » : `.LimitOncePerRound()`.


def GetAbilities() -> Sequence['Ability']:

    def recharge(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return

        candidates = CardFinder(has_printed_res="Y").Checks(
            joueur.discard_pile.Get(True)
        )
        if not candidates:
            return

        choisie = joueur.AskChooseFace(
            candidates,
            effect,
            prompt="Place on top of your deck",
        )
        if choisie is None:
            return

        Faces.MoveAllToDeck([choisie], joueur.player_deck, "Top", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            recharge,
        ).SetName("Recharge")
        .LimitOncePerRound(),
    ]
