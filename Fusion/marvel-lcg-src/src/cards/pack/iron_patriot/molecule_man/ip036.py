from . import *

# * Master of Molecules — ATTACHEMENT du set MOLECULE MAN (3/6). Boost 3. TITLE.
# Attach to Molecule Man. If you cannot, this card gains surge.
# [star] Forced Interrupt: When Molecule Man attacks you, discard 1 card at
#   random from your hand. If that card's printed resource has:
#   [energy]   – This attack gains overkill and piercing.
#   [mental]   – Stun and confuse the attacked character.
#   [physical] – This attack deals 2 addtional damage.
#   [wild]     – Discard 1 additional card.
#
# ⚠ « addtional » est LA COQUILLE IMPRIMEE de l'auteur. Elle reste dans le
# texte de la carte, pas dans le code.
#
# CARTES DE REFERENCE
#  - `01099` Charge (attachement de Rhino) : le calque exact —
#    `AttachToFaceWhenPutIntoPlay(CardFinder(name=...))` +
#    `WhenUnitWouldAttack(ForcedInterrupt, CardFinder(name=...), op)` +
#    `message.GainOverKill(effect)`.
#  - `41028` Psionic Illusion : `FacesCounter.GetPrintedResources([face])` et
#    `HasColorPrinted`, sur une carte defaussee au hasard.
#  - `01122` Klaw's Vengeance : `player.DiscardRandomHandCards(1, effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « If you cannot, this card GAINS SURGE » : Molecule Man absent, la carte
#    ne s'attache pas et enchaine. `AttachToFaceWhenPutIntoPlay` sait le faire
#    par `if_cannot_gain_surge=True`.
#  ⚠⚠ LES QUATRE LIGNES NE SONT PAS EXCLUSIVES. Une carte [wild] n'a qu'une
#    icone, mais rien n'interdit a une carte d'en porter deux (aucune du jeu ne
#    le fait aujourd'hui). On teste donc les quatre, on n'en choisit pas une.
#  ⚠ « discard 1 card AT RANDOM » : au hasard, pas au choix du joueur.
#  ⚠ « Discard 1 ADDITIONAL card » sur [wild] : une carte de plus, defaussee au
#    hasard elle aussi. Elle ne redeclenche PAS le tableau — le texte parle de
#    « that card », au singulier, celle de la premiere defausse.
#  ⚠ « the ATTACKED character » ([mental]) : la cible de l'attaque, connue
#    seulement une fois le defenseur declare. On la lit sur le message a la
#    resolution, pas a l'interruption.
#  ⚠ Main vide : rien n'est defausse, aucune ligne ne s'applique, l'attaque
#    suit son cours.


def GetAbilities() -> Sequence['Ability']:

    def maitre_des_molecules(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(this)
        # ⚠ `message.against_player`, PAS `GetToPlayer()` :
        # `Message.WhenUnitWouldAttack` n'a pas cette methode
        # (sender_damage.py:310, elle y est meme commentee avec un `assert
        # False`). Le joueur vise se lit sur la propriete d'attaque. Mesure du
        # 10/09/2026 : `AttributeError` en pleine interruption, donc AVANT que
        # la moitie « selon la couleur defaussee » ne s'applique.
        joueur = message.against_player
        if joueur is None:
            return

        defaussees = joueur.DiscardRandomHandCards(1, effect)
        if not defaussees:
            return
        couleurs = FacesCounter.GetPrintedResources(defaussees)

        if couleurs.HasColorPrinted("Y"):
            message.GainOverKill(effect)
            message.GainPiercing(effect)
        if couleurs.HasColorPrinted("R"):
            message.GainATKForThisAttack(2, effect)
        if couleurs.HasColorPrinted("G"):
            joueur.DiscardRandomHandCards(1, effect)
        if couleurs.HasColorPrinted("B"):
            def frapper_les_esprits(cible: 'CardFace') -> None:
                Faces.GiveStatus([cible], "Stunned", effect)
                Faces.GiveStatus([cible], "Confused", effect)
            message.IfThisAttackDealDamage(frapper_les_esprits, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(name="Molecule Man"),
            if_cannot_gain_surge=True,
        ),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            CardFinder(name="Molecule Man"),
            maitre_des_molecules,
        ),
    ]
