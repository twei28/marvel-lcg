from . import *

# Star Lightning (2/2) - exemplaire physique 2/2, contenu identique a
# ma020 (voir ce fichier pour le detail des modeles et des trois
# clauses).


def GetAbilities() -> Sequence['Ability']:

    def star_lightning(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()
        if joueur is None:
            return

        def sonner(degats: int):
            Unused(degats)
            identite = joueur.GetIdentity()
            if identite is not None:
                Faces.GiveStatus([identite], "Stunned", effect)

        def deferlement():
            ThisCardGainSurge(effect, message)

        catalina = Worlds.FindCardOnField(effect, name=NOM_CATALINA,
                                          card_type=Enemy)
        if catalina:
            catalina.DoAttackYou(
                joueur,
                effect,
                if_this_attack_deals_damage=sonner,
                if_no_attack_was_made=deferlement,
            )
        else:
            deferlement()

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            star_lightning,
        ),
    ]
