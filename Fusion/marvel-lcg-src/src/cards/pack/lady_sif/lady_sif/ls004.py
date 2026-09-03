from . import *

# Lead The Charge — evenement signature, x3 (n/15 = 4, 5 et 6).
# ATTACK. TACTIC. Cout 1, ressource [physical].
# Hero Action (attack): Lady Sif makes a basic attack without exhausting.
#   Choose another friendly character. That character gets +1 ATK until the
#   end of the round.
#
# Cartes de reference :
#  - `bw024` Strong as Silk (meme auteur, Rainy) : la SEULE autre carte du
#    depot qui imprime « makes a basic attack without exhausting ». Son
#    commentaire pose la regle qu'on reprend : `BasicAttack` resout l'attaque
#    de base sans rien incliner — c'est l'ACTION de base du joueur qui incline
#    d'ordinaire, pas l'attaque elle-meme ;
#  - `bw024` encore pour `face.GainUntilRoundEnd(effect, attack=1)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « LADY SIF makes a basic attack » : la face HEROS nommement, pas un allie
#    et pas « votre personnage ». En forme civile la carte ne se joue pas
#    (Hero Action), donc `initiator.GetHero()` est toujours elle.
#  - « without exhausting » : ne RIEN incliner. Ne pas ajouter de
#    `Faces.ExhaustAll` par symetrie avec les cartes qui, elles, inclinent.
#  - ⚠ Cette attaque de base declenche Valiant Warrior (ls001a) et Sif's Crest
#    (ls009) : 1 menace retiree et 1 carte piochee en prime. C'est le coeur du
#    pack, pas un effet de bord.
#  - « ANOTHER friendly character » : un AUTRE que Lady Sif — d'ou l'exclusion
#    explicite du heros dans le selecteur. Sans elle, la carte se donnerait
#    +1 ATQ a elle-meme, ce que le texte interdit.
#  - « until the end of the ROUND », pas de la phase.
#  - Le +1 ATQ arrive APRES l'attaque de base : il ne la renforce pas. L'ordre
#    imprime est respecte.
#  - Le libelle `(attack)` alimente Sonne.


def GetAbilities() -> Sequence['Ability']:

    def lead_the_charge(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        heros = initiator.GetHero()
        if heros is None:
            return

        heros.BasicAttack(effect.targets, effect)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "That character gets +1 ATK until the end of the round",
                lambda cibles: [face.GainUntilRoundEnd(effect, attack=1)
                                for face in cibles if face is not None],
            ).SetTarget("YouControlUnit", exclude=[heros]),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            lead_the_charge,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
