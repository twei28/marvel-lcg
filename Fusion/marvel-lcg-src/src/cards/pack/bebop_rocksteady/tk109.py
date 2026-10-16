from . import *

# * Power Play (manigance joueur Linked)

def GetAbilities() -> Sequence['Ability']:

    def hors_limite(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        for face in effect.this.card.printed_faces:
            face.not_count_player_side_scheme_limit = True

    def apres_retrait(effect: 'Effect', message: 'Message.AfterSchemeRemoveThreat') -> None:
        this = effect.this
        this.RemoveThreatFromSchemes([this], 2, effect)

    def retire_par_vous(effect: 'Effect', message: 'Message.AfterSchemeRemoveThreat') -> bool:
        controleur = effect.this.GetControlByPlayer()
        par = message.would_remove_message.by_face
        if controleur is None or par is None:
            return False
        if par == controleur.GetIdentity():
            return True
        return par == effect.this and message.would_remove_message.by_effect.initiator is controleur

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        def action(joueur: 'Player') -> None:
            joueur.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Stun and confuse an enemy",
                    lambda targets: (Faces.GiveStatus(list(targets), "Stunned", effect),
                                     Faces.GiveStatus(list(targets), "Confused", effect))
                ).SetTarget(Enemy),
            )
        Players.ForEachPlayer(effect, action)

    return [
        AbilityFactory.AfterCardEnterPlay(AbilityType.Temp0, "This", hors_limite),
        # « Hero Response: After you remove threat from this scheme, discard 1 card from
        # your hand -> remove 2 threat from this scheme. »
        AbilityFactory.AfterSchemeRemoveThreat(
            AbilityType.HeroResponse, "This", apres_retrait,
            # « After YOU remove threat » : l'identite du controleur (pas ses allies), ou la
            # carte elle-meme quand c'est SA Reponse (resolue par son controleur) qui retire :
            # la Reponse se redeclenche alors (tranche par l'utilisateur le 16/10/2026, Q6).
            conditions=[lambda effect, message: retire_par_vous(effect, message)],
        ).SetCostFunc(CostFunc.Discard("YourHandCards", range=(1, 1))),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
    ]
