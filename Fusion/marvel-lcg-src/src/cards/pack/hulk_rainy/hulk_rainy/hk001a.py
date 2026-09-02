from . import *

# * Hulk (face heros) — AVENGER. GAMMA.
# THW 0 / ATK 2 / DEF 3 — HS 4 / PV 15
# Anger — Response: After Hulk takes damage, deal 1 damage to an enemy.
#
# Cartes de reference :
#  - `aa001a` * Agatha Harkness (« Power Absorption »), meme declencheur
#    exact `AfterUnitTookDamage(Response, "You", op)` sur une FACE HEROS ;
#  - `08013` Stealth Strike pour le choix de la cible par
#    `ChooseAbilities` + `ForChoiceAbility(...).SetTarget(Enemy)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « After HULK takes damage » : le declencheur est l'identite, pas un
#    allie ni une amelioration. `who_took_damage="You"` — et `GetYouRule`
#    l'etend a l'IDENTITE (`identity=True`), donc la capacite existe sur la
#    face heros seule, ce qui suffit : la carte est la face heros.
#  - **AUCUN filtre `is_from_attack`.** Le texte dit « takes damage », pas
#    « takes damage from an attack ». Un degat de traitrise, un degat
#    indirect ou le degat que Hulk s'inflige lui-meme avec hk006 Reckless
#    Charge declenchent donc Anger. C'est l'ecart avec hk010 Intimidating
#    Roar, qui imprime « from an attack » et le filtre.
#  - « deal 1 damage TO AN ENEMY » : n'importe quel ennemi au choix, pas
#    forcement celui qui a frappe. Rien dans le texte ne dit « that enemy ».
#  - Le degat rendu n'est PAS une attaque : ni overkill, ni piercing, ni
#    riposte adverse.
#
# ⚠ Boucle impossible : les 1 degat rendus ne visent jamais Hulk lui-meme
# (`SetTarget(Enemy)`), la Response ne peut donc pas se rappeler elle-meme.


def GetAbilities() -> Sequence['Ability']:

    def anger(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Hero)
        Unused(message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal 1 damage to an enemy",
                lambda cibles: this.DealDamage(cibles, 1, effect),
            ).SetTarget(Enemy),
        )

    return [
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.Response,
            "You",
            anger,
        ).SetName("Anger"),
    ]
