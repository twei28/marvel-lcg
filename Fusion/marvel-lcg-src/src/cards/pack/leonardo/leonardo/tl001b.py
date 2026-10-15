from . import *

# * Leo (face alter-ego) — TEENAGER. MUTANT. TURTLE.
# REC 3 — HS 6 / PV 12
# Action: Discard 1 card from your hand -> search your deck and discard pile
#   for up to 2 [[KATANA]] upgrades and put them into play, exhausted.
#   (Shuffle.)
#
# Cartes de reference :
#  - `ls005` Lady Sif / `40059` Superpower Training : `Search.PlayerCard(...,
#    include_player_deck=True, include_discard_pile=True, ...)` et
#    `face.PutIntoPlay(player, effect)` pour un « put into play » depuis le
#    deck ET la defausse ;
#  - `ra026` / `45080` : coût `CostFunc.Discard("YourHandCards", ...)` ;
#  - `Faces.ExhaustAll` pour « exhausted » a l'entree.
#
# Mots-pieges :
#  - « Discard 1 card from your hand -> » : dans le COUT. Pas de carte en main
#    = capacite non proposee ;
#  - « UP TO 2 » : deux recherches successives, chacune `may=True` (le joueur
#    peut s'arreter a 0 ou 1) ;
#  - « (Shuffle.) » : comportement par defaut de la fouille ;
#  - « put them into play, EXHAUSTED » : on incline apres la mise en jeu (insert
#    du pack : « they enter play exhausted ») ;
#  - Action NUE sur l'alter-ego (comme ls001b) ;
#  - Katana `Restricted` mis en jeu par effet : la limite (2 Restricted) ne
#    gene pas ici (le pack n'a que DEUX katanas, Restricted 1 chacun). A
#    verifier en jeu (phase C) que `PutIntoPlay` ne leve rien sur Restricted.


def GetAbilities() -> Sequence['Ability']:

    def leo(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return

        for _ in range(2):
            face = Search.PlayerCard(
                effect,
                joueur,
                include_player_deck=True,
                include_discard_pile=True,
                trait="KATANA",
                card_type=Upgrade,
                may=True,
            )
            if not face:
                break
            face.PutIntoPlay(joueur, effect)
            Faces.ExhaustAll([face], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            leo,
        ).SetCostFunc(CostFunc.Discard("YourHandCards", range=(1, 1))),
    ]
