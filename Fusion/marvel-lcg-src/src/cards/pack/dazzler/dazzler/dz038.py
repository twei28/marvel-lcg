from . import *

# Love from Beyond the Stars
# Team-Up (Dazzler and Longshot). Max 1 per deck.
# Hero Action: Choose:
#   - Confuse an enemy.
#   - Stun an enemy.
#   Then, give Dazzler a sound counter and Longshot a knife counter.
#
# Le mot-cle Team-Up est porte par le desc (`"TeamUp": "Dazzler;Longshot"`) :
# le moteur exige alors que les DEUX personnages soient en jeu pour jouer la
# carte, et que l'identite choisie soit l'une des deux pour l'inclure au deck.
# Le separateur est un POINT-VIRGULE (has_teamup.py:18) ; la virgule fait
# planter la creation de la carte.
#
# Le compteur `sound` pose sur Dazzler n'a aucun consommateur dans la version
# de la carte heros retenue — voir la note de dz018.


def GetAbilities() -> Sequence['Ability']:

    def amour_des_etoiles(effect: 'Effect',
                          message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        def confondre(targets: Sequence['CardFace']) -> None:
            Faces.GiveStatus(targets, "Confused", effect)

        def etourdir(targets: Sequence['CardFace']) -> None:
            Faces.GiveStatus(targets, "Stunned", effect)

        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility("Confuse an enemy", confondre)
            .SetTarget(Enemy, canbe_confused=True),
            AbilityFactory.ForChoiceAbility("Stun an enemy", etourdir)
            .SetTarget(Enemy, canbe_stunned=True),
        )

        # « THEN » : les compteurs se posent quel que soit le choix.
        identite = joueur.GetIdentity()
        if identite is not None and identite.IsName(NOM_HEROS):
            identite.PlaceCountersInternal(1, COMPTEUR, effect)
        longshot = Worlds.FindCardOnField(effect, name="Longshot")
        if longshot is not None:
            longshot.PlaceCountersInternal(1, 'knife', effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            amour_des_etoiles,
        ).SetPlay().SetLabel()
        # OBLIGATOIRE sur un evenement Team-Up (database.py:222) : c'est ce
        # selecteur qui exige Dazzler ET Longshot en jeu. Les cibles des deux
        # branches du « Choose » sont portees par leurs propres capacites.
        .SetTarget("TeamUp"),
    ]
