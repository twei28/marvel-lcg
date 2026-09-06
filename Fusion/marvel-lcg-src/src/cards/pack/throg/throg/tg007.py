from . import *

# * Foreverglade — SOUTIEN, cout 1, [wild]. LOCATION. UNIQUE.
# Alter-Ego Response: After you make a basic recovery, exhaust Foreverglade ->
#   ready Puddlegulp and draw 1 card.
#
# CARTES DE REFERENCE
#  - `45015` Sidekick : « Response: After you make a basic recovery, ... » ->
#    `AfterUnitMakeRecovery(<type>, "You", op, is_basic_recovery=True)`. C'est
#    LA fabrique de ce declencheur.
#  - `br007` * Skuttlebutt : le squelette d'un soutien signature unique
#    (`CanPlayThisSupportCard()` + un cout d'inclinaison).
#  - `53029` Harlem's Protector : une capacite reservee a la forme civile.
#
# TEXTE CONTRE CODE
#  ⚠ « ALTER-EGO Response » -> `AbilityType.AlterEgoResponse`, pas `Response`.
#    Sans ca la carte se declencherait aussi sur la recuperation d'un ALLIE en
#    forme heros, ce qui n'est pas ce qu'elle dit.
#  « after you make a BASIC recovery » -> `is_basic_recovery=True`. Une
#    guerison par carte n'est pas une recuperation de base.
#  ⚠ « ready PUDDLEGULP » -> UN NOM PROPRE, donc UNE SEULE FACE. Contrairement
#    a beta_ray_bill, les deux faces de ce heros ont des noms differents :
#    « Puddlegulp » ne designe QUE l'alter-ego. Le declencheur etant deja
#    reserve a la forme civile, l'identite en jeu est forcement la bonne — on
#    redresse donc l'identite du joueur, et le filtre par nom serait redondant
#    (meme raisonnement que `br010`, RECETTES-MOTEUR §3 « LIRE LE MOT »).
#  ⚠ Redresser l'alter-ego apres une recuperation de base est le coeur de la
#    carte : la recuperation incline l'identite, Foreverglade la relance, ce
#    qui rend une SECONDE recuperation possible dans le meme tour.
#  « exhaust Foreverglade » est devant la fleche : un COUT. La carte ne sert
#    donc qu'une fois par round, tant qu'elle n'est pas redressee.


def GetAbilities() -> Sequence['Ability']:

    def clairiere_eternelle(effect: 'Effect', message: 'Message.AfterUnitRecovery') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        identite = joueur.GetIdentity()
        if identite is not None:
            Faces.ReadyAll([identite], effect)
        joueur.DrawUp(1, effect)

    return [
        AbilityFactory.CanPlayThisSupportCard(),
        AbilityFactory.AfterUnitMakeRecovery(
            AbilityType.AlterEgoResponse,
            "You",
            clairiere_eternelle,
            is_basic_recovery=True,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
