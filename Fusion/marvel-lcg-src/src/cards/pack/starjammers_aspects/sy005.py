from . import *
# * Waldo (Basic, allie 3 [mental], 2*/1*, PV 3). ANDROID. STARJAMMER.
# [star] Response: After Waldo uses a basic power, ready a VEHICLE you control.
#
# Cartes de reference : 14001a Quicksilver (`AfterUnitUseBasicPower(Response, "This", op, powers=[...])`) ; cr006 Ace Pilot (ready « a
# VEHICLE you control » : recherche des cartes en jeu portant le trait, controlees par le joueur, choix du joueur).
# L'etoile d'une Response est une convention d'IMPRESSION (RECETTES §1), pas un `NonKeywordStar`. « a basic power » : les trois.
# « a VEHICLE you control » : allie, soutien ou amelioration (Jet Bike attache) ; Waldo lui-meme n'est pas un VEHICLE.
def GetAbilities() -> Sequence['Ability']:
    def waldo(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        joueur = JoueurDe(effect)
        if joueur is None:
            return
        vehicules = [f for f in Worlds.FindCardsOnField(effect, trait="VEHICLE")
                     if f.IsInPlay() and f.GetControlByPlayer() is joueur and f.IsExhaust()]
        if not vehicules:
            return
        choisi = vehicules[0] if len(vehicules) == 1 else joueur.AskChooseFace(
            vehicules, effect, prompt="Ready a VEHICLE you control", forced=True)
        if choisi is not None:
            Faces.ReadyAll([choisi], effect)
    def un_vehicule_incline(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> bool:
        joueur = JoueurDe(effect)
        return joueur is not None and any(
            f.IsInPlay() and f.GetControlByPlayer() is joueur and f.IsExhaust()
            for f in Worlds.FindCardsOnField(effect, trait="VEHICLE"))
    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.Response,
            "This",
            waldo,
            powers=["ATK", "THW", "DEF"],
            conditions=[un_vehicule_incline],
        ),
    ]
