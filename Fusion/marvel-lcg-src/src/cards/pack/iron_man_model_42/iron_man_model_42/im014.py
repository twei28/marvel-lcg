from . import *

# Technical Issues — OBLIGATION du pack, x1.
# Give to the Tony Stark player.
# You may flip to alter-ego form. Choose:
#  • Exhaust Tony Stark and Tony's Workshop -> remove Technical Issues from
#    the game.
#  • Remove 2 reactor counters from your identity. If no reactor counters were
#    removed this way, this card gains surge. Discard this obligation.
#
# Carte de reference : **`an010` Banished from Asgard** (pack angela), et
# c'est un jumeau de STRUCTURE, pas seulement d'esprit :
#   « You may flip to alter-ego form. Choose:
#     • Exhaust <alter-ego> -> remove <cette carte> from the game.
#     • <effet>. If <rien ne s'est passe>, this card gains surge. Discard. »
# Meme `YouMayFlipToYourAlterEgoForm`, meme `ChooseAbilities` a deux branches,
# meme `GainSurge` conditionne a un effet qui n'a rien fait, meme
# `AbilityFactory.Otherwise` en repli.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « You **MAY** flip » et non « must » : le helper
#    `YouMayFlipToYourAlterEgoForm`, comme an010 et 48026. Le mot compte —
#    vp011 One Too Many Voices dit « must » et passe par un autre chemin.
#  - La premiere branche exige **DEUX cartes inclinees** : Tony Stark ET
#    Tony's Workshop. Si le soutien n'est pas en jeu, ou s'il est deja
#    incline, la branche n'est pas prenable — d'ou sa `condition`. C'est le
#    piege `wd005` : un cout a deux parties dont on n'oublie aucune.
#  - « remove ... **from the game** » : la branche indolore fait disparaitre
#    l'obligation pour de bon. L'autre la DEFAUSSE : elle reviendra.
#  - « If **NO** reactor counters were removed this way » : le surge tombe
#    seulement si le compteur etait a ZERO. En retirer un seul sur les deux
#    demandes suffit a l'eviter. On lit donc le nombre REELLEMENT retire, pas
#    le nombre demande.
#  - L'obligation vient piocher dans la ressource centrale du pack : sur un
#    heros a 10 PV dont tout depend du reacteur, c'est une vraie perte, et
#    c'est voulu.


def GetAbilities() -> Sequence['Ability']:

    def technical_issues(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetGaveToPlayer()
        if joueur is None:
            return

        YouMayFlipToYourAlterEgoForm(joueur, effect)

        identite = joueur.GetIdentity()

        def atelier_pret() -> 'CardFace|None':
            # ⚠ `Player.GetPlayArea()` N'EXISTE PAS. La premiere ecriture
            # l'appelait, et le moteur a AVALE l'AttributeError : l'obligation
            # ne faisait plus RIEN du tout, ni bascule, ni statut, ni
            # defausse — et rien ne l'ecrivait nulle part. Trouve par les deux
            # cas de test le 03/09/2026, exactement comme les trois defauts de
            # ls014 la veille. Le bon accesseur est `joueur.supports.Get()`
            # (player.py:75).
            for face in joueur.supports.Get():
                if face.IsName("Tony's Workshop") and not face.IsExhaust():
                    return face
            return None

        def retirer_de_la_partie(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            atelier = atelier_pret()
            if identite is None or atelier is None:
                return
            Faces.ExhaustAll([identite, atelier], effect)
            Faces.RemoveAllFromGame([this], effect)

        def vider_le_reacteur(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            retires = 0
            if identite is not None:
                retires = Faces.RemoveCountersOn([identite], 2, 'reactor', effect) or 0
            # « If NO reactor counters were removed THIS WAY » : zero, pas
            # « moins de deux ».
            if not retires:
                this.GainSurge(1, effect)
            Faces.DiscardAll([this], effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust Tony Stark and Tony's Workshop → remove Technical Issues from the game",
                retirer_de_la_partie,
                # ⚠ `condition` de `ForChoiceAbility` attend un BOOLEEN, pas
                # un callable (for_choice.py:43) : il est evalue a la
                # CONSTRUCTION de la branche, ce qui convient ici puisque le
                # ChooseAbilities est monte au moment de resoudre
                # l'obligation.
                condition=(identite is not None
                           and not identite.IsExhaust()
                           and atelier_pret() is not None),
            ),
            AbilityFactory.ForChoiceAbility(
                "Remove 2 reactor counters from your identity. Discard this obligation",
                vider_le_reacteur,
            ),
            AbilityFactory.Otherwise(vider_le_reacteur),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            technical_issues
        ),
    ]
