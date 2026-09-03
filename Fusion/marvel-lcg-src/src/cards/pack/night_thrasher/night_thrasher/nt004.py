from . import *

# Drop In — evenement signature, x2 (n/16 = 3 et 4). SKILL.
# Cout 1, ressource [mental].
# Hero Response: After you change to hero form, if the Battle Board upgrade
#   has the:
#   • [[VEHICLE]] trait, confuse an enemy.
#   • [[WEAPON]] trait, stun an enemy.
#
# Cartes de reference :
#  - **`01019a`** / `12001a` / `bt001b` : `AfterUnitChangeForm(type, "You",
#    op, to_form=Hero)` pour « After you change TO HERO form ».
#  - **`08013`** Stealth Strike pour le ciblage DANS l'operation : la nature
#    du statut depend de la face de la planche, et les filtres de cible ne
#    sont pas les memes (`canbe_confused` / `canbe_stunned`).
#  - `05015` / `01083` pour `Faces.GiveStatus(cibles, "Confused"|"Stunned",
#    effect)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « change **to hero form** » : PAS « change form » tout court. C'est la
#    difference exacte avec `nt008` The Mancave, qui se declenche dans les
#    DEUX sens. `to_form=Hero`, sans quoi la carte se declencherait aussi en
#    rangeant le costume — moment ou elle est de toute facon injouable,
#    etant une `Hero Response`.
#  - « confuse » cote VEHICLE, « stun » cote WEAPON : ne PAS les intervertir.
#    Le vehicule empeche de manigancer, l'arme empeche de frapper — la
#    correspondance est thematique et elle est imprimee.
#  - Les filtres `canbe_confused` / `canbe_stunned` ne sont pas decoratifs :
#    un ennemi Stoique peut absorber le statut, un ennemi qui ne peut pas
#    l'etre ne doit pas etre propose (leçon 05015).
#  - Les deux branches sont EXCLUSIVES, et aucune ne tombe sans planche.
#  - Aucun libelle : ce n'est ni une attaque ni une menee, malgre le statut
#    inflige.


def GetAbilities() -> Sequence['Ability']:

    def drop_in(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        if PlancheEstVehicule(effect):
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Confuse an enemy",
                    lambda cibles: Faces.GiveStatus(cibles, "Confused", effect),
                ).SetTarget(Enemy, canbe_confused=True),
            )
        elif PlancheEstArme(effect):
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Stun an enemy",
                    lambda cibles: Faces.GiveStatus(cibles, "Stunned", effect),
                ).SetTarget(Enemy, canbe_stunned=True),
            )

    return [
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.HeroResponse,
            "You",
            drop_in,
            to_form=Hero,
        ).SetPlay(),
    ]
