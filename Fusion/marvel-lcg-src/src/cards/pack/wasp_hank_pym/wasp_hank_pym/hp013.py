from . import *
# Identity Crisis — obligation (Give to Hank Pym). Forced Response : apres un changement de forme, 1 compteur crisis ici ;
# a 5 ou plus : « find Shadow of the Past and reveal it. If you cannot, place 7 pursuit counters on Pursued by the Past ».
# CORRECTIF 26/10/2026 : ces deux cartes ne manquent PAS, ce sont des cartes OFFICIELLES du moteur : Shadow of the Past `01190`
# (traitrise du set Standard, dans le deck rencontre ou sa defausse : RR FIND) et Pursued by the Past `45075a/b` (environnement
# permanent du set Standard III, `AfterCounterPlacedOn 'pursuit'`). Modele de la recherche + revelation : `hp018`, `sk193a`.
# Alter-Ego Action : « Choose to take 1 damage or place 1 threat on the main scheme for each crisis counter here. Then, exhaust
# Hank Pym -> discard this obligation ». CORRECTIF 26/10/2026 (RR COST ARROW ICON) : TOUT ce qui precede la fleche est le COUT
# (le choix degats / menace ET l'inclinaison de Hank Pym) ; l'effet est la defausse. L'Action n'est donc pas offerte si Hank Pym
# est deja incline (modele 40160 Manufactured Drama : `Exhaust("YourIdentity")` en cout).
def GetAbilities() -> Sequence['Ability']:
    def crise(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Obligation)
        # Forced Response d'une obligation : l'« initiateur » est le vilain ; le joueur est celui dont l'identite a change de forme.
        joueur = message.trigger.GetControlByPlayer()
        Faces.PlaceCountersOn([this], 1, 'crisis', effect)
        if this.GetCounters('crisis') < 5:
            return
        ombre = Search.EncounterCard(effect, include_discard_pile=True, name="Shadow of the Past", card_type=Treachery)
        if ombre is not None:
            ombre.Reveal(joueur, effect)
            return
        poursuite = Worlds.FindCardOnField(effect, name="Pursued by the Past")
        if poursuite is not None:
            from game.effect.rule import GameRule
            # 45075a ne reagit qu'a un compteur pose PAR UN JOUEUR (`place_player`, sender_token.py) : l'effet de cette obligation a le
            # vilain pour initiateur et un message d'unite, donc aucun joueur. `GameRule(identite)` (modele iron_lad) porte le joueur.
            Faces.PlaceCountersOn([poursuite], 7, 'pursuit', GameRule(joueur.GetIdentity()))
    def cout_du_choix(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        """« Choose to take 1 damage or place 1 threat on the main scheme for each crisis counter here » : fait partie du COUT.
        Les degats pris comme cout doivent l'etre en entier (RR COST : « not considered paid unless all of that damage was taken »)."""
        from game.ability.cost_func import TakeDamageOnCall
        this = effect.this.CastTo(Obligation)
        joueur = effect.GetInitiator()
        identite = joueur.GetIdentity()
        n = this.GetCounters('crisis')
        if n == 0:
            return True
        paye: List[bool] = []
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Take 1 damage for each crisis counter",
                lambda cibles: paye.append(TakeDamageOnCall([identite], n, effect)),
            ),
            AbilityFactory.ForChoiceAbility(
                "Place 1 threat on the main scheme for each crisis counter",
                lambda cibles: (this.PlaceThreatOnSchemes("MainScheme", n, effect), paye.append(True)),
            ),
        )
        return bool(paye) and paye[0]
    def sortir(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)
        Faces.DiscardAll([this], effect)
    return [
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.ForcedResponse,
            "You",
            crise,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            sortir,
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity"))
        .SetCostFunc(CostFunc.Custom(None, cout_du_choix)),
    ]
