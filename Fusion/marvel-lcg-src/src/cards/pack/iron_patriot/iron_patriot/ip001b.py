from . import *

# * Norman Osborn — ALTER-EGO. REC 3, main 6, 11 PV. BUISNESSMAN. GENIUS.
# New World Order — Setup: During deck building, your deck cannot include any
#   aspect allies. Norman Osborn begins the game with the REGISTERED deck and
#   the Registration Act side-scheme in play. (See insert.)
# Action: Exhaust Norman Osborn -> resolve the "Special" ability on 1
#   REGISTERED ally.
#
# ⚠ LE TRAIT IMPRIME EST « BUISNESSMAN », coquille de l'auteur. `cards.json`
# porte BUSINESSMAN, le trait correct : un trait est une CLE MECANIQUE, pas du
# texte d'affichage, et la coquille ne s'apparierait a aucun effet du jeu.
# C'est le SEUL endroit du pack ou l'on s'ecarte de ce qui est imprime.
#
# CARTE DE REFERENCE, ET ELLE FAIT PRESQUE TOUT
#  - `09001b` Stephen Strange (pack drs) : le deck d'Invocation. Trois pieces
#    reprises telles quelles —
#      1. `AbilityFactory.BeginGameWithSetAside([...])` declare les cartes du
#         second deck ;
#      2. `WhenPlayerSelectHero` les deplace vers `player.additional_deck` ;
#      3. `WhenCardWouldMoveToArea` + `message.ChangeToArea` REDIRIGE leur
#         defausse vers `additional_discard_pile`.
#    ⚠⚠ LE POINT 3 NE VAUT QUE POUR LES ALLIES. L'insert coupe la poire en
#    deux, et c'est contre-intuitif :
#      « REGISTERED allies get put into the REGISTERED deck discard pile when
#        defeated, while REGISTERED deck MINIONS get put into the ENCOUNTER
#        deck discard pile when defeated. This is because they are still
#        treated as minions when they are defeated, their separation
#        determined by if they gained the REGISTERED trait when they entered
#        play. »
#    Autrement dit : le sbire qu'on a REFUSE de payer meurt comme un sbire
#    ordinaire et part en defausse de RENCONTRE — il est perdu pour de bon
#    cote Norman. Seul celui qu'on a recrute revient dans le deck REGISTERED.
#    ⚠ Et il faut le POUSSER : la carte appartient au JOUEUR, donc sans cette
#    branche le moteur la range dans SA defausse a lui, au milieu des cartes
#    qu'on pioche. Les deux branches sont donc actives, pas une seule.
#    D'ou le test `HasTrait(TRAIT_REGISTERED)` : les sbires du deck ne portent
#    PAS le trait sur le papier, ils le gagnent en devenant allies
#    (`Faces.TreatAsAlly` echange leur face contre le gabarit `registered_ally`,
#    qui le porte). La premiere version redirigeait les deux, ce qui rendait le
#    deck REGISTERED inepuisable.
#  - `58031` Cameo / `cameo_compliment` : `face.ResolveSpecialAbility(player,
#    effect)` pour l'Action.
#
# TEXTE CONTRE CODE
#  ⚠ « begins the game with ... the Registration Act side-scheme IN PLAY » ne
#    se code PAS ici : `ip002a` porte `desc.Setup = "1"`, base native, et le
#    moteur la pose lui-meme. C'est pour cela que `HasSetup` a du etre ajoute
#    a `PlayerSideScheme` (correctif moteur du 09/09/2026).
#  ⚠ « your deck cannot include ANY ASPECT ALLIES » est une regle de
#    CONSTRUCTION de deck : elle appartient a l'editeur, pas au moteur de
#    partie. Non codee ici, signalee dans le rapport.
#  ⚠ « resolve the "Special" ability on 1 REGISTERED ALLY » : un ALLIE, donc
#    pas un sbire du deck reste sbire. `AlliesRegistered` lit le trait sur la
#    FACE, ce qui inclut les allies ordinaires a qui `ip001a` a donne le trait.


def GetAbilities() -> Sequence['Ability']:

    DECK_REGISTERED = (["ip020"] * 3 + ["ip021"] * 3 + ["ip022"] * 3
                       + [f"ip{i:03d}" for i in range(23, 34)])

    def monter_le_deck_registered(effect: 'Effect', message: 'Message.WhenPlayerSelectHero') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        # Chaque sbire du deck REGISTERED apprend a rentrer chez lui.
        for face in joueur.set_aside_deck.Get():
            face.effect.Registers(RedirectionVersLeDeckRegistered(joueur))

        Faces.ShuffleAllTo(list(joueur.set_aside_deck.Get()),
                           DeckRegistered(joueur), effect)

    def new_world_order(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        for allie in effect.targets:
            allie.ResolveSpecialAbility(joueur, effect)

    def un_allie_registered(effect: 'Effect') -> Sequence['CardFace']:
        joueur = effect.GetInitiator()
        return AlliesRegistredPouvantResoudreUnSpecial(joueur)

    return [
        AbilityFactory.BeginGameWithSetAside(DECK_REGISTERED),
        # ⚠ `which_hero` d'abord : la fabrique prend la CARTE surveillee avant
        # l'operation (setup.py:82). « This » — c'est NOTRE identite qu'on
        # attend, pas celle d'un autre joueur.
        AbilityFactory.WhenPlayerSelectHero("This", monter_le_deck_registered),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            new_world_order,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(un_allie_registered),
    ]
