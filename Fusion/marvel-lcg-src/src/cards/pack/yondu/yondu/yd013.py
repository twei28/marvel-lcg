from . import *

# Banished — OBLIGATION. Boost 2, donnee au joueur Yondu Udonta.
# Give to the Yondu Udonta player.
# You may flip to alter-ego form. Choose:
#  • Exhaust your alter-ego -> remove Banished from the game.
#  • Discard the Yaka Arrow upgrade and exhaust the Tahlei upgrade. Discard
#    this obligation.
#
# ⚠ CE MODULE VIT DANS `yondu/`, PAS DANS `yondu_nemesis/`. Son `set_name`
# vaut « Yondu » — l'obligation appartient au set du HEROS, comme im014, as014
# et nt012 — et `database.py:197` cherche le module dans le dossier qui porte
# le nom du SET. Range ailleurs, le fichier ne serait JAMAIS charge et
# l'obligation entrerait en jeu sans rien faire, en silence. C'est le piege
# bt019, et il a ete paye la veille sur `nt012`.
#
# Cartes de reference :
#  - **`im014`** Technical Issues, **`nt012`** Practice et `an010` Banished
#    from Asgard : MEME structure — `WhenThisObligationGiveToYou(op)`,
#    `YouMayFlipToYourAlterEgoForm(joueur, effect)` (helper global,
#    cards/pack/__init__.py:132), puis un `ChooseAbilities` a deux branches
#    dont l'une RETIRE DE LA PARTIE et l'autre DEFAUSSE.
#  - `Faces.DiscardAll` / `Faces.RemoveAllFromGame` / `Faces.ExhaustAll`.
#
# ⚠ HOMONYME : `an010` du pack angela s'appelle « Banished from Asgard », pas
# « Banished ». Les deux noms sont distincts, verifie le 03/09/2026.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « remove Banished **from the game** » (branche 1) contre « **Discard**
#    this obligation » (branche 2) : deux sorties DIFFERENTES. La premiere ne
#    revient jamais, la seconde retourne dans le deck de rencontre au
#    remelange. Ne jamais coder l'une pour l'autre.
#  - « **Discard** the Yaka Arrow upgrade » : elle part a la DEFAUSSE, d'ou
#    `yd001b` Whistlin' et `yd004` pourront la CONVOQUER — c'est exactement
#    pourquoi le mot-cle maison `summon` inclut la defausse (arbitrage du
#    03/09/2026). Sans cela, cette branche tuerait le pack pour la partie.
#  - « **and** exhaust the Tahlei upgrade » : les deux, et l'une ou l'autre
#    peut manquer sur le terrain — la branche reste prenable.
#  - « **You may** flip to alter-ego form » : facultatif, et c'est ce que rend
#    `YouMayFlipToYourAlterEgoForm`.
#  - « Exhaust your **alter-ego** » : la face civile, pas le heros. Le joueur
#    vient d'y basculer, ou pas — d'ou la condition sur l'inclinaison.


def GetAbilities() -> Sequence['Ability']:

    def banished(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetGaveToPlayer()
        if joueur is None:
            return

        YouMayFlipToYourAlterEgoForm(joueur, effect)

        identite = joueur.GetIdentity()

        def incliner_puis_retirer(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            if identite is None:
                return
            Faces.ExhaustAll([identite], effect)
            Faces.RemoveAllFromGame([this], effect)

        def sacrifier_la_fleche(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            fleche = LaFleche(effect)
            if fleche is not None:
                Faces.DiscardAll([fleche], effect)
            tahlei = LaTahlei(effect, joueur)
            if tahlei is not None:
                Faces.ExhaustAll([tahlei], effect)
            Faces.DiscardAll([this], effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust your alter-ego → remove Banished from the game",
                incliner_puis_retirer,
                condition=(identite is not None and not identite.IsExhaust()),
            ),
            AbilityFactory.ForChoiceAbility(
                "Discard the Yaka Arrow and exhaust Tahlei. Discard this obligation",
                sacrifier_la_fleche,
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            banished,
        ),
    ]
