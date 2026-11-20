from . import *

# West Village (4) — LIEU (environnement LOCATION).
# Each player in West Village gets +1 hand size.
# Forced Interrupt: During step 3 of the villain phase, deal yourself an additional encounter card.
#
# Cartes de reference : an002 / 06007 (+N hand size : `GiveKeywordToInPlayWhenApplyThis(Identity, hand_size=..., get_new_value=fn)`),
# 39026b (`AbilityFactory.WhenVillainPhaseStepStart(ForcedInterrupt, 3, ...)` + `DealEncounterCards`), pu035 (recalcul au deplacement :
# `AfterPlayerMovedInCity`).
# ⚠ « each player IN West Village » : l'IDENTITE (les deux formes, hero et alter-ego) de chaque joueur present, pas ceux d'ailleurs.
# ⚠ « deal YOURSELF an additional encounter card » : une carte de plus POUR CHAQUE joueur present, a l'etape 3 AVANT la distribution normale.

def GetAbilities() -> Sequence['Ability']:

    def taille_ici(effect: 'Effect', face: 'CardFace') -> int:
        joueur = face.GetControlByPlayer()
        return 1 if joueur is not None and Ville.Occupe(effect, joueur, effect.this) else 0

    def carte_en_plus(effect: 'Effect', message: 'Message.WhenVillainPhaseStepStart') -> None:
        Unused(message)
        for joueur in Ville.Joueurs(effect, effect.this):
            if not joueur.is_eliminated:
                joueur.DealEncounterCards(1, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Identity, hand_size=1, get_new_value=taille_ici,
            change_on_event=OnEvent.TemplateTrigger(Message.AfterPlayerMovedInCity),
        ),
        AbilityFactory.WhenVillainPhaseStepStart(AbilityType.ForcedInterrupt, 3, carte_en_plus),
    ]
