from . import *

# Unrequited Love — OBLIGATION du pack, x1.
# Give to the Lady Sif player.
# You may flip to alter-ego form.
# Stun Lady Sif. Stun or confuse Thor. If you cannot, confuse Lady Sif.
#   Discard this obligation.
#
# Cartes de reference :
#  - **`an010` Banished from Asgard** (pack angela), squelette exact :
#    `WhenThisObligationGiveToYou` + `YouMayFlipToYourAlterEgoForm` +
#    `ChooseAbilities` + `Faces.DiscardAll([this], effect)` ;
#  - `05015` / `01083` pour `Faces.GiveStatus(cibles, "Stunned"/"Confused")`.
#
# ⚠ « You MAY flip » et non « You MUST flip » : on passe donc par le helper
# `YouMayFlipToYourAlterEgoForm`, comme an010 et 48026. Le mot compte — vp011
# One Too Many Voices, qui dit « must », force la bascule par un autre chemin.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « Stun LADY SIF » : l'IDENTITE, et les deux faces s'appellent pareil. Le
#    statut se pose sur l'identite quelle que soit la forme, y compris apres
#    la bascule facultative ci-dessus.
#  - « Stun OR confuse Thor » : un choix, pas les deux. Deux
#    `ForChoiceAbility` dans un seul `ChooseAbilities`.
#  - « THOR » : l'allie ls002 de CE pack, et le nom est partage par six cartes
#    du jeu. On ne cherche donc que parmi les allies que LE JOUEUR controle.
#  - « **If you cannot**, confuse Lady Sif » : la branche de repli, et elle est
#    REELLEMENT atteignable — Thor n'est pas en jeu la plupart du temps (un
#    seul exemplaire dans le deck). Elle tire aussi si Thor est en jeu mais ne
#    peut recevoir NI l'un NI l'autre statut (Tenace, ou statut deja pose) :
#    d'ou la verification sur le RETOUR de `GiveStatus`, et non sur la seule
#    presence de l'allie. C'est le piege `wd028`, ou un « If you cannot »
#    testait un cas impossible.
#  - « Discard this obligation » est INCONDITIONNEL : il tombe dans les deux
#    branches, contrairement a des obligations qui se remettent en jeu.


def GetAbilities() -> Sequence['Ability']:

    def thor_du_joueur(joueur: 'Player') -> 'CardFace|None':
        for face in joueur.allies.Get():
            if face.IsName("Thor"):
                return face
        return None

    def unrequited_love(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetGaveToPlayer()
        if joueur is None:
            return

        YouMayFlipToYourAlterEgoForm(joueur, effect)

        identite = joueur.GetIdentity()
        if identite is not None:
            Faces.GiveStatus([identite], "Stunned", effect)

        thor = thor_du_joueur(joueur)
        touche = {"thor": False}

        def frapper_thor(statut: str) -> None:
            if thor is not None and Faces.GiveStatus([thor], statut, effect):
                touche["thor"] = True

        if thor is not None:
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Stun Thor",
                    lambda cibles: frapper_thor("Stunned"),
                ),
                AbilityFactory.ForChoiceAbility(
                    "Confuse Thor",
                    lambda cibles: frapper_thor("Confused"),
                ),
            )

        # « If you cannot, confuse Lady Sif » : ni Thor en jeu, ni statut
        # reellement pose sur lui.
        if not touche["thor"] and identite is not None:
            Faces.GiveStatus([identite], "Confused", effect)

        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            unrequited_love
        ),
    ]
