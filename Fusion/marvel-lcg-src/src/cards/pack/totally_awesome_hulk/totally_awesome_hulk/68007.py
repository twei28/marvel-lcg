from . import *

# The Power of Forgiveness — custom « DesignHacker »
# Response: After you resolve the effects of the card you paid for with The
#   Power of Forgiveness, remove all counters from "The Trunk" and heal 2 hit
#   points from another friendly character.


def GetAbilities() -> Sequence['Ability']:

    def autres_personnages_amis(effect: 'Effect') -> List['CardFace']:
        initiator = effect.GetInitiator()
        identity = initiator.GetIdentity()
        return [
            x for x in Worlds.FindCardsOnField(effect, card_type=Friend)
            if x != identity
        ]

    def the_power_of_forgiveness(effect: 'Effect', message: 'Message.WhenCardBeSpendAsResource') -> None:
        initiator = effect.GetInitiator()
        identity = initiator.GetIdentity()

        def apres_resolution(effect2: 'Effect', message2: 'Message.AfterEffectResolved') -> None:
            joueur = effect2.GetInitiator()

            # Le retrait des compteurs est INCONDITIONNEL. Le declarer en
            # `SetTarget` avec le soin liait les deux : sans autre personnage
            # ami en jeu (le cas normal en solo tant qu'aucun allie n'est pose),
            # l'abilite n'avait aucune cible legale, ne partait jamais, et
            # « The Trunk » gardait ses compteurs.
            trunk = FindTrunk(effect2, joueur)
            if trunk:
                Faces.RemoveCountersOn(trunk, "All", 'rage', effect2)

            cibles = autres_personnages_amis(effect2)
            if not cibles:
                return

            joueur.ChooseAbilities(
                effect2,
                AbilityFactory.ForChoiceAbility(
                    "Heal 2 hit points from another friendly character",
                    lambda targets: effect2.this.HealthUnits(targets, 2, effect2),
                # CORRECTIF (4/8/2026) : meme piege que Fetch! 78001a, une
                # liste de faces se passe par `faces=`, sinon TypeError.
                ).SetTarget(Select.From(faces=cibles), canbe_heal=True),
            )

        # L'abilite differee est portee par l'IDENTITE, pas par la ressource :
        # celle-ci est defaussee au moment meme du paiement, ce qui emportait
        # ses effets temporaires avant que la carte payee ne se resolve.
        identity.effect.RegisterTemp(
            AbilityFactory.AfterCardResolveAbility(
                AbilityType.Response,
                None,
                CardFace,
                apres_resolution,
                which_effect=message.for_effect,
            ),
            unregister_after_exec=True,
            until_resolve_effect=message.for_effect,
        )

    return [
        AbilityFactory.WhenYouSpendThisCardToPlay(
            AbilityType.Response,
            the_power_of_forgiveness,
        ),
    ]
