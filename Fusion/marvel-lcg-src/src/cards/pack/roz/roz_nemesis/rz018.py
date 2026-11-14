from . import *

# Legal Council — MANIGANCE ANNEXE nemesis, menace 2 par joueur, boost 2, 1 icone Acceleration.
# Forced Interrupt: When you would exhaust or use a "Special" ability on an upgrade you control, spend 1 resource
#   of any type or cancel its effects.
#
# CARTES DE REFERENCE (PROCESSUS-CARTE etape 2)
#  - « When X would resolve ... cancel » : `AbilityFactory.WhenCardWouldResolveAbility` (resolve.py:48) ; l'effet
#    est annule par `message.SetBeInstead(effect)` (`CanBeInstead`, message_type.py:256).
#  - « spend 1 resource of any type » : `Cost("1")` = N'IMPORTE QUELLE ressource (rainy 90115 / 90123 : `CostFunc.Spend(Cost("1"))`) ;
#    `Cost("G")` n'est PAS cela : c'est une icone WILD imprimee (04166) que ni Strength (RR) ni Energy ne fournissent. Choix par
#    `joueur.ChooseAbilities(effect, ForChoiceAbilityWithCost(Cost("1"), nom), ForChoiceAbility(...))` (modele `27176`).
#  - icone Acceleration imprimee : `01109` Bomb Scare (`desc.Acceleration = "1"`), menace par joueur : `StartingThreat "2*"`.
#
# MOTS-PIEGES
#  - « EXHAUST OR USE a Special ability » : deux declencheurs, UN seul prix par declenchement. Rendu : tout effet
#    d'une amelioration que tu controles qui est un Special OU dont le cout incline la carte.
#  - « spend 1 resource OF ANY TYPE OR cancel its effects » : le JOUEUR choisit ; sans ressource a depenser,
#    seule l'annulation reste.
#  - « upgrade YOU control » : seules les ameliorations du joueur, pas celles des autres.
#  - « YOU » : tout joueur, pour SES ameliorations : le joueur interroge est le CONTROLEUR de l'amelioration
#    (`message.control_by`), pas le joueur d'un effet de la manigance (qui n'en a pas).
#  - ⚠ LECTURE PROVISOIRE : le moteur n'a AUCUN message « would exhaust » (seulement `AfterCardExhausted`). On lit donc
#    « exhaust OR use a Special » comme : toute capacite d'amelioration dont un COUT incline la carte (`CostFunc.Exhaust`
#    sur « This ») ou qui EST un Special. Le cout d'inclinaison est deja paye quand l'effet va se resoudre : annuler
#    l'effet laisse donc l'amelioration inclinee. Voir la question en attente du gabarit.
def GetAbilities() -> Sequence['Ability']:

    def incline_cette_amelioration(ability: 'Ability') -> bool:
        return any(isinstance(c, CostFunc.Exhaust) and getattr(c, "exige_cette_carte_en_jeu", False)
                   for c in ability.cost_funcs)

    def conseil_juridique(effect: 'Effect', message: 'Message.WhenEffectWouldResolve') -> None:
        Unused(effect)
        joueur = message.control_by
        if not Player.IsType(joueur):
            return
        ability = message.effect.ability
        if not (ability.type == AbilityType.Special or incline_cette_amelioration(ability)):
            return
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbilityWithCost(
                Cost("1"),
                "Spend 1 resource of any type",
            ),
            AbilityFactory.ForChoiceAbility(
                "Cancel its effects",
                lambda targets: message.SetBeInstead(effect),
            ),
        )

    return [
        AbilityFactory.WhenCardWouldResolveAbility(
            AbilityType.ForcedInterrupt,
            None,
            CardFinder(card_type=Upgrade),
            conseil_juridique,
            card_control_by="AnyPlayer",
            trigger_player="AnyPlayer",
        ),
    ]
