from . import *

# Sense It! — evenement signature, x2. SUPERPOWER. Cout 1, ressource [wild].
# Hero Interrupt: When a treachery card is revealed from the encounter deck,
#   cancel all of its effects and discard it. You may remove a metal counter
#   from Spider Armor -> deal 1 damage to the villain or remove 1 threat from
#   the main scheme for each boost icon discarded this way.
#
# Cartes de reference :
#  - **`im011`** Save The Day (pack iron_man_model_42), `dz013` Velvet Sky et
#    `09007` Protective Ward : `WhenPlayerRevealCard(HeroInterrupt,
#    "AnyPlayer", Treachery, "All", op)` puis
#    `message.CancelAllEffectsAndDiscardIt(effect)`.
#  - **`15004`** / `ho014` pour `FacesCounter.CountTotalBoostIcons([face])` :
#    compter les icones de boost d'une carte rencontre.
#  - `im002` pour le « you may » paye en compteur (`MayChooseOneAbility`).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « cancel **all** of its effects » : niveau d'annulation `"All"`, PAS
#    `"WhenRevealed"`, qui laisserait passer les mots-cles, Surge compris.
#    Leçon dz013, payee en partie reelle.
#  - « revealed **from the encounter deck** » : `from_encounter=True`. C'est
#    la difference exacte avec im011, qui imprime « When a treachery is
#    revealed » tout court et attrape donc aussi une revelation depuis la
#    defausse.
#  - « for each boost icon **discarded this way** » : les icones de la
#    traitrise que CETTE carte vient d'annuler et de defausser, pas celles
#    d'un paquet de boost. Le decompte se fait donc sur `message.trigger`.
#  - « deal 1 damage to the villain **or** remove 1 threat from the main
#    scheme » : un CHOIX entre deux effets, pas les deux. Et « the villain » /
#    « the main scheme » sont nommes, il n'y a aucun ciblage a offrir.
#  - « **You may** remove a metal counter » : facultatif. L'annulation, elle,
#    tombe toujours — c'est le coeur de la carte, le bonus n'en est que la
#    prime. D'ou le retrait dans le corps (`RetirerUnMetal`), pas dans le
#    cout : sans compteur la carte annule quand meme.
#  - ⚠ ARBITRAGE TECHNIQUE (§9 du GUIDE) : les deux options sont proposees
#    dans UNE SEULE question, chacune portant deja le retrait du compteur,
#    plutot qu'en deux temps (« veux-tu payer ? » puis « quel effet ? »). Deux
#    questions enchainees sur la meme capacite ont bloque une partie
#    d'autoplay au pack lady_sif le 03/09/2026 : le pilote epuise son
#    compteur de repetitions avant d'avoir repondu aux deux.


def GetAbilities() -> Sequence['Ability']:

    def sense_it(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        this = effect.this.CastTo(Event)

        traitrise = message.trigger
        icones = FacesCounter.CountTotalBoostIcons([traitrise]) if traitrise else 0

        message.CancelAllEffectsAndDiscardIt(effect)

        if icones <= 0 or CompteursMetal(effect) < 1:
            return

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        def degats_au_vilain(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            if not RetirerUnMetal(effect):
                return
            vilains = Worlds.GetVillains(effect)
            if vilains:
                this.DealDamage([vilains[0]], icones, effect)

        def menace_du_principal(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            if not RetirerUnMetal(effect):
                return
            this.RemoveThreatFromSchemes("MainScheme", icones, effect)

        initiator.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                f"Remove 1 metal counter -> deal {icones} damage to the villain",
                degats_au_vilain,
            ),
            AbilityFactory.ForChoiceAbility(
                f"Remove 1 metal counter -> remove {icones} threat from the main scheme",
                menace_du_principal,
            ),
        )

    return [
        AbilityFactory.WhenPlayerRevealCard(
            AbilityType.HeroInterrupt,
            "AnyPlayer",
            Treachery,
            "All",
            sense_it,
            from_encounter=True,
        ).SetPlay(),
    ]
