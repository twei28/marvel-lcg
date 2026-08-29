from . import *

# Coolest Team-Up Ever!
# Team-Up (Dazzler and Jubilee). Max 1 per deck.
# Hero Interrupt: When a treachery card is revealed from the encounter deck,
#   cancel its "When Revealed" effects, then choose to either Confuse or Stun
#   up to 2 enemies in play.
#
# Meme fenetre que Velvet Sky (dz013) et qu'Enhanced Spider-Sense (01004), mais
# elle n'annule QUE le « When Revealed » et ne defausse pas la carte.
#
# « UP TO 2 enemies » : la fourchette monte a deux, et le statut choisi
# s'applique aux deux — le texte ne propose pas un statut par ennemi.


def GetAbilities() -> Sequence['Ability']:

    def team_up(effect: 'Effect',
                message: 'Message.WhenPlayerRevealCard') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        message.CancelWhenRevealedEffect(effect)

        joueur = effect.GetInitiator()
        if joueur is None:
            return

        def confondre(targets: Sequence['CardFace']) -> None:
            Faces.GiveStatus(targets, "Confused", effect)

        def etourdir(targets: Sequence['CardFace']) -> None:
            Faces.GiveStatus(targets, "Stunned", effect)

        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility("Confuse up to 2 enemies", confondre)
            .SetTarget(Enemy, canbe_confused=True, range=(1, 2)),
            AbilityFactory.ForChoiceAbility("Stun up to 2 enemies", etourdir)
            .SetTarget(Enemy, canbe_stunned=True, range=(1, 2)),
        )

    return [
        AbilityFactory.WhenPlayerRevealCard(
            AbilityType.HeroInterrupt,
            "AnyPlayer",
            Treachery,
            "WhenRevealed",
            team_up,
            from_encounter=True,
        ).SetPlay()
        # OBLIGATOIRE sur un evenement Team-Up : le moteur verifie que le
        # PREMIER selecteur vaut « TeamUp » (database.py:222), c'est lui qui
        # exige que Dazzler ET Jubilee soient en jeu. Modele Daughters of
        # Thanos (22022).
        .SetTarget("TeamUp"),
    ]
