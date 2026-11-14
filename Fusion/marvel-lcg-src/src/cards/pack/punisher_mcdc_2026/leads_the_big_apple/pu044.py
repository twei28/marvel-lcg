from . import *

# Kings of Yancy Street (6) — PISTE. Interrupt : While in Lower East Side, when you attack the villain, place that attack's damage here instead.
#   Then, if there is 8 or more damage here, add this card to the victory display, reveal the top LEAD card, and draw 1 card.
#
# Cartes de reference : fiche piste-lead.md ; `Message.WhenUnitWouldTakeDamage` (`will_take_damage`, `would_atk_message`, `SetBeInstead`),
# jetons `damage` (`Faces.PlaceTokensOn`, modele fne/typhoid_mary).
# ⚠ « instead » : le vilain NE SUBIT PAS les degats (ils partent sur la piste) ; « that attack's damage » = ce que le vilain aurait subi
# (apres boost, protection...) ; seuil 8 degats ; attaque d'un personnage du joueur (identite ou allie).

def GetAbilities() -> Sequence['Ability']:

    def est_concerne(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        joueur = Joueur(effect)
        if joueur is None or not EnLieu("pu035")(effect, message):
            return False
        attaque = getattr(message, "would_atk_message", None)
        if attaque is None or not Villain.IsType(message.trigger) or message.will_take_damage <= 0:
            return False
        return ControlePar(attaque.attacker, joueur)

    def a_la_place(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this
        n = message.will_take_damage
        message.SetBeInstead(effect)
        Faces.PlaceTokensOn([this], n, 'damage', effect)
        if this.GetTokens('damage') >= 8:
            PisteTerminee(effect, Joueur(effect))

    return [Ability(AbilityType.Interrupt, Message.WhenUnitWouldTakeDamage, [est_concerne], a_la_place)]
