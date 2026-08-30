from . import *

# MGH Drug — ATTACHEMENT nemesis, custom « CptScorp »
# `ATK+ "1"`, `Boost "0"` + une capacite de bonus etoilee, aucun trait.
#
# Attach to Mr. Hyde, if able. If you cannot, attach to the villain.
# [star] Attached enemy's attacks gain overkill.
# Hero Action: Spend [mental][energy] resources -> discard this card.
# ---
# [star] Boost: Reveal this card.
#
# ---------------------------------------------------------------------------
# ⚠ LA CLE DE DONNEES EST `ATK+`, JAMAIS `ATK`
#
# « +1 ATQ » sur un attachement est un BONUS donne a la carte PORTEUSE, pas
# une valeur d'attaque propre : `ATK` ferait de l'attachement une carte a 1
# d'ATQ, ce qui n'a aucun sens. La cle est lue nativement
# (`HasModify.RegisterAttribute("ATK+", "modify_atk")`,
# attribute/has_modify.py:22) et reversee au porteur par un
# `GiveKeywordToAttached` que le moteur construit tout seul
# (has_modify.py:33-38). RIEN a coder ici. Modele : `sd021` Magic Chains,
# meme structure dans le pack frere.
#
# `Boost "0"` : ZERO icone de bonus imprimee, mais une capacite `[star]
# Boost` (voir plus bas). Modele `wd005`.
#
# ---------------------------------------------------------------------------
# L'ATTACHE CONDITIONNELLE
#
# « Attach to Mr. Hyde, IF ABLE. IF YOU CANNOT, attach to the villain. » ->
# `AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name=NOM_MR_HYDE),
# if_cannot_attach_to=Villain)`. Modeles exacts : `04029` Crossfire's Rifle
# et `04064` Crossbones' Machine Gun, qui impriment la meme tournure.
# `sd021` Magic Chains emploie la meme construction dans le pack frere.
#
# La recherche par nom est sans danger : « Mr. Hyde » est une chaine unique
# du catalogue (l'officielle `24035` s'appelle « Mister Hyde », chaine
# DIFFERENTE), et elle appartient a ce set nemesis. Le nom est ecrit SANS
# l'etoile d'unicite (`cards/paper.py:45-46`).
#
# ---------------------------------------------------------------------------
# « [star] ATTACHED ENEMY'S ATTACKS GAIN OVERKILL »
#
# Capacite de stat etoilee, permanente tant que la carte est en jeu ->
# `AbilityFactory.UnitAttackGainKeyword("AttachedEnemy", overkill=True)`
# (factory/do_attack.py:828-877). Modele : `57007` Superhuman Strength, qui
# ecrit `UnitAttackGainKeyword('AttachedCharacter', overkill=True)`.
#
# `"AttachedEnemy"` plutot que `"AttachedCharacter"` : le texte dit
# « attached ENEMY », et la carte peut atterrir sur le vilain comme sur le
# sbire. La cible-chaine est resolue par `check_attached() and
# Enemy.IsType(face)` (condition/card_type.py:180-181).
#
# ⚠ Le mot-cle est donne aux ATTAQUES du porteur, pas au porteur : la
# fabrique ecoute `Message.CheckIfAttackMessageHasKeyword`, recalcule a
# chaque attaque. Un attachement retire rend donc son overkill aussitot.
#
# ---------------------------------------------------------------------------
# LA HERO ACTION : LA FLECHE EST UN COUT -> UN EFFET
#
# « Hero Action: Spend [mental][energy] resources -> discard this card. »
#
# ⚠ COUT RELEVE PAR DECOUPE D'IMAGE, PAS A VUE : UNE icone mentale et UNE
# icone energie. Dans le vocabulaire du moteur (element/cost.py:29-46),
# B = [mental], Y = [energy], R = [physical], G = [wild] : le cout s'ecrit
# donc `Cost("YB")`.
#
# Modele exact : `04073` Energy Shield (pack trors), qui imprime
# « Hero Action: Spend [energy][mental] resources -> discard this card » et
# s'ecrit `AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction)
# .SetCost(Cost("YB"))`. `04072` Laser Rifle fait de meme avec `Cost("YR")`.
#
# `.SetCost` et non `.SetCostFunc` : un cout en RESSOURCES se declare par
# `SetCost` (ability.py:320), `SetCostFunc` etant reserve aux couts d'action
# (incliner, defausser, subir...). Le moteur ne propose pas l'action quand le
# joueur ne peut pas reunir les deux icones : cout impayable = rien ne se
# passe.
#
# ---------------------------------------------------------------------------
# « [star] BOOST: REVEAL THIS CARD »
#
# `AbilityFactory.WhenCardBecomeBoost("This", RevealThisCard)` : l'idiome
# unique du depot (modeles `16140` Sound the Alarms, `56144` Cap's Helmet,
# `57007`, `56145`). `RevealThisCard` est l'aide partagee de
# `cards/pack/__init__.py:120`.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(name=NOM_MR_HYDE),
            if_cannot_attach_to=Villain,
        ),
        AbilityFactory.UnitAttackGainKeyword(
            "AttachedEnemy",
            overkill=True,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCost(Cost("YB")),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            RevealThisCard,
        ),
    ]
