from . import *

# Skrull Infiltration — evenement signature x2 (8/16, 9/16). SKRULL. THWART.
# Cout 2 [mental].
# Hero Action (thwart): Remove 4 threat from a scheme. You may take 2 indirect
#   damage → this thwart ignores the patrol keyword and the crisis icon
#   ([crisis]).
#
# Cartes de reference :
#  - **`rs008`** Savage She-Devil (pack red_sonja) : ignorance CONDITIONNELLE
#    de Patrol + Crisis, `SetIgnoreKeyword('Patrol', 'Crisis', condition=...)`.
#  - **`90119`** Search and Rescue : un contre qui ignore la Crise doit le
#    DECLARER sur l'abilite (le complot principal n'est plus ciblable sinon,
#    `MainScheme.CanBeThwartBy`), pas seulement le passer a la resolution.
#  - **`32008`** Steel Fist : « You may <cout> → <bonus> » dans l'effet,
#    `MayChooseOneAbility(effect, ForChoiceAbility3(...))`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « You **may** take 2 **indirect** damage → » : optionnel ; indirects =
#    repartis entre identite et allies (`TakeIndirectDamage`).
#  - TIMING : le joueur choisit sa cible AVANT de savoir s'il paiera. La
#    condition d'ignorance est donc VRAIE au ciblage (le complot principal
#    reste ciblable sous Patrouille/Crise), puis tranchee a la resolution par
#    le choix du joueur : refuser les 2 degats laisse la Patrouille / la Crise
#    s'appliquer, et le contre ne retire rien du complot principal.
#  - La question n'est posee QUE si la cible est le complot principal ET
#    qu'une Patrouille (sbire engage avec vous) ou une icone Crise bloque :
#    sinon payer 2 degats n'achete rien, et la carte retire ses 4 menaces.
#  - « a scheme » : principal ou annexe (`Scheme2`).
#  - « (thwart) » : `SetLabel('thwart')`.


def GetAbilities() -> Sequence['Ability']:

    def ignorance_payee(effect: 'Effect') -> bool:
        # Tant que la resolution n'a pas tranche, on reste ciblable.
        return getattr(effect, "sk007_ignore", True)

    def bloque(effect: 'Effect', cibles: Sequence['CardFace']) -> bool:
        if not any(MainScheme.IsType(c) for c in cibles):
            return False
        return bool(Worlds.GetCrisisFaces(effect)) or bool(MainScheme.GetPatrolFaces(effect))

    def infiltration(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        cibles = list(effect.targets)
        effect.sk007_ignore = False
        if bloque(effect, cibles):
            joueur = effect.GetInitiator()

            def payer(targets: Sequence['CardFace'], by_effect: 'Effect') -> None:
                Unused(targets, by_effect)
                joueur.GetIdentity().TakeIndirectDamage(this, 2, effect)
                effect.sk007_ignore = True

            joueur.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility3(
                    "Take 2 indirect damage: this thwart ignores patrol and crisis",
                    payer,
                ),
            )
        try:
            this.RemoveThreatFromSchemes(cibles, 4, effect, ignore_crisis=effect.sk007_ignore)
        finally:
            # L'objet Effect peut etre REUTILISE au jeu suivant de la meme carte
            # (registre par face) : sans ce menage, un refus de payer rendrait
            # le complot principal inciblable au prochain jeu.
            del effect.sk007_ignore

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            infiltration,
        ).SetPlay().SetLabel('thwart')
        .SetIgnoreKeyword('Patrol', 'Crisis', condition=ignorance_payee)
        .SetTarget(Scheme2),
    ]
