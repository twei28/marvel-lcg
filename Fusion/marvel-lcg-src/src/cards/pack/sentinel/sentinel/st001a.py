from . import *

# * Sentinel — FACE HEROS. ANDROID. GIANT. CTR 2 / ATQ 1 / DEF 2, main 4, 14 PV.
# Ablative Protocol — Interrupt: When you would take any amount of damage,
#   destroy a [[COMPONENT]] upgrade instead. (See insert.)
#
# Cartes de reference :
#  - `49006` Magnetic Bubble : le SEUL montage qui remplace integralement des
#    degats, `message.SetBeInstead(effect)` dans un `WhenUnitWouldTakeDamage`.
#    `08032` Defensive Stance et `31019` Forcefield Generator, eux, PREVIENNENT
#    une partie des degats (`PreventDamage`) : ce n'est pas ce que dit la
#    carte, qui remplace TOUT (« any amount »).
#  - `nt003a` pour la mecanique de plateau des Component.
#
# ⚠ MOT-CLE MAISON DESTROY, fiche docs/reference/mots-cles/destroy.md lue avant
# d'ecrire une ligne. Tout passe par `Detruire()` : 2 degats imblocables puis
# retournement de la carte.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **instead** » : les degats d'origine disparaissent ENTIEREMENT, quelle
#    que soit leur quantite. D'ou `SetBeInstead`, pas `PreventDamage(n)`.
#  - « destroy **a** COMPONENT upgrade » : UN seul, au choix du joueur, et
#    seulement un Component encore INTACT — un Component deja detruit ne peut
#    pas l'etre (insert du pack). Le selecteur porte donc `trait="INTACT"`, ce
#    qui a un second effet, indispensable : sans Component intact, la capacite
#    n'a plus de cible legale et ne se declenche plus.
#  - **LA BOUCLE, ET CE QUI LA COUPE.** Les 2 degats de la destruction sont, eux
#    aussi, des degats que « vous alliez subir » : sans garde-fou l'interruption
#    se represente, et le robot se demonte ENTIEREMENT sur une seule attaque a 2
#    (mesure du 12/09/2026, cas st015 : quatre pieces retournees). Ce n'est pas
#    ce que dit le mot-cle : l'insert ecrit « 2 **unpreventable** damage », et
#    remplacer des degats EST une prevention. Le moteur ne savait pas le dire —
#    `DamageProperty.unpreventable` a donc ete AJOUTE (fiche destroy.md). La
#    condition ci-dessous n'est que la moitie visible du correctif : elle evite
#    de PROPOSER une interruption que le moteur refuserait ensuite.
#  - « Interrupt » NUE, pas « Hero Interrupt » : mais la capacite est imprimee
#    sur la face HEROS, elle ne vit donc qu'en forme heroique de toute facon.


def GetAbilities() -> Sequence['Ability']:

    def protocole_ablatif(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)

        message.SetBeInstead(effect)
        Detruire(effect.targets, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt,
            "You",
            protocole_ablatif,
            conditions=[
                lambda effect, message: not message.IsUnpreventable()
            ],
        ).SetName("Ablative Protocol")
        .SetTarget(
            Upgrade,
            trait=TRAIT_INTACT,
            from_where=["YouControlCards"],
        ),
    ]
