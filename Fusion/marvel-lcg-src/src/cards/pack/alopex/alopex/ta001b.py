from . import *

# * Alopex (face alter-ego) — FOX. MUTANT. TEENAGER.
# REC 3 — HS 6 / PV 9
# Setup: Set your Prey upgrade aside.
# Action: Discard 1 card from your hand -> search your deck and discard pile
#   for up to 2 [[KAMA]] upgrades and put them into play, exhausted.
#   (Shuffle.)
#
# Cartes de reference :
#  - Setup « mise de cote » : `bt001b` / `sf001b` / `09001b` :
#    `AbilityFactory.BeginGameWithSetAside([...])` FABRIQUE la carte dans
#    `joueur.additional_discard_pile` (= `set_aside_deck`). Ce n'est PAS le
#    champ `set_aside` du deck de depart, que le moteur ne lit pas en vraie
#    partie (PROCESSUS-HEROS etape 3). Prey est la 16e carte du deck imprime
#    (x/16), jamais dans les 15 : on la cree ici, au Setup ;
#  - l'Action : `leonardo/tl001b` (meme texte, KATANA -> KAMA) :
#    `Search.PlayerCard(..., include_player_deck=True, include_discard_pile=True,
#    trait=..., card_type=Upgrade, may=True)` x2 + `PutIntoPlay` +
#    `Faces.ExhaustAll`.
#
# Mots-pieges :
#  - « Discard 1 card from your hand -> » : dans le COUT. Pas de carte en main
#    = capacite non proposee ;
#  - « UP TO 2 » : deux recherches successives, chacune `may=True` ;
#  - « (Shuffle.) » : comportement par defaut de la fouille ;
#  - « put them into play, EXHAUSTED » : on incline apres la mise en jeu ;
#  - Action NUE sur l'alter-ego (comme ls001b) ;
#  - Restricted (2 max) : les deux Kama sont Restricted 1 chacune, la limite
#    ne gene pas ici (le pack n'a que DEUX Kama).


def GetAbilities() -> Sequence['Ability']:

    def alopex(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
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
                trait=TRAIT_KAMA,
                card_type=Upgrade,
                may=True,
            )
            if not face:
                break
            face.PutIntoPlay(joueur, effect)
            Faces.ExhaustAll([face], effect)

    return [
        AbilityFactory.BeginGameWithSetAside([ID_PREY]),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            alopex,
        ).SetCostFunc(CostFunc.Discard("YourHandCards", range=(1, 1))),
    ]
