from . import *

# The Chosen Leader — AMELIORATION signature, custom « CptScorp »
# Cout 3, ressource [wild], trait TITLE.
#
# Response: After an ally you control is defeated by consequential damage,
#   search your deck for an ally and add it to your hand.
# Forced Response: When an ally you control is used to defend, deal 1 damage
#   to your identity.
#
# ---------------------------------------------------------------------------
# CAPACITE 1 : « DEFEATED **BY CONSEQUENTIAL DAMAGE** »
#
# Carte de reference : `38028` Med Lab (pack rogue, OFFICIELLE), qui imprime
# la meme restriction et s'ecrit
# `AfterUnitBeDefeated(AbilityType.Response, Ally, ..., by_consequential=True)`.
#
# `by_consequential=True` (factory/defeated.py:355-358) teste
# `message.IsByConsequential()`, soit `type(...by_effect) is Consequential`
# (sender_unit.py:116-118). RESTRICTION FORTE, et c'est le sujet de la
# carte : un allie tue par une ATTAQUE du vilain ne declenche RIEN. Coder
# « defeated » tout court aurait rendu la carte deux fois plus forte
# (mot-piege `defeated` vs `damaged` du PROCESSUS-CARTE §5).
#
# « an ally YOU CONTROL » : rendu par la cible-chaine `"YouControlAlly"`
# plutot que par le type `Ally` nu. La fabrique bascule alors sur un
# `WhenUnitWouldBeDefeated` + capacite temporaire (defeated.py:395-428) :
# c'est le seul moyen de connaitre le CONTROLEUR d'un allie qui est en train
# de quitter le jeu — une fois vaincu, il n'en a plus.
#
# « search YOUR DECK for an ally » : le deck SEUL, pas la defausse
# (difference avec pt001b et pt002, qui disent « and discard pile »). Le
# remelange est fait par la recherche (search_internal.py:61-66). Modele du
# couple recherche + main : `gp007` Gwen's Room.
#
# ---------------------------------------------------------------------------
# CAPACITE 2 : LE TEXTE EST CONTRADICTOIRE, ET IL A ETE TRANCHE
#
# Imprime : « **Forced Response**: WHEN an ally you control is used to
# defend, deal 1 damage to your identity. »
#
# « Forced Response » resout APRES l'evenement ; « When » annonce un AVANT.
# Les deux ne peuvent pas etre vrais. ARBITRAGE DE L'UTILISATEUR, 30/08/2026 :
# **c'est une Forced Response, donc APRES**. Le mot-cle en gras fait foi,
# « When » n'est que de l'anglais relache. C'est le meme cas que The Made Men
# (« Forced Interrupt : After Maniac schemes or attacks »), cite en exemple
# dans le PROCESSUS-CARTE §3.
#
# Rendu : `AbilityFactory.AfterUnitBecomeDefender(AbilityType.ForcedResponse,
# ...)`. Cette fabrique (factory/do_attack.py:1257-1286) part au moment ou
# l'unite DEVIENT le defenseur (`DeclareDefenderInternal`,
# sender_damage.py:170), c'est-a-dire exactement « is used to defend » — et
# non « a fini de defendre ». La difference compte : avec
# `AfterUnitDefendAgainstAttack` (modele `36035` Hangar Bay), un allie tue par
# l'attaque qu'il vient d'encaisser ne declencherait plus rien.
#
# La fabrique n'a pas de parametre « qui defend » : le filtre passe par
# `conditions`, avec la cible-chaine `"YouControlAlly"`
# (condition/card_type.py:32 et 168-169) sur `message.trigger`.
#
# « deal 1 damage to YOUR IDENTITY » : l'identite du controleur de cette
# amelioration, quelle que soit sa forme (le texte dit « identity », pas
# « hero »). Les degats partent de l'amelioration, qui route vers l'identite
# comme toute carte joueur.
#
# ⚠ PAS de cout, pas de fleche sur cette seconde capacite : c'est une
# consequence FORCEE, elle ne se paie pas et ne se refuse pas.
#
# ⚠ PAS de `SetPlay()` (piege `66006`/`66007`).


def GetAbilities() -> Sequence['Ability']:

    def chercher_un_allie(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        joueur = this.GetControlByPlayer()
        if joueur is None:
            return

        face = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            card_type=Ally,
        )
        if face:
            joueur.GainCard(face, effect)

    def est_un_allie_du_joueur(effect: 'Effect', message: 'Message.AfterUnitBecomeDefender') -> bool:
        return Condition.CheckWhichCard("YouControlAlly", message.trigger, effect)

    def degat_au_leader(effect: 'Effect', message: 'Message.AfterUnitBecomeDefender') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        joueur = this.GetControlByPlayer()
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is None:
            return

        this.DealDamage([identite], 1, effect)

    return [
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.Response,
            "YouControlAlly",
            chercher_un_allie,
            by_consequential=True,
        ),
        AbilityFactory.AfterUnitBecomeDefender(
            AbilityType.ForcedResponse,
            degat_au_leader,
            conditions=[est_un_allie_du_joueur],
        ),
    ]
