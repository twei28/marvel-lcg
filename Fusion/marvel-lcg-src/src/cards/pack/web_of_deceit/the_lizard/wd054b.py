from . import *

# * Curt Connors (B)

def GetAbilities() -> Sequence['Ability']:

    def au_lieu_dattaquer(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        # « [star] Forced Interrupt: When Curt Connors would attack, remove
        # 1 sanity counter from Lizard Brain instead. » Connors se bat contre
        # son propre cerveau, pas contre les heros.
        message.SetBeInstead(effect)
        RetirerUnCompteurDeSante(effect)

    def en_complotant(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        # « After this activation, remove 1 sanity counter from Lizard Brain. »
        RetirerUnCompteurDeSante(effect)

    return [
        # « HIT POINTS ∞ » : le moteur ne connait pas les PV infinis, et les PV
        # sont de toute facon portes par la CARTE, pas par la face. On rend donc
        # le sens jouable de la phrase — Connors ne peut pas etre vaincu — et la
        # fiche affiche les PV de The Lizard. ECART DE FORME, ecrit.
        *AbilityFactory.UnitCannotBeDefeatedWhile(
            AbilityType.NonKeywordBold,
            "This",
        ),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            "This",
            au_lieu_dattaquer,
        ),
        # « [star] Forced Interrupt: When Curt Connors schemes, this activation
        # removes threat instead of placing it. »
        AbilityFactory.WhenUnitWouldScheme(
            AbilityType.ForcedInterrupt,
            "This",
            lambda effect, message: message.SetRemoveThreatInsteadOfPlacing(effect),
        ),
        AbilityFactory.AfterUnitSchemeEnd(
            AbilityType.ForcedResponse,
            "This",
            en_complotant,
        ),
    ]
