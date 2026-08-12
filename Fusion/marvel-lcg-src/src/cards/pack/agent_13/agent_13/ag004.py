from . import *

# Infiltrate — custom « Rainy »
# Hero Action (thwart): Remove 3 threat from a scheme. Look at the top card of
# the encounter deck and remove 1 additional threat for each boost icon on
# that card. Then, you may discard that encounter card.
#
# Modele pour le calcul de la valeur : Astral Projection (09003, Doctor
# Strange), qui regarde le dessus du deck de rencontre, additionne les icones
# a une base fixe, puis resout `RemoveThreatFromSchemes` sur une cible choisie
# en amont par `.SetTarget(Scheme2)`. Modele pour compter les icones : Hex
# Bolt (15004, Scarlet Witch).
#
# REGARDER n'est pas DEFAUSSER : `initiator.LookAtDeck("EncounterDeck", 1,
# effect)` laisse la carte en place sur le deck, contrairement a
# `Worlds.DiscardEncounterCards` (utilise sur ag008, le Pistolet). La
# defausse finale est separee, optionnelle, et posee APRES le retrait de
# menace, dans l'ordre du texte imprime.
#
# La proposition de defausse passe par `MayChooseOneAbility` (modele : Panther
# Claws 51011). Le pilote de test decline les choix optionnels par defaut :
# ce n'est pas le probleme de cette tache, mais la carte est ecrite pour que
# ce choix soit atteignable (`accepter_choix: True`, tache 8).
#
# Cas limite couvert : deck de rencontre vide (`faces` vide) -> ni icones
# supplementaires ni proposition de defausse ; seule la base de 3 menaces
# s'applique, sans erreur.

def GetAbilities() -> Sequence['Ability']:

    def infiltrate(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()

        valeur = 3
        faces = initiator.LookAtDeck("EncounterDeck", 1, effect)
        valeur += FacesCounter.CountTotalBoostIcons(faces)

        this.RemoveThreatFromSchemes(effect.targets, valeur, effect)

        if faces:
            initiator.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Discard that encounter card",
                    lambda targets: Faces.DiscardAll(faces, effect)
                ).SetHasNoTargetEffect(),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            infiltrate
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
