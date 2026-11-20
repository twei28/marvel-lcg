from . import *

# * Recognizing Evil : COMPLOT ANNEXE (paysage), menace de depart 2 par joueur, Acceleration 1, boost 2. Set modulaire « Twisted Killers ».
# Excess damage dealt by KILLER minions is placed as threat here.
# When Revealed: Find a copy of Murderous Nature and reveal it.
#
# CARTES DE REFERENCE
#  - « Find a copy of X and reveal it » : `find.md` / ca015 : `Search.EncounterCard(.., include_discard_pile=True, include_set_aside=True, name=..)` + `face.Reveal(joueur, effect)`.
#  - Exces d'une attaque : `AfterUnitDefeatedUnit(.., is_from_attack=True, has_excess_damage=True)` + `message.excess_damage` (ca001a, ar005) ; menace posee sur ce complot : `this.PlaceThreatOnSchemes([this], n, effect)`.
#  - Interdire l'exces : le transfert d'overkill est un `WhenUnitWouldTakeDamage` dont `property.is_from_overkill` est vrai (damage_property.py:7, can_health.py:243) : `message.PreventDamage("All", effect)`.
#  - Acceleration 1 et menace de depart par joueur : natifs (`desc`, fiche mots-cles/acceleration.md), aucun code.
#
# TEXTE CONTRE CODE
#  « EXCESS damage dealt BY KILLER MINIONS is placed AS THREAT here » : DECISION UTILISATEUR du 03/11 (lecture B, EN REMPLACEMENT) : l'exces d'un sbire KILLER qui abat un personnage est CONVERTI en menace sur ce complot annexe et N'EST PLUS INFLIGE (le transfert d'overkill vers l'identite est empeche).
#    Seuls les sbires portant le trait KILLER (Torment, Muse, Bushwacker, tout sbire sous Murderous Nature) ; l'exces mesure ce qui depasse les PV restants du personnage abattu (attaque seulement). Sans exces, rien. « When Revealed: FIND A COPY of Murderous Nature and REVEAL it » : recherche dans le deck, la defausse et la zone de cote ; aucune copie : rien.
#  Chiffres : menace de depart 2 par joueur, Acceleration 1, boost 2.


def GetAbilities() -> Sequence['Ability']:

    killers = CardFinder(card_type=Minion, trait="KILLER")

    def recognizing_evil_revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        face = Search.EncounterCard(
            effect,
            joueur,
            include_discard_pile=True,
            include_set_aside=True,
            name=NOM_MURDEROUS_NATURE,
        )
        if face is not None:
            face.Reveal(joueur, effect)

    def exces_en_menace(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        exces = int(getattr(message, "excess_damage", 0) or 0)
        if exces > 0:
            this = effect.this
            this.PlaceThreatOnSchemes([this], exces, effect)

    def exces_non_inflige(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        message.PreventDamage("All", effect)

    def est_un_transfert_d_overkill(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        Unused(effect)
        return bool(message.property.is_from_overkill)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            recognizing_evil_revelee,
        ),
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.ForcedResponse,
            killers,
            Unit2,
            exces_en_menace,
            is_from_attack=True,
            has_excess_damage=True,
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt,
            Unit2,
            exces_non_inflige,
            who_deal_damage=killers,
            conditions=[est_un_transfert_d_overkill],
        ),
    ]
