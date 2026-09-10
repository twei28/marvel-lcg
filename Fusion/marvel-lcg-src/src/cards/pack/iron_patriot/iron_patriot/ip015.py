from . import *

# Exposed Insanity — OBLIGATION de Norman Osborn. Boost 2.
# Give to the Norman Osborn Player.
# You may flip to alter-ego form. Choose:
#  • Exhaust Norman Osborn -> remove Exposed Insanity from the game.
#  • Discard each ally with the REGISTERED trait under your control. If no
#    allies were discarded this way, find the Reign's End side scheme and
#    reveal it.
#
# CARTE DE REFERENCE
#  - `su014` Crisis of Conscience : le calque exact de la structure —
#    `WhenThisObligationGiveToYou`, `YouMayFlipToYourAlterEgoForm`, un choix a
#    deux branches, `Faces.RemoveAllFromGame` sous `CostFunc.Exhaust(
#    "YourIdentity")`, et une branche de repli.
#  - `56027` * Madame Masque : `Find.FindAndReveal(effect, joueur, name=...)`.
#
# TEXTE CONTRE CODE
#  ⚠ « Give to the Norman Osborn Player » est une BASE NATIVE, `desc.GiveTo`.
#    Sans elle le montage du deck tombe sur `AssertionError: ip015` (mesure du
#    09/09/2026).
#  ⚠ « YOU MAY flip » : optionnel, et AVANT le choix — le joueur peut vouloir
#    passer civil pour pouvoir payer la premiere branche, qui exige d'incliner
#    Norman Osborn.
#  ⚠ « Exhaust NORMAN OSBORN » : l'ALTER-EGO. En forme heros, l'identite est
#    Iron Patriot et la branche mentirait ; d'ou la condition de forme, comme
#    sur `su014`.
#  ⚠ « remove from the game » n'est PAS une defausse : `Faces.RemoveAllFromGame`
#    (⚠ `Faces.RemoveFromGame` au singulier n'existe pas).
#  ⚠ « each ally with the REGISTERED trait UNDER YOUR CONTROL » : la punition
#    frappe l'armee entiere, pas un allie au choix. Le trait est lu sur la
#    FACE EN JEU, donc les allies ordinaires a qui `ip001a` a donne le trait
#    tombent aussi — c'est bien ce qui est ecrit.
#  ⚠ « IF NO ALLIES WERE DISCARDED THIS WAY » : le repli ne se declenche que si
#    la defausse n'a RIEN pris. Avoir une armee protege donc de Reign's End,
#    et ne pas en avoir la fait entrer. C'est le pivot du set nemesis.
#  ⚠ La deuxieme branche NE DEFAUSSE PAS l'obligation elle-meme : le texte ne
#    le dit pas. Le moteur s'en charge tout seul, comme pour toute obligation
#    resolue.


def GetAbilities() -> Sequence['Ability']:

    def obligation(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetGaveToPlayer()
        if joueur is None:
            return

        YouMayFlipToYourAlterEgoForm(joueur, effect)

        def retirer(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            Faces.RemoveAllFromGame([this], effect)

        def purger(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            allies = AlliesRegistered(joueur)
            if allies:
                Faces.DiscardAll(allies, effect)
            else:
                Find.FindAndReveal(effect, joueur, name="Reign's End")

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust Norman Osborn → remove Exposed Insanity from the game",
                retirer,
                condition=joueur.IsAlterEgo(),
            ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
            AbilityFactory.ForChoiceAbility(
                "Discard each REGISTERED ally you control",
                purger,
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(obligation),
    ]
