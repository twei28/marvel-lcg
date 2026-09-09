from . import *

# Agility — EVENEMENT, cout 0 [energy]. DEFENSE. SUPERPOWER.
# Hero Interrupt (defense): When you would take any amount of damage, prevent 3
#   of that damage (prevent all of that damage instead if you have the AERIAL
#   trait).
#
# CARTES DE REFERENCE
#  - `50159`, `16098`, `21117` : `WhenUnitWouldTakeDamage` +
#    `message.ReduceDamage(n, effect)`, la brique de toute prevention.
#
# TEXTE CONTRE CODE
#  ⚠ « ANY AMOUNT of damage » : pas seulement les attaques. Les degats
#    indirects d'une traitrise comptent aussi — donc PAS de `is_from_attack`.
#  ⚠ « PREVENT ALL of that damage INSTEAD if you have the AERIAL trait » :
#    « instead » remplace les 3, il ne s'y ajoute pas. Et le trait se lit sur
#    l'IDENTITE au moment ou les degats tombent : `su011` Web-Shooters le donne,
#    donc la valeur change en cours de partie et ne peut pas etre figee.
#  ⚠ « Hero Interrupt (DEFENSE) » : le libelle est imprime, donc
#    `SetLabel('defense')` — la carte devient injouable sous un statut Sonne.
#  ⚠ Cout 0 : la carte reste payante en ACTION (elle occupe le tour), c'est
#    voulu.
#  ⚠ Aucune limite imprimee : etape 7 bis sans objet.


def GetAbilities() -> Sequence['Ability']:

    def esquiver(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        identite = IdentiteDuJoueur(effect)
        porte_aerial = bool(identite is not None and identite.HasTrait(TRAIT_AERIAL))
        message.ReduceDamage(999 if porte_aerial else 3, effect)

    return [
        # ⚠⚠ LA CARTE SE BRANCHE SUR LES DEGATS, PAS SUR LE TOUR DE JEU.
        # Premiere ecriture (08/09/2026) : `WhenInYourPlayTurn(HeroInterrupt,
        # ...).SetPlay().SetLabel('defense')`. Elle passait `test_cards`, les
        # gates statiques ET le montage du deck — mais l'AUTOPLAY a rendu
        # **26 AssertionError** en 8 parties, toutes dans
        # `can_defense.py:138` (`SpecialDefense`, `assert False`) : le moteur
        # route un evenement libelle « defense » vers un chemin qui attend un
        # message d'attaque, et `WhenPlayerInTurn` n'en est pas un.
        # C'est l'etape 8 de PROCESSUS-CARTE qui l'a vue, et elle SEULE.
        # Le bon montage est celui des cartes de prevention (`50159`, `16098`,
        # `21117`) : `WhenUnitWouldTakeDamage` + `.SetPlay()` pour que la carte
        # se joue depuis la main dans la fenetre d'interruption.
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            esquiver,
        ).SetPlay(),
    ]
