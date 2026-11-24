from . import *

# Agent of Wakanda — AMELIORATION, cout 2, [physical]. TITLE. WAKANDA.
# Roz gets +1 THW.
# Response: After you resolve a "Special" ability on another card, place 1 agent counter here.
# Special: Exhaust Agent of Wakanda and remove 6 agent counters → stun or confuse an enemy.
#
# CARTES DE REFERENCE (PROCESSUS-CARTE etape 2)
#  - « gets +1 THW » : `01028` (`GiveKeywordToAttached(CardFinder(name=...), thwart=1)`).
#  - « After you resolve a Special » : `storm/36007` (`AfterPlayerResolveAbility(..., which_abilities=["Special"],
#    control_by_you=True)`).
#  - compteurs : `ch015` Stark Nunchaku (`CostFunc.Counter("This", N, 'nom')` + condition « au moins N »),
#    `ch019` (`Faces.PlaceCountersOn([this], 1, 'nom', effect)`).
#  - « stun OR confuse » : `nebu/22005` Evasive Maneuvering (`ChooseAbilities` de deux `ForChoiceAbility`).
#
# MOTS-PIEGES
#  - « on ANOTHER card » : la Reponse ne se declenche PAS sur le Special de cette carte-ci (sinon elle se
#    nourrirait elle-meme en se depensant).
#  - « exhaust AND remove 6 agent counters » : DEUX couts, tous deux obligatoires ; le Special est injouable
#    avec moins de 6 compteurs ou si la carte est inclinee.
#  - compteur `agent` : declare dans `CardFace.COUNTER` (CORRECTIF du 25/10/2026) et `compteurs-fr.ts`.
def GetAbilities() -> Sequence['Ability']:

    def six_compteurs(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> bool:
        Unused(message)
        return effect.this.GetCounters(NOM_COMPTEUR_AGENT) >= 6

    def un_agent_de_plus(effect: 'Effect', message: 'Message.AfterEffectResolved') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        Faces.PlaceCountersOn([this], 1, NOM_COMPTEUR_AGENT, effect)

    def une_autre_carte(effect: 'Effect', message: 'Message.AfterEffectResolved') -> bool:
        return message.trigger is not effect.this

    def etourdir_ou_embrouiller(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Stun an enemy",
                lambda targets: Faces.GiveStatus(targets, "Stunned", effect),
            ).SetTarget(Enemy, canbe_stunned=True),
            AbilityFactory.ForChoiceAbility(
                "Confuse an enemy",
                lambda targets: Faces.GiveStatus(targets, "Confused", effect),
            ).SetTarget(Enemy, canbe_confused=True),
        )

    return [
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Roz"),
            thwart=1,
        ),
        AbilityFactory.AfterPlayerResolveAbility(
            AbilityType.Response,
            "You",
            None,
            un_agent_de_plus,
            which_abilities=["Special"],
            control_by_you=True,
            conditions=[une_autre_carte],
        ),
        AbilityFactory.WhenResolveSpecialAbility(
            "This",
            etourdir_ou_embrouiller,
            conditions=[six_compteurs],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 6, NOM_COMPTEUR_AGENT)),
    ]
