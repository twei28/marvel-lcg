from . import *

# Portal (x5) — AMELIORATION, cout 0, [mental]. PORTAL.
# Hero form only. Attach to an enemy or a scheme.
# Interrupt: When attached enemy or scheme would be a target of an [[ATTACK]]
#   or [[THWART]] event, reduce that event's resource cost by 2. Discard this
#   card after that event resolves.
#
# LA CARTE QUI PORTE TOUT LE PACK. Cinq exemplaires, six cartes la lisent, les
# deux faces de l'identite la recyclent.
#
# CARTES DE REFERENCE
#  - `yd012` Yaka Arrow (pack yondu) : meme famille — une amelioration qui
#    s'attache a un ENNEMI et que tout le kit deplace.
#  - `hercules/59009` pour `WhenCalculateEffectCost` + `UpdateCost`.
#
# TEXTE CONTRE CODE
#  « an enemy OR a scheme » -> `Enemy | Scheme2` : les deux, ce qui distingue
#    ce portail de la Yaka Arrow (ennemis seuls).
#  « an [[ATTACK]] or [[THWART]] EVENT » -> le TRAIT imprime de l'evenement,
#    pas son libelle d'action : une attaque de base ne reduit rien.
#  « would be A TARGET OF » -> `ReduceCostToPlayFaceWhen` + `message.for_targets`,
#    modele `09039` * Iron Man: Tony Stark. ⚠ UNE PREMIERE VERSION lisait
#    `check_effect.targets` depuis un `WhenCalculateEffectCost` nu : les cibles
#    ne sont PAS encore choisies a ce moment-la, la condition etait donc
#    toujours fausse et la reduction ne tombait JAMAIS. Journal : « (Hero
#    Action,Play,attack) [bk005] WhenPlayerInTurn failed » — cout impayable.
#
# ⚠ LE TIMING DE LA DEFAUSSE N'EST PAS COSMETIQUE, et une premiere version
# s'est trompee. « Discard this card AFTER that event RESOLVES » : si l'on
# defausse des la reduction de cout, le portail n'est PLUS LA a la resolution
# — et `bk005` Lose Footing, qui compte « 2 degats supplementaires par PORTAL
# attache a la cible », infligerait 4 au lieu de 6. Deux cartes du pack
# (bk005, bk006) lisent le portail PENDANT l'evenement qu'il finance.
#
# La defausse est donc reportee : on enregistre une capacite TEMPORAIRE sur
# `AfterPlayerPlayedCard`, qui retire le portail une fois l'evenement resolu.
# Constate en concevant le cas de test, avant meme de l'executer.


def GetAbilities() -> Sequence['Ability']:

    def est_attack_ou_thwart(face: 'CardFace|None') -> bool:
        """Un evenement ATTACK ou THWART, les deux seuls mots du texte."""
        return (face is not None and Event.IsType(face)
                and (face.HasTrait("ATTACK") or face.HasTrait("THWART")))

    def vise_mon_hote(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        """L'evenement dont on calcule le cout vise-t-il l'hote de CE portail ?

        ⚠ `message.for_targets` EST LE SEUL CHAMP QUI DIT LES CIBLES ICI.
        `WhenCalculateEffectCost` (sender_player.py:234) n'expose que
        `check_effect`, `for_targets`, `is_play` et `cost` : ni `for_face`, ni
        `for_effect`. Deux versions successives ont interroge des champs
        inexistants, `getattr` rendait None, la condition etait TOUJOURS
        FAUSSE et la reduction ne tombait jamais — le journal ne disait rien
        d'autre que « WhenPlayerInTurn failed », c'est-a-dire cout impayable.
        """
        Unused(effect)
        hote = Hote(effect.this)
        if hote is None:
            return False
        return hote in list(message.for_targets or [])

    def a_vise_mon_hote(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> bool:
        """Meme question, mais APRES coup : autre message, autres champs.

        ⚠ `AfterPlayerPlayedCard` n'a pas `for_targets` : les cibles vivent
        sur `message.play_effect.targets`, et la carte jouee sur
        `message.played_face`.
        """
        hote = Hote(effect.this)
        if hote is None or not est_attack_ou_thwart(getattr(message, "played_face", None)):
            return False
        cibles = list(getattr(message.play_effect, "targets", []) or [])
        return hote in cibles

    def defausser_apres_resolution(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        """« Discard this card AFTER that event RESOLVES. »

        ⚠ LE TIMING N'EST PAS COSMETIQUE : bk005 et bk006 comptent les portails
        attaches a leur cible PENDANT leur resolution. Defausser des le calcul
        du cout ferait perdre 2 degats a Lose Footing, c'est-a-dire la moitie
        du kit.
        """
        Unused(message)
        Faces.DiscardAll([effect.this], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(card_type=Enemy | Scheme2),
        ),
        # ⚠ `which_player="AnyPlayer"` ET NON `"You"` : `"You"` passe par
        # `Select.GetYou(effect)`, or `effect.this` est ici une amelioration
        # attachee a un ENNEMI. Modele `09039` * Iron Man: Tony Stark, seule
        # autre carte du depot qui reduit le cout « quand cette carte-ci est
        # la cible ». Le filtre par cible suffit a borner l'effet.
        AbilityFactory.ReduceCostToPlayFaceWhen(
            Event,
            2,
            "AnyPlayer",
            conditions=[vise_mon_hote],
        ),
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Rule,
            "AnyPlayer",
            Event,
            defausser_apres_resolution,
            conditions=[a_vise_mon_hote],
        ),
    ]
