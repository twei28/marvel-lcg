from . import *

# * Colleen Wing — ALLIE 3 [physical], aspect Basic (Iron Fist 21). HERO FOR HIRE. MARTIAL ARTIST. PV 3, THW 1*, ATK 2*.
# [star] Colleen Wing takes −1 consequential damage (✪) after she attacks an enemy who has been attacked by another
#   MARTIAL ARTIST character this phase.
#
# CARTES DE REFERENCE
#  - `33016` Coordinated Attack : `WhenUnitWouldAttack(NonKeyword, Ally, ..., attack_targets=...)` + `ally.GainForThisActive(
#    effect, message, attack_consequential_damage=-1)` = la reduction « pour CETTE attaque ».
#  - `32091` Cannonball : le meme geste sur une capacite etoilee (`AbilityType.NonKeywordStar`).
#  - moteur : `world.stat.this_phase_made_attack` (AJOUT du 22/10/2026) = (attaquant, effet, cibles) de TOUTE la phase,
#    la liste par TOUR (`this_turn_made_attack`) etant videe a chaque tour de joueur.
#
# TEXTE CONTRE CODE
#  ⚠ « an enemy WHO HAS BEEN attacked » : l'attaque de Colleen elle-meme ne compte pas ; il faut une attaque ANTERIEURE.
#  ⚠ « ANOTHER Martial Artist character » : un personnage (heros ou allie) au trait MARTIAL ARTIST, jamais Colleen.
#  ⚠ « THIS PHASE » : toute la phase des joueurs (autre tour de joueur compris), pas seulement le tour en cours.
#  ⚠ « −1 consequential damage » : 1 degat consecutif imprime (ATK 2*) moins 1 = 0 ; la THW n'est pas touchee.


def EnnemiDejaAttaqueParArtisteMartial(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
    this = effect.this
    cibles = [c for c in message.attacked_targets if c is not None]
    for attaquant, _, attaquees in effect.world.stat.this_phase_made_attack:
        if attaquant is this or attaquant is None or not attaquant.HasTrait("MARTIAL ARTIST"):
            continue
        if any(c in attaquees for c in cibles):
            return True
    return False


def GetAbilities() -> Sequence['Ability']:

    def colleen_wing(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Ally)
        this.GainForThisActive(effect, message, attack_consequential_damage=-1)

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.NonKeywordStar,
            "This",
            colleen_wing,
            conditions=[EnnemiDejaAttaqueParArtisteMartial],
        ),
    ]
