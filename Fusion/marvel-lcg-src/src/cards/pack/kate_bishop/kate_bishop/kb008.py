from . import *

# Hawkeye Investigations — LOCATION
# Response: After you prevent any amount of threat from being placed on a
#   scheme, remove 1 threat from a scheme.
# Response: After you prevent any amount of damage, remove 1 threat from a
#   scheme.
#
# AJOUT MOTEUR (voir sender_scheme.py et game/ability/factory/scheme.py) :
# le cote menace de « after you prevent » n'existait pas encore
# (`Message.AfterThreatBePrevented` / `AbilityFactory.AfterThreatBePrevented`),
# contrairement au cote degats qui a deja `AfterDamageBePrevented`
# (damage.py:657, utilise par abjuration mts/ebony_maw/21082.py). Ajoute en
# miroir exact pour cette carte, seule du depot a en avoir besoin.
#
# `prevent_by=("YouControl", CardFinder(...))` : « after YOU prevent », pas
# « after a specific card prevents » -- n'importe quelle carte que le joueur
# controle (Infiltrate, Evasive Shot, Athletic Agility...) declenche la
# reponse.
#
# CORRECTIF 1 (test de comportement) : un `CardFinder()` VIDE (aucun
# parametre) leve `AssertionError` a chaque verification (`checker.py:36`,
# `assert not self.is_empty`) -- il n'existe pas de CardFinder "n'importe
# quelle carte" implicite dans ce moteur. `card_type=CardFace` ne marche pas
# non plus : `CardFinder.__init__` le convertit explicitement en `None` (hack
# documente `# Hack for CardFaceType`, finder.py:220), ce qui redonne un
# finder vide. Fixe avec `check_face_fn=lambda face: True`, qui ajoute un
# parametre reellement non vide (`self.check_face_fns`) tout en acceptant
# TOUTE carte -- exactement le sens de « after you prevent [any amount] »,
# sans restreindre la source de la prevention.
#
# CORRECTIF 2 (test de comportement) : `.SetTarget(Scheme2)` ne declenche
# JAMAIS l'operation, meme conditions remplies (confirme par sonde : les deux
# `check_*` internes de la fabrique renvoient True, mais `hawkeye_investigations`
# n'est jamais appelee). `ProcessForcedEffect` (event/manager.py:345) filtre
# les effets Forced par `FilterAvailableEffects` AVANT de les executer ; sans
# cible legale trouvee par cette resolution generique de `.SetTarget()`, la
# liste devient vide et la boucle s'arrete en silence, sans exception. Fixe en
# resolvant la cible A LA MAIN (`Worlds.GetOnFieldSchemes`), sur le modele du
# CORRECTIF de kb001a (`message.attacker` au lieu de `.SetTarget("Trigger")`) :
# une capacite passive (ni Play ni CostFunc) ne doit pas s'appuyer sur la
# resolution de cible du framework, reservee aux cartes jouees depuis la main.


def GetAbilities() -> Sequence['Ability']:

    def hawkeye_investigations(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Support)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        schemes = Worlds.GetOnFieldSchemes(effect)
        if not schemes:
            return
        cible = schemes[0] if len(schemes) == 1 else joueur.MayChooseOneText(schemes)
        if cible is None:
            return
        this.RemoveThreatFromSchemes([cible], 1, effect)

    return [
        AbilityFactory.AfterThreatBePrevented(
            AbilityType.ForcedResponse,
            hawkeye_investigations,
            prevent_by=("YouControl", CardFinder(check_face_fn=lambda face: True)),
        ),
        AbilityFactory.AfterDamageBePrevented(
            AbilityType.ForcedResponse,
            hawkeye_investigations,
            who_not_take_damage="You",
            prevent_by=("YouControl", CardFinder(check_face_fn=lambda face: True)),
        ),
    ]
