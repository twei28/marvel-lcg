from . import *

# To Arms! — evenement signature, x1 (n/15 = 7).
# TACTIC. Cout 0, ressource [energy].
# Alter-Ego Action: Change to hero form. You may spend 1 resource to ready
#   your hero.
# Hero Action: Search your deck and discard pile for a WEAPON upgrade and add
#   it to your hand. Shuffle your deck.
#
# Cartes de reference :
#  - la bascule : `ag005` Parting Shots / `hk001b` —
#    `initiator.GetIdentity().ChangeToForm(Hero, effect)` ;
#  - « you may spend 1 resource » : `50134` / `ho010`, motif
#    `MayChooseOneAbility(ForChoiceAbilityWithCost(Cost("1"), ...))` — le
#    « may » impose la branche Cancel, que `MayChooseOneAbility` ajoute
#    d'office ;
#  - la fouille : **`an001b` * Aldrif Odinsdottir** (et `ok001b` * Okoye),
#    jumeaux exacts — `Search.PlayerCard(include_player_deck=True,
#    include_discard_pile=True, trait="WEAPON")` + `GainCard`. Le
#    « Shuffle your deck » est le comportement PAR DEFAUT de `Search`, il ne
#    se code pas.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - Les deux capacites sont sur la MEME carte et s'excluent par leur forme :
#    la civile bascule, l'heroique cherche une arme. Une seule des deux est
#    jouable a un instant donne.
#  - « You MAY spend » : facultatif. Un `SetCostFunc` sur l'abilite en ferait
#    un cout obligatoire, et la carte deviendrait injouable sans ressource.
#  - « ready YOUR HERO » : apres la bascule, donc la face heros qui vient
#    d'arriver. On relit `GetHero()` APRES `ChangeToForm`, jamais avant.
#  - « a [[WEAPON]] UPGRADE » : le type compte. an001b cherche une « WEAPON
#    card » sans type ; ici c'est une AMELIORATION, d'ou `card_type=Upgrade`.
#    Dans ce pack, ls010 Sif's Spear et ls011 Sif's Sword sont les deux
#    seules — et elles sont toutes deux Restricted, donc on ne peut en poser
#    que deux au total.
#  - « deck AND discard pile » : les DEUX, d'ou `include_discard_pile=True`.
#    Le modele d'origine 01040b T'Challa ne fouille QUE le deck : le copier
#    aurait tu la moitie de la phrase.
#  - « add it to your HAND » : la carte n'entre pas en jeu, elle est piochee.


def GetAbilities() -> Sequence['Ability']:

    def basculer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        identite = initiator.GetIdentity()
        if identite is None:
            return
        identite.ChangeToForm(Hero, effect)

        # ⚠ Relire la face APRES la bascule : c'est le heros qui vient
        # d'arriver qu'on redresse, pas la face de depart.
        # ⚠ `Player.GetHero()` LEVE UN ASSERT hors forme de heros
        # (player_get.py:208), et le moteur avale l'exception : si un effet
        # adverse empeche le changement de forme (vv011 Grounded, 02048 All
        # Tied Up), l'appel nu ferait echouer la carte EN SILENCE. Paye sur
        # ls014 au premier passage de la batterie, le 03/09/2026.
        if not initiator.IsHero():
            return
        heros = initiator.GetHero()
        initiator.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbilityWithCost(
                Cost("1"),
                "Ready your hero",
                lambda cibles, res: Faces.ReadyAll([heros], effect),
            ),
        )

    def chercher_une_arme(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
            trait="WEAPON",
            card_type=Upgrade,
        )
        if face:
            initiator.GainCard(face, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            basculer,
        ).SetPlay(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            chercher_une_arme,
        ).SetPlay(),
    ]
