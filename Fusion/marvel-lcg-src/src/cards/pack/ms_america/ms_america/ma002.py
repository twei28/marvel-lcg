from . import *

# * Alloy — ALLIE signature, custom « jakxin »
# Cout 3, PV 3, ATQ 2*, CTR 1*, [wild], Toughness 1, traits AERIAL + MUTATE.
#
# Toughness.
# Hero Response: After you resolve "Star-Gaze", Alloy gets +1 ATK until the
#   end of the turn.
#
# ---------------------------------------------------------------------------
# TOUGHNESS EST LU NATIVEMENT — AUCUN CODE ICI
#
# `desc.Toughness = "1"` : `HasToughness`
# (game/card/face/attribute/has_toughness.py) pose la carte de statut Tough a
# l'entree en jeu et restaure la valeur a chaque reset. C'est une des « bases
# automatiques » du guide, a ne pas recoder. Fiche :
# docs/reference/mots-cles/toughness.md.
#
# ATQ 2* / CTR 1* : l'etoile vaut « 1 degat consecutif » (can_attack.py:47),
# lue nativement elle aussi.
#
# ---------------------------------------------------------------------------
# LE DECLENCHEUR — « APRES QUE TU RESOUS STAR-GAZE », PAS « APRES QUE TU JOUES
# UNE CARTE SUPERPOWER »
#
# Ce sont DEUX choses differentes : si Star-Gaze est eteinte (identite en
# forme civile, capacite ignoree), ou si la carte jouee n'imprime aucune
# ressource, Star-Gaze ne resout pas et Alloy ne gagne rien.
#
# Carte de reference : `sr007` Great Power (pack spider_man_rainy) et `av006`
# Anti-Venom Goo, tous deux montes sur
# `AbilityFactory.AfterCardResolveAbility(...)`. Ici on emploie sa forme
# NOMMEE : `ability_name=NOM_STAR_GAZE` (resolve.py:137-141) compare
# `message.effect.ability.name` a la chaine posee par `.SetName()` sur
# ma001a. C'est le seul lien entre les deux cartes, et il est exact.
#
# `which_card=Hero` + `card_control_by="You"` + `trigger_player="You"` :
# la capacite ne repond qu'a la face heros du joueur qui controle Alloy.
#
# « Hero Response » -> `AbilityType.HeroResponse` (sous-type dedie,
# mot-piege du PROCESSUS-CARTE §5) : la reponse n'existe qu'en forme heros —
# ce qui est de toute facon la seule forme ou Star-Gaze peut resoudre.
#
# « until the end of the TURN » -> `GainUntilTurnEnd`
# (face_action.py:466-489), qui defait le bonus sur
# `Message.WhenPlayerTurnEnd`. PAS `GainUntilPhaseEnd` ni
# `GainUntilRoundEnd` : trois portees differentes, le texte en nomme une.
# Modele : `12009` Pym Particles.


BONUS_ATK = 1


def GetAbilities() -> Sequence['Ability']:

    def alloy(effect: 'Effect', message: 'Message.AfterEffectResolved') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)

        this.GainUntilTurnEnd(effect, attack=BONUS_ATK)

    return [
        AbilityFactory.AfterCardResolveAbility(
            AbilityType.HeroResponse,
            None,
            Hero,
            alloy,
            ability_name=NOM_STAR_GAZE,
            card_control_by="You",
            trigger_player="You",
        ),
    ]
