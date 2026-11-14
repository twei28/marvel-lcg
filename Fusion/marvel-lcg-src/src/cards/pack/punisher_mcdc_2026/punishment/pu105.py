from . import *

# Say Good Night — TRAITRISE. Boost 1.
# When Revealed (Alter-Ego) : Deal damage to the TARGETED villain equal to Punisher's ATK.
# When Revealed (Hero) : Take damage equal to Punisher's ATK. You may exhaust your hero or discard an ally you control to
#   prevent this damage.
#
# Cartes de reference : pu100 (`WhenThisRevealed("Alter-Ego"|"Hero")`), `ChooseAbilities` (pu059), `TakeDamage`.
# ⚠ « damage EQUAL TO Punisher's ATK » : son ATQ courant (bonus d'armes et de Target Lock compris) ; « You may exhaust your hero OR
# discard an ally » : prevenir TOUT ce degat, une seule des deux options, la derniere etant impossible sans allie.

def GetAbilities() -> Sequence['Ability']:

    def alter_ego(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        punisher = Punisher(effect)
        cible = VilainCible(effect)
        if punisher is not None and cible is not None:
            effect.this.DealDamage([cible], punisher.attack, effect)

    def heros(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        punisher = Punisher(effect)
        if joueur is None or punisher is None:
            return
        degats = punisher.attack

        def prendre() -> None:
            joueur.GetIdentity().TakeDamage(this, degats, effect)

        options = [AbilityFactory.ForChoiceAbility("Take the damage", lambda cibles: prendre())]
        identite = joueur.GetIdentity()
        if identite.IsReady():
            options.append(AbilityFactory.ForChoiceAbility("Exhaust your hero to prevent this damage", lambda cibles: Faces.ExhaustAll([identite], effect)))
        allies = [a for a in joueur.GetControlCharacters() if Ally.IsType(a)]
        if allies:
            def defausser(cibles):
                choisi = allies[0] if len(allies) == 1 else joueur.AskChooseFace(allies, effect)
                if choisi is not None:
                    Faces.DiscardAll([choisi], effect)
            options.append(AbilityFactory.ForChoiceAbility("Discard an ally you control to prevent this damage", defausser))
        joueur.ChooseAbilities(effect, *options)

    return [
        AbilityFactory.WhenThisRevealed("Alter-Ego", alter_ego),
        AbilityFactory.WhenThisRevealed("Hero", heros),
    ]
