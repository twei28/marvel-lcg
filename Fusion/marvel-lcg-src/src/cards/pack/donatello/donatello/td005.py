from . import *

# Improvised Tactics — EVENEMENT, cout 2, [energy]. TACTIC. x2.
# Hero Action: Exhaust a [[TECH]] upgrade you control -> choose two (you
#   cannot choose the same option twice):
#   • Cloak two friendly characters.
#   • Stun or confuse an enemy.
#   • Draw 2 cards.
#
# CARTES DE REFERENCE
#  - `55023`-`55025` (tt/enchantress) : `player.ChooseAbilities(effect,
#    ForChoiceAbility(...), ..., choose_x_different_options=2)` = « choose two
#    (cannot choose the same twice) ».
#  - `br004` / `04009` : cout `CostFunc.Exhaust(card_type=Upgrade,
#    from_where=["YouControlCards"])` (+ `trait="TECH"`), `SetPlay()`.
#  - `gwen_stacy 27001b` : une branche de choix qui porte sa cible =
#    `ForChoiceAbility(nom, fn).SetTarget(...)`.
#  - `mf011` : `DrawUp(2, effect)`.
#
# TEXTE CONTRE CODE
#  « Exhaust a TECH upgrade you control » est DEVANT la fleche : un COUT
#    (l'amelioration incline, elle n'est pas defaussee).
#  « choose TWO ... not the same option twice » -> deux options DIFFERENTES.
#  « Stun OR confuse an enemy » -> UNE seule option de la liste, qui contient
#    elle-meme un choix etourdir/desorienter.
#  « Draw 2 cards » -> le joueur qui joue la carte.
#
# « CLOAK two friendly characters » : pose une carte d'etat Cloaked sur DEUX
# personnages amis (identites et allies de tous les joueurs,
# `Worlds.GetOnFieldFriendlyCharacters`), choisis par le joueur : exactement
# deux quand il y en a au moins deux, sinon tous ceux qui existent. Aucune
# restriction de statut : Cloaked n'a pas de plafond. Fiches :
# docs/reference/mots-cles/cloak.md et cloaked.md.


def GetAbilities() -> Sequence['Ability']:

    def tactiques(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        def cloak(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            amis = Worlds.GetOnFieldFriendlyCharacters(effect)
            if not amis:
                return
            nombre = min(2, len(amis))
            choisis = joueur.AskChooseFaces(
                amis,
                (nombre, nombre),
                effect,
                prompt="Cloak two friendly characters",
                not_move=True,
            )
            if choisis:
                Faces.GiveStatus(choisis, "Cloaked", effect)

        def etourdir_ou_desorienter(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Stun an enemy",
                    lambda cibles2:
                        Faces.GiveStatus(cibles2, "Stunned", effect),
                ).SetTarget(Enemy, canbe_stunned=True),
                AbilityFactory.ForChoiceAbility(
                    "Confuse an enemy",
                    lambda cibles2:
                        Faces.GiveStatus(cibles2, "Confused", effect),
                ).SetTarget(Enemy, canbe_confused=True),
            )

        def piocher(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            joueur.DrawUp(2, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Cloak two friendly characters", cloak),
            AbilityFactory.ForChoiceAbility("Stun or confuse an enemy", etourdir_ou_desorienter),
            AbilityFactory.ForChoiceAbility("Draw 2 cards", piocher),
            choose_x_different_options=2,
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            tactiques,
        ).SetPlay()
        .SetCostFunc(CostFunc.Exhaust(
            card_type=Upgrade,
            trait="TECH",
            from_where=["YouControlCards"],
        )),
    ]
