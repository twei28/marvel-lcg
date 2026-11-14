from . import *

# Nega-Bomb (222A) — COMPLOT ANNEXE (Nega-Bomb). Menace de depart 8[per_hero], aucune icone de boost.
# Setup. Victory 0.
# Enters play with 4 time counters on it.
# Forced Response: After resolving step one of the villain phase, remove 1 time counter from here. If there
#   is no time counter here, flip this card and reveal Detonation.
#
# Cartes de reference :
#  - **`raphael/tr014`** Mutagen Bomb : `AfterResolveVillainPhaseStep(ForcedResponse, 1, op)` = « after
#    resolving step one of the villain phase », compteur pose puis seuil.
#  - **`gmw/16034`** / `dz002` : `ThisEnterPlayWithCounters(4, 'time')` = « enters play with 4 time
#    counters ».
#  - **`mut_gen/32065a`** Find the Senator : `this.card.Flip(effect)`, complot annexe dont le verso est un
#    ENVIRONNEMENT ; la face revelee est relue par `this.card.face`.
#  - Setup / Victory : bases AUTOMATIQUES (`desc.Setup`, `desc.Victory`), fiches setup.md et victory.md.
#
# ⚠ Mots-pieges : « AFTER resolving step ONE » (apres la pose de menace sur le complot principal) ; « remove 1
# time counter » PUIS « if there is NO time counter here » (Green Interference peut en avoir deja retire :
# 0 compteur = on retourne) ; « flip this card AND REVEAL Detonation » (ses « When Revealed » partent) ; la
# menace presente sur la Nega-Bomb est lue par Detonation (« the amount of threat HERE ») : elle est notee
# sur la carte au moment du retournement. Victory 0 : dejouee, elle va dans la pile de victoire (0 point).


def GetAbilities() -> Sequence['Ability']:

    def apres_etape_un(effect: 'Effect', message: 'Message.AfterResolveVillainPhaseStep') -> None:
        Unused(message)
        this = effect.this.CastTo(EncounterSideScheme)
        if this.GetCounters('time') > 0:
            Faces.RemoveCountersOn([this], 1, 'time', effect)
        if this.GetCounters('time') > 0:
            return
        setattr(this.card, ATTR_MENACE, this.threat)
        # Le retournement d'un complot annexe vers une face NON complot REVELE deja cette face (moteur, mesure
        # au journal du cas gs222a : « Detonation revelee » sans appel) : un `Reveal` en plus la revelait deux fois.
        this.card.Flip(effect)

    return [
        AbilityFactory.ThisEnterPlayWithCounters(4, 'time'),
        AbilityFactory.AfterResolveVillainPhaseStep(AbilityType.ForcedResponse, 1, apres_etape_un),
    ]
