from . import *

# * Chilly McHotpants (titre d'origine « War Skrull ») — ALLIE de campagne ('Pool / Campaign, n° 268).
# Cout 0. SCH 2 (a la place du THW, ecrit THW 2 dans le desc) / ATK 2, 5 PV. SKRULL.
# *Treat this ally as a minion engaged with you.
# [star] Response: After "Chilly McHotpants" attacks you, draw 1 cards. If you take no damage from that
#   attack, draw 1 card.
#
# Cartes de reference :
#  - **`36038`** Possessed / **`sk098`** Impostor (`TreatAttachedCardAsMinion`) et **`sk243`**
#    (`TreatAsMinion(allie, gabarit, joueur, effect, process=...)`) : un allie echange sa FACE contre celle d'un
#    SBIRE engage avec le joueur ; SCH = THW imprime ; quand le sbire quitte le jeu l'allie revient dans la
#    defausse de son proprietaire (`Card.CheckIfCanDiscard` remet la face imprimee).
#  - Ici le TEXTE de la carte reste actif (contrairement a Possessed : « blank text box ») : le gabarit
#    `skrull_war_minion` (voir ce dossier) porte la Reponse ; `TreatAsMinion` ajoute les capacites du gabarit
#    (« Hack for 50171 »).
#
# ⚠ Mots-pieges :
#  - « Treat this ally AS A MINION ENGAGED WITH YOU » : des l'entree en jeu ; le sbire s'engage avec le
#    controleur de l'allie ; ni limite d'allies ni capacite d'allie pendant qu'il est sbire ;
#  - nom, sous-titre, image, ATQ et MNG sont repris de la carte (`process`) ; MNG = THW imprime.


def GetAbilities() -> Sequence['Ability']:

    def reprendre_l_allie(minion: 'Any', allie: 'Any', effect: 'Effect') -> None:
        Unused(effect)
        minion.SetName(allie.printed_name)
        minion.SetSubtitle(allie.printed_subtitle)

    def devenir_sbire(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        joueur = this.GetControlByPlayer()
        TreatAsMinion(this, GABARIT_SBIRE_WAR_SKRULL, joueur, effect, process=reprendre_l_allie)

    return [
        # Un SBIRE n'est pas un allie : tant qu'il entre en jeu sous sa face d'allie, il ne doit pas faire depasser
        # la limite d'allies (sinon le joueur defausserait un allie pour une carte qui n'en sera plus un).
        *AbilityFactory.ThisNotCountAllyLimit(),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.NonKeyword,
            "This",
            devenir_sbire,
        ),
    ]
