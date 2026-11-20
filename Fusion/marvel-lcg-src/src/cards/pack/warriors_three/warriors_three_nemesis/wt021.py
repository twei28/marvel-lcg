from . import *


def GetAbilities() -> Sequence['Ability']:
    def fated_clash(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        joueur = message.GetToPlayer()
        soutiens = soutiens_persona_du_joueur(joueur)
        fenris = en_jeu(effect, "Fenris", Minion)
        options = []
        if len(soutiens) >= 2:
            options.append(AbilityFactory.ForChoiceAbility(
                "Exhaust two PERSONA supports you control",
                lambda cibles: Faces.ExhaustAll(cibles, effect),
            ).SetTarget(check_fn=lambda e, f: f in soutiens, from_where=["YouControlCards"], range=(2, 2)))
        if fenris is not None:
            options.append(AbilityFactory.ForChoiceAbility(
                "Fenris schemes",
                lambda cibles: fenris.CastTo(Minion).DoSchemes(joueur, effect),
            ))
        if options:
            joueur.ChooseAbilities(effect, *options)
        else:
            cherche_et_revele(effect, joueur, "Fenris")

    return [
        AbilityFactory.WhenThisRevealed(None, fated_clash),
    ]
