from . import *

# * The Mancave — soutien signature, x1 (n/16 = 12). LOCATION.
# Cout 2, ressource [wild].
# Alter-Ego Response: After you change form, heal 1 damage from your identity.
# Hero Response: After you change form, reduce the resource cost of the next
#   [[SKILL]] card you play this turn by 1.
#
# ⚠ NOM : « The **Mancave** », en UN SEUL MOT, alors que le fichier du zip
# s'appelle `SUPPORT - The Man Cave.png`. Dans ce pack les noms de fichiers ne
# sont pas les noms de cartes (voir aussi nt011).
#
# Cartes de reference :
#  - **`01019a`** / `12001a` / `bt001b` pour `AfterUnitChangeForm(type, "You",
#    op)` — ici SANS `to_form`, voir les mots-pieges.
#  - `42018` * Angel's Aerie pour `this.HealthUnits(cibles, 1, effect)` et le
#    filtre `canbe_heal=True`.
#  - **`im001b`** * Tony Stark (pack iron_man_model_42) pour
#    `Worlds.UpdateNextCardPlayCost(joueur, -1, effect, finder=..., in_this=
#    'Turn')`, modele `16024` Deft Focus.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « After you **change form** » tout court, dans les DEUX capacites : PAS
#    « change to hero form ». C'est la difference exacte avec `nt004` Drop In.
#    Aucun `to_form` ici — mais chaque capacite est de toute facon filtree par
#    son propre type (`AlterEgoResponse` / `HeroResponse`), donc c'est bien la
#    forme d'ARRIVEE qui decide laquelle des deux se propose.
#  - « heal 1 damage from **your identity** » : l'identite, pas un personnage
#    au choix, pas un allie.
#  - « the **next** SKILL card you play **this turn** » : UNE carte, la
#    prochaine, et la fenetre se ferme a la fin du TOUR. `in_this='Turn'`, pas
#    `'Phase'`.
#  - « **[[SKILL]]** card » : le trait, pas le type — un allie ou une
#    amelioration SKILL comptent aussi. Le `finder` porte donc sur le trait.
#  - Aucun cout d'inclinaison imprime : le soutien N'EST PAS incline par ces
#    capacites. Ne pas ajouter de `CostFunc.Exhaust`, ce serait affaiblir la
#    carte — les deux Reponses sont gratuites et se declenchent a chaque
#    bascule.


def GetAbilities() -> Sequence['Ability']:

    def soin_en_civil(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)

        this.HealthUnits(effect.targets, 1, effect)

    def remise_en_heros(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        Worlds.UpdateNextCardPlayCost(
            joueur, -1, effect,
            finder=CardFinder(trait="SKILL"),
            in_this='Turn',
        )

    return [
        AbilityFactory.CanPlayThisSupportCard(),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.AlterEgoResponse,
            "You",
            soin_en_civil,
        ).SetTarget("YourIdentity", canbe_heal=True),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.HeroResponse,
            "You",
            remise_en_heros,
        ),
    ]
