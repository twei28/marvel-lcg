from . import *

# * Sentinel — FACE ALTER-EGO (Juston Seyfert au volant). ANDROID. GIANT.
# REC 4, main 6, 14 PV.
# Action: Search your deck and discard pile for Juston Seyfert and add him to
#   your hand. (Limit once per phase.)
# Action: Discard 1 card from your hand → flip each [[COMPONENT]]
#   ([[DESTROYED]] side) upgrade to its [[INTACT]] side.
# Setup: Put each [[COMPONENT]] upgrade ([[INTACT]] side up) into play.
#
# Cartes de reference :
#  - `06001b` Odinson : la recherche d'une carte nommee dans le deck ET la
#    defausse, puis `initiator.GainCard(face, effect)`, avec une limite.
#  - `45014` : `CostFunc.Discard("YourHandCards")` pour « defaussez 1 carte de
#    votre main → ».
#  - `dz017a` : `Faces.FlipAllTo(cibles, None, effect)` pour retourner.
#
# ⚠ LA MISE EN PLACE N'A PAS DE SCRIPT. « Setup: Put each COMPONENT upgrade
# into play » est deja porte par les quatre cartes elles-memes : `desc.Setup`
# sur st002a, st003a, st004a et st005a (modele nt003a Battle Board, et
# world.py:531 qui ne scanne ce mot-cle que dans le DECK DU JOUEUR — c'est
# pourquoi les Component vivent dans `hero_deck` et non dans `set_aside`).
# Ecrire ici un second `SetupPutIntoPlay` les mettrait en jeu DEUX FOIS.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « flip **each** COMPONENT (DESTROYED side) » : TOUS d'un coup, pas un au
#    choix. Aucune selection, aucune cible : on lit le terrain.
#  - « (Limit once per **phase**.) » : `LimitOncePerPhase`, pas `PerRound`. En
#    alter-ego on ne joue qu'une fois par tour, mais deux joueurs Sentinel
#    n'existent pas et la limite reste celle imprimee.
#  - Le deuxieme pouvoir n'a PAS de limite imprimee : il se repete tant qu'il
#    reste des cartes en main. C'est voulu, c'est la soupape du pack.
#  - « Action » NUE sur les deux : imprimees sur la face ALTER-EGO, elles ne
#    valent qu'en forme civile de toute facon.


def GetAbilities() -> Sequence['Ability']:

    def rappeler_juston(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        initiator = effect.GetInitiator()
        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
            card_type=Support,
            name=NOM_JUSTON,
        )
        if face:
            initiator.GainCard(face, effect)

    def remonter_le_robot(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        Faces.FlipAllTo(ComposantsDetruits(effect), None, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            rappeler_juston,
        ).LimitOncePerPhase(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            remonter_le_robot,
            conditions=[
                lambda effect, message: ComposantsDetruits(effect) != []
            ],
        ).SetCostFunc(CostFunc.Discard("YourHandCards")),
    ]
