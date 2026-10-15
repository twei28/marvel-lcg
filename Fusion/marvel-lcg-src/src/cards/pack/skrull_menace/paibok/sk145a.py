from . import *

# Mastering Superpowers 2A — complot principal, face A.
# When Revealed: Place 1 mastery counter on Paibok. Then, if Captain Paibok is in
#   play, resolve its "Boost" ability. Otherwise, search the encounter deck and
#   discard pile for Captain Paibok and attach it to Paibok. Shuffle the encounter
#   deck.
#
# Cartes de reference : **`24017`** Double Trouble (`Faces.ResolveAbility([this], player,
# AbilityType.X, effect)` : resoudre une capacite NOMMEE d'une carte, ici le Boost de
# Captain Paibok) ; **`01136`** Ultron (`Search.EncounterCard(include_discard_pile=True,
# name=...)`).
#
# ⚠ Mots-pieges : « if Captain Paibok IS IN PLAY ... OTHERWISE » : deux branches
# exclusives ; « attach it to Paibok » = elle ENTRE EN JEU et s'attache (`PutIntoPlay`, son
# « Attach to Paibok » fait le reste) ; « Shuffle the encounter deck » : toujours, a la fin
# (phrase separee, hors du « Otherwise »). Le Boost resolu est celui de LA carte : « Heal 2
# damage from Paibok ». Un 2A sans TargetThreat avance seul en 2B.


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        PoserMaitrise(effect)
        capitaine = Worlds.FindCardOnField(effect, name="Captain Paibok", card_type=Attachment)
        if capitaine is not None:
            capitaine.ResolveAbility(joueur, AbilityType.Boost, effect)
        else:
            face = Search.EncounterCard(effect, include_discard_pile=True, name="Captain Paibok", card_type=Attachment)
            if face is not None:
                face.PutIntoPlay(joueur, effect)
        Worlds.GetEncounterDeck(effect).Shuffle(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelation),
    ]
