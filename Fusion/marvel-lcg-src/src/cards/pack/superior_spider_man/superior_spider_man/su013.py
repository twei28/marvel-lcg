from . import *

# Ghost of a Conscience — OBLIGATION de Peter Parker. Boost 2.
# Give to the Peter Parker player.
# You may flip to alter-ego form. Choose:
#  • Exhaust Peter Parker -> remove Ghost of a Conscience from the game.
#  • You are stunned and confused. If you were already stunned and confused,
#    this card gains surge. Discard this obligation.
#
# ⚠⚠ CE HEROS A DEUX OBLIGATIONS, UNE PAR ALTER-EGO, et une seule entre en jeu.
# La jumelle est `su014`, au texte STRICTEMENT IDENTIQUE au nom pres. Le
# deck de depart qui embarque `su001b` embarque celle-ci, et l'autre n'existe pas
# de la partie (insert : « the other set will not be needed »).
#
# ⚠ ELLE VIT DANS LE DOSSIER DU HEROS, PAS DANS `_nemesis`. Son bandeau imprime
# dit « SPIDER-MAN », donc son `set_name` est celui du heros, et le moteur
# cherche le module dans le dossier du `set_name` (database.py:195). Rangee
# dans `_nemesis`, elle ne serait JAMAIS chargee, EN SILENCE (lecon `bt019`,
# 1/9/2026). Treizieme fois que le piege se presente.
#
# CARTES DE REFERENCE
#  - `an010` Banished from Asgard : le calque presque exact — « You may flip to
#    your alter-ego form », un choix a deux branches, « Exhaust <identite> ->
#    remove from the game » (`Faces.RemoveAllFromGame` +
#    `CostFunc.Exhaust("YourIdentity")`), et la branche de repli qui defausse
#    l'obligation.
#  - `ho013`, `an010` : `WhenThisObligationGiveToYou(op)` + `desc.GiveTo`.
#  - `05015` : `Faces.GiveStatus(..., "Stunned"/"Confused", effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « YOU MAY flip to alter-ego form » : optionnel, et il PRECEDE le choix —
#    le joueur peut vouloir passer civil pour pouvoir payer la premiere branche
#    (qui exige d'incliner l'alter-ego).
#  ⚠ « Exhaust Peter Parker » : c'est l'ALTER-EGO qui doit etre incline, donc la
#    branche n'est payable qu'en forme civile. `CostFunc.Exhaust("YourIdentity")`
#    s'en charge : en forme heros, l'identite est le heros, et le texte nomme
#    l'alter-ego. On double d'une condition de forme pour ne pas offrir une
#    branche qui mentirait.
#  ⚠ « IF YOU WERE ALREADY stunned AND confused » : les DEUX, et AVANT que la
#    carte ne les pose. On lit donc l'etat AVANT `GiveStatus`, pas apres — sinon
#    la condition serait toujours vraie et l'obligation aurait toujours surge.
#  ⚠ « remove from the game » n'est PAS une defausse : `Faces.RemoveAllFromGame`
#    (⚠ `Faces.RemoveFromGame` au singulier n'existe pas).
#  ⚠ Aucune limite imprimee : etape 7 bis sans objet.


def GetAbilities() -> Sequence['Ability']:

    def obligation(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetGaveToPlayer()
        if joueur is None:
            return

        YouMayFlipToYourAlterEgoForm(joueur, effect)
        identite = joueur.GetIdentity()

        def retirer(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            Faces.RemoveAllFromGame([this], effect)

        def encaisser(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            # ⚠ L'etat est lu AVANT de poser les statuts : « if you WERE
            # ALREADY stunned and confused ».
            deja = False
            if identite is not None:
                statut = identite.CastTo(Unit2)
                deja = bool(statut.HasStatus("Stunned") and statut.HasStatus("Confused"))
            if identite is not None:
                Faces.GiveStatus([identite], "Stunned", effect)
                Faces.GiveStatus([identite], "Confused", effect)
            if deja:
                this.GainSurge(1, effect)
            Faces.DiscardAll([this], effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust Peter Parker → remove Ghost of a Conscience from the game",
                retirer,
                condition=joueur.IsAlterEgo(),
            ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
            AbilityFactory.ForChoiceAbility(
                "You are stunned and confused. Discard this obligation",
                encaisser,
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(obligation),
    ]
