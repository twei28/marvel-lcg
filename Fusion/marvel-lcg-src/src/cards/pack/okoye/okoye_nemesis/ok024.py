from . import *

# War Drumming (2/2)
# Exemplaire physique 2 de 2, contenu identique a ok023 (voir ce fichier pour
# le detail du modele repris, y compris l'ecart assume sur "villainous").


def GetAbilities() -> Sequence['Ability']:

    def war_drumming_hero(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()
        if joueur is None:
            return

        minions = Worlds.GetOnFieldMinions(effect)
        if not minions:
            ThisCardGainSurge(effect, message)
            return

        cible = minions[0] if len(minions) == 1 else joueur.MayChooseOneText(minions)
        if cible is None:
            return

        gagne_overkill = cible.attack >= 3
        cible.CastTo(Enemy).DoAttackYou(
            joueur, effect,
            property=AttackProperty(overkill=True) if gagne_overkill else None,
        )

    return [
        AbilityFactory.WhenThisRevealed(
            "Hero",
            war_drumming_hero,
        ),
        AbilityFactory.WhenThisRevealed(
            "Alter-Ego",
            ThisCardGainSurge,
        ),
    ]
