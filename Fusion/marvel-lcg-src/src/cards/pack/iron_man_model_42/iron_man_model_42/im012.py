from . import *

# * Hulkbuster Armor — amelioration signature, n/15 = 14b.
# ARMOR. TECH. Cout 2, ressource [physical].
# Iron Man gets -1 hand size, +1 ATK and DEF and his basic attacks gain
#   overkill.
# Interrupt: When Iron Man would take any amount of damage, remove this card
#   from the game -> prevent all of that damage.
#
# ⚠ CARTE ALTERNATIVE. L'auteur la donne comme « alternative replacement for
# Save The Day » et les deux portent le numero imprime 14/15 : ce n'est PAS un
# cumul, c'est un choix de deckbuilding. Decision de l'utilisateur
# (03/09/2026) : les DEUX cartes existent avec deux card_id distincts, et
# c'est `im011` Save The Day qui part dans le deck de depart livre. Celle-ci
# reste disponible dans le deck-builder.
#
# Cartes de reference :
#  - `05023` / `hk011` pour `GiveKeywordToAttached` ;
#  - `ls011` Sif's Sword (pack precedent) pour
#    `UnitAttackGainKeyword(..., is_basic_attack=True)` ;
#  - `si016` / `01098` pour `PreventDamage`, ici en version « All » ;
#  - `32177` Swagger pour `Faces.RemoveAllFromGame`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - **« -1 hand size »** est un MALUS, et il est reel : le heros passe de 5 a
#    4 cartes. Sur un personnage qui vit de sa main pour charger son reacteur
#    (im001a exige des cartes energie IMPRIMEES), c'est le vrai prix de la
#    carte.
#  - « IRON MAN gets ... » : un nom PROPRE, la face HEROS seule (l'alter-ego
#    s'appelle Tony Stark). D'ou `Hero` et non `"You"` — piege an002.
#  - « his **BASIC** attacks gain overkill » : `is_basic_attack=True`, sinon
#    im002 Repulsor Barrage en profiterait aussi.
#  - **`Interrupt` NU, pas `Hero Interrupt`** : contrairement a im007 Energy
#    Shield, la prevention marche dans les DEUX formes. Le mot compte.
#  - « remove this card **from the game** » : pas une defausse. La carte ne
#    revient jamais, contrairement a `im011` qui, elle, va au cimetiere.
#  - « prevent **ALL** of that damage » : `PreventDamage("All", ...)`, une
#    seule fois dans la partie. C'est un filet unique, pas un mur.


def GetAbilities() -> Sequence['Ability']:

    def hulkbuster(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Upgrade)

        Faces.RemoveAllFromGame([this], effect)
        message.PreventDamage("All", effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            Hero,
            hand_size=-1,
            attack=1,
            defense=1,
        ),
        AbilityFactory.UnitAttackGainKeyword(
            "You",
            overkill=True,
            is_basic_attack=True,
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt,
            "You",
            hulkbuster,
        ),
    ]
