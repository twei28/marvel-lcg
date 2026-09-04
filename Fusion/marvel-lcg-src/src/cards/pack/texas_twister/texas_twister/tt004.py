from . import *

# Keep Spinning — EVENEMENT, cout 1, [energy]. SUPERPOWER. CINQ EXEMPLAIRES.
# Hero Response: After you use one of Texas Twister's basic powers (THW, ATK,
#   or DEF), ready Texas Twister.
#
# CARTE DE REFERENCE
#  - `14001a` Quicksilver : meme effet mot pour mot, mais imprime sur
#    l'identite et limite une fois par phase. Ici c'est un evenement, donc la
#    limite est le nombre d'exemplaires en main.
#
# TEXTE CONTRE CODE
#  CINQ EXEMPLAIRES dans le deck de depart : c'est la carte la plus jouee du
#    pack, et la raison pour laquelle tt001a n'a pas de limite — chaque
#    redressement rend un pouvoir de base, qui redonne +1.
#  « ready TEXAS TWISTER » -> l'identite, cible declaree par
#    `.SetTarget("YourHero")` (idiome Quicksilver) plutot que retrouvee a la
#    main : le moteur affiche alors la cible au joueur.


def GetAbilities() -> Sequence['Ability']:

    def continuer_a_tourner(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        Faces.ReadyAll(effect.targets, effect)

    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.HeroResponse,
            "You",
            continuer_a_tourner,
            powers=POUVOIRS_DE_BASE,
        ).SetPlay().SetTarget("YourHero"),
    ]
