from cards.pack import *

# ===========================================================================
# Scenario 5 SUPREME INTELLIGENCE (Galactic Storm, Kajislav) — gs195-gs208.
# Livret 1.2 p.19 et insert du scenario. Paquet de rencontre : Supreme
# Intelligence, Starforce (OBLIGATOIRE), Seeds of Corruption (modulaire par
# defaut), Standard (+ Expert).
#
# Regles propres :
#  - 1A (Setup) : chaque sbire STARFORCE est mis de cote, l'un d'eux au hasard
#    entre en jeu engage avec le premier joueur ; Holding Tank (mis de cote par
#    le scenario) s'attache au mechant.
#  - 1B : chaque fois que le complot serait complete, toute la menace part et un
#    sbire STARFORCE mis de cote au hasard entre en jeu ; a 5 sbires STARFORCE
#    mis de cote ou moins, on avance au stade 2A (qui remelange les autres).
#
# ⚠ Lecture retenue en attendant la reponse (question Q1 du lot GS-8,
# .planning/todos/2026-10-20-gs8-questions.md) : Supremor (gs204) porte le
# trait STARFORCE, il est donc mis de cote par 1A comme les huit sbires du set
# Starforce (10 sbires STARFORCE au total).
# ===========================================================================

NOM_MECHANT = "Supreme Intelligence"
NOM_RESERVOIR = "Holding Tank"


def LeMechant(effect: 'Effect') -> 'Villain|None':
    return Worlds.FindVillain(effect)


def SbiresStarforceMisDeCote(effect: 'Effect') -> List['CardFace']:
    """« set aside STARFORCE minion(s) » : les sbires au trait STARFORCE de la zone mise de cote."""
    return list(Worlds.GetSetAsideAreaCards(effect, CardFinder(card_type=Minion, trait="STARFORCE")))


def MettreEnJeuUnStarforceAuHasard(effect: 'Effect') -> 'CardFace|None':
    """« put a random set aside STARFORCE minion into play engaged with the first player ». Aucun
    sbire mis de cote : rien."""
    sbires = SbiresStarforceMisDeCote(effect)
    if not sbires:
        return None
    sbire = Rand.RandomChoice(sbires, effect)
    sbire.PutIntoPlay(Worlds.GetFirstPlayer(effect), effect)
    return sbire


def MettreDeCoteLesSbiresStarforce(effect: 'Effect') -> List['CardFace']:
    """1A, Setup : « Set each STARFORCE minion aside » (deck rencontre et table)."""
    return SetupCards.SetAsideCards(effect, card_type=Minion, trait="STARFORCE")


def EtaitElite(message: 'Message.AfterUnitBeDefeated') -> bool:
    """« If that minion has the ELITE trait » : le trait imprime OU gagne (Genetic Augmentation) AU MOMENT
    de la defaite. Genetic Augmentation note l'etat sur le message de defaite (voir gs201), car
    l'attachement quitte le jeu avec le sbire et le trait gagne disparait avant la Reponse."""
    sbire = message.trigger
    if sbire.HasTrait("ELITE"):
        return True
    return bool(getattr(message.would_defeated_message, "gs_elite_a_la_defaite", False))


def ReponseSbireKreeVaincu(boost_si_elite_seulement: bool) -> 'Ability':
    """Supreme Intelligence (I)/(II) : « After a KREE minion is defeated, heal 1 damage from the villain.
    If that minion has the ELITE trait, give the villain a facedown boost card. » ; (III) : « ... heal 1
    damage from the villain and give it a facedown boost card. »"""

    def vaincu(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        mechant = effect.this.CastTo(Villain)
        mechant.HealthUnits([mechant], 1, effect)
        if not boost_si_elite_seulement or EtaitElite(message):
            Faces.GiveFacedownBoostCards([mechant], 1, effect)

    return AbilityFactory.AfterUnitBeDefeated(
        AbilityType.ForcedResponse,
        CardFinder(card_type=Minion, trait="KREE"),
        vaincu,
    )
