from . import *

# Skrull Energy Gun — ATTACHEMENT (Skrull Elite - Jazinda). WEAPON. +1 ATQ, 1 icone de boost.
# Attach to a SKRULL minion. If you cannot, attach to the villain.
# While attached to a SKRULL enemy, attached enemy's attacks gain overkill, piercing, and ranged.
# Hero Action: Spend a [physical] resource → attach this card to another enemy.
#
# Cartes de reference :
#  - Attache : helper `AttacherAUnSbireSkrull` (modele 01100 / sk146).
#  - « attacks gain overkill, piercing, and ranged » : **`27152`** Tracking Display / **`ls015`**
#    (`UnitAttackGainKeyword(attaquant, overkill=True, piercing=True, ranged=True)`), attaquant
#    `"AttachedEnemy"`, avec la condition « SKRULL » sur l'hote.
#  - « Hero Action: Spend ... → <effet> » : **`sk086`** Incite Rebellion (`WhenInYourPlayTurn(HeroAction, op)
#    .SetCost(...)`) ; deplacement : `AttachTo2` ; la cible est choisie DANS l'effet (`AskChooseFace`), pas par
#    `SetTarget` (voir le commentaire de `deplacer`).
#  - +1 ATQ : natif (`ATK+`).
#
# ⚠ Mots-pieges : « WHILE attached to a SKRULL enemy » (les trois mots-cles ne vivent que sur un hote
# SKRULL : sur un hote non-Skrull, apres deplacement, il ne reste que le +1 ATQ) ; « ANOTHER enemy »
# (un ennemi different de l'hote actuel : sbire ou mechant, Skrull ou non) ; « a [physical] resource » :
# UNE ressource physique (Cost("R")) ; « attached enemy's ATTACKS » : toutes ses attaques ; l'action est
# une Action de heros (le joueur la declenche pendant son tour).


def GetAbilities() -> Sequence['Ability']:

    def hote_skrull(effect: 'Effect', message: 'Message2') -> bool:
        hote = effect.this.GetBindFace()
        return hote is not None and hote.HasTrait("SKRULL")

    def autres_ennemis(effect: 'Effect') -> List['CardFace']:
        hote = effect.this.GetBindFace()
        return [f for f in Worlds.GetOnFieldCards(effect)
                if Enemy.IsType(f) and f.IsInPlay() and f != hote]

    def un_autre_ennemi_existe(effect: 'Effect', message: 'Message2') -> bool:
        Unused(message)
        return bool(autres_ennemis(effect))

    def deplacer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        this = effect.this.CastTo(Attachment)
        cibles = autres_ennemis(effect)
        if not cibles:
            return
        # Le choix de la cible se fait DANS l'effet (apres le cout), pas par `SetTarget` : une cible obligatoire
        # declaree sur l'action la rendait « forcee » pour le pilote de l'autoplay, qui la rejouait sans fin quand
        # la ressource manquait (journal autoplay du 15/10/2026, graine 2 : partie « bloquee »).
        cible = cibles[0] if len(cibles) == 1 else effect.GetInitiator().AskChooseFace(cibles, effect)
        if cible is not None:
            this.AttachTo2(cible, effect)

    return [
        AttacherAUnSbireSkrull(),
        AbilityFactory.UnitAttackGainKeyword(
            "AttachedEnemy", overkill=True, piercing=True, ranged=True,
            conditions=[hote_skrull],
        ),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, deplacer, conditions=[un_autre_ennemi_existe])
        .SetCost(Cost("R")),
    ]
