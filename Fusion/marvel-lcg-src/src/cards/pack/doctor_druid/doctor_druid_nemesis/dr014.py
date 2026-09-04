from . import *

# Resurrection of Nekra — TRAITRISE NEMESIS. 2 icones de boost.
# When Revealed: If Nekra is in play, she activates against you. Otherwise,
#   search the encounter deck and discard pile for Nekra and reveal her.
#
# CARTE DE REFERENCE
#  - `yd018` Savage Destruction (pack yondu) : structure identique, « si le
#    sbire est la il agit, sinon on le convoque ».
#
# TEXTE CONTRE CODE
#  « she ACTIVATES against you » -> `DoActivate`, donc son activation
#    COMPLETE (attaque ou manigance selon les regles), pas une simple attaque.
#    C'est la difference avec yd018, qui dit « attacks you ».
#  « search the encounter deck AND DISCARD PILE » -> les deux zones, sans quoi
#    la carte serait inerte des la premiere mort de Nekra, cas que cette carte
#    existe precisement pour couvrir.


def GetAbilities() -> Sequence['Ability']:

    def resurrection(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        joueur = message.GetToPlayer()

        nekra = NekraEnJeu(effect)
        if nekra is not None:
            if joueur is not None:
                nekra.CastTo(Enemy).DoActivate(joueur, effect)
            return

        trouvee = ChercherNekra(effect)
        if trouvee is not None:
            trouvee.Reveal(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            resurrection,
        ),
    ]
