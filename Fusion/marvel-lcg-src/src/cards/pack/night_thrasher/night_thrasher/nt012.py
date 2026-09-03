from . import *

# Practice — OBLIGATION. Boost 1, donnee au joueur Night Thrasher.
# Give to the Night Thrasher player.
# You may flip to alter-ego form. Choose:
#  • Exhaust your identity or discard 1 card from your hand -> remove Practice
#    from the game.
#  • You cannot flip the Battle Board upgrade until the start of the next
#    villain phase. Discard this obligation.
#
# Cartes de reference :
#  - **`im014`** Technical Issues (pack iron_man_model_42) et `an010` Banished
#    from Asgard : MEME structure — `WhenThisObligationGiveToYou(op)`,
#    `YouMayFlipToYourAlterEgoForm(joueur, effect)` (helper global,
#    cards/pack/__init__.py:132), puis un `ChooseAbilities` a deux branches
#    dont l'une retire la carte de la PARTIE et l'autre la DEFAUSSE.
#  - `11020` Depowered / `as014` pour le « you cannot ... » d'une obligation
#    qui reste en jeu — sauf qu'ici elle ne reste PAS : les deux branches la
#    font partir, et l'interdiction est TEMPORAIRE.
# ⚠ CE MODULE VIT DANS `night_thrasher/`, PAS DANS `night_thrasher_nemesis/`,
# et c'est un CORRECTIF du 03/09/2026. Son `set_name` vaut « Night Thrasher »
# (l'obligation appartient au set du HEROS, comme im014 et as014), et
# `database.py:197` cherche le module dans le dossier qui porte le nom du SET.
# Range dans le dossier nemesis, le fichier n'etait JAMAIS charge : l'obligation
# entrait en jeu et ne faisait rien, en silence. Le journal du cas le dit —
# « Practice entered play », puis plus une ligne. C'est exactement le piege
# bt019, ecrit noir sur blanc en tete de ce pack, et paye quand meme.
#
#  - `YouCannotFlipCards` (ability_factory.py:212) pour l'interdiction, et
#    `RegisterTemp(..., until_phase_end=...)` pour sa duree.
#
# ⚠ `desc.GiveTo` vaut « **Dwayne Taylor** », le nom de l'ALTER-EGO, alors que
# la carte imprime « Give to the **Night Thrasher** player ». C'est un
# CORRECTIF du 03/09/2026, et il a ete paye : avec « Night Thrasher »,
# `Worlds.FindPlayerByName` ne trouvait AUCUN joueur, l'obligation entrait en
# jeu sans jamais etre DONNEE, et `WhenObligationGiveToPlayer` n'etait donc
# jamais envoye — la carte restait sur la table sans rien faire, en silence.
# Le journal du cas le montre : « Practice entered play », puis plus rien.
# Les autres obligations du depot nomment toutes leur alter-ego (im014 « Tony
# Stark », as014 « Peter Parker »), et cinq d'entre elles ont deja un `GiveTo`
# qui differe de leur texte imprime : c'est la convention du moteur, pas une
# trahison du texte — les deux designent le meme joueur.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « Exhaust your identity **or** discard 1 card from your hand » : un OU
#    dans le COUT de la premiere branche, pas deux branches de plus. Le
#    moteur ne sait pas offrir un choix DANS un cout : la branche est donc
#    dedoublee en deux options, ce qui rend exactement les trois choix
#    possibles au joueur.
#  - « remove Practice **from the game** » (branche 1) contre « **Discard**
#    this obligation » (branche 2) : deux sorties DIFFERENTES. La premiere ne
#    revient jamais, la seconde retourne dans le deck de rencontre au
#    remelange. Ne jamais coder l'une pour l'autre.
#  - « You cannot flip the Battle Board upgrade **until the start of the next
#    villain phase** » : l'interdiction est TEMPORAIRE, et sa borne est le
#    DEBUT de la phase du vilain — donc elle couvre la fin de la phase des
#    joueurs en cours. `until_phase_end=True` la termine a la fin de la phase
#    courante, ce qui est la meme frontiere vue de l'autre cote.
#  - ⚠ C'est la branche la plus punitive du pack : sans planche retournable,
#    nt002, nt004, nt006, nt007 et nt009 perdent leur moitie utile.
#  - « **You may** flip to alter-ego form » : facultatif, et c'est ce que rend
#    `YouMayFlipToYourAlterEgoForm`.


def GetAbilities() -> Sequence['Ability']:

    def practice(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetGaveToPlayer()
        if joueur is None:
            return

        YouMayFlipToYourAlterEgoForm(joueur, effect)

        identite = joueur.GetIdentity()
        main = list(joueur.hand_cards.Get())

        def incliner_puis_retirer(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            if identite is None:
                return
            Faces.ExhaustAll([identite], effect)
            Faces.RemoveAllFromGame([this], effect)

        def defausser_puis_retirer(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            cartes = list(joueur.hand_cards.Get())
            if not cartes:
                return
            Faces.DiscardAll(cartes[:1], effect)
            Faces.RemoveAllFromGame([this], effect)

        def bloquer_la_planche(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            this.effect.RegisterTemp(
                AbilityFactory.YouCannotFlipCards(
                    CardFinder(name="Battle Board", card_type=Upgrade),
                ),
                unregister_after_exec=False,
                until_phase_end=True,
            )
            Faces.DiscardAll([this], effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust your identity → remove Practice from the game",
                incliner_puis_retirer,
                condition=(identite is not None and not identite.IsExhaust()),
            ),
            AbilityFactory.ForChoiceAbility(
                "Discard 1 card from your hand → remove Practice from the game",
                defausser_puis_retirer,
                condition=bool(main),
            ),
            AbilityFactory.ForChoiceAbility(
                "You cannot flip the Battle Board until the next villain phase. Discard this obligation",
                bloquer_la_planche,
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            practice,
        ),
    ]
