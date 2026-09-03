from . import *

# Energy Shield — amelioration signature, x1 (n/15 = 10).
# TECH. Cout 2, ressource [energy].
# Iron Man gets +1 DEF.
# Hero Interrupt: When Iron Man would take any amount of damage, remove 1
#   reactor counter from him -> prevent up to 2 of that damage.
#
# Cartes de reference :
#  - `03009` / `ls010` pour `GiveKeywordToAttached(Hero, defense=1)` ;
#  - **`si016` * Tony Stark A.I.** (pack superior_iron_man, mot-cle maison
#    « Armored 2 ») et `01098` Armored Rhino Suit :
#    `WhenUnitWouldTakeDamage(..., op)` + `message.PreventDamage(2, effect)`.
#    ⚠ Coincidence utile : si016 est un sbire nemesis dont le `desc.Nemesis`
#    vaut « Tony Stark ». Meme personnage source, meme mecanique.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « IRON MAN gets +1 DEF » : un nom PROPRE, celui de la seule face HEROS
#    (l'alter-ego s'appelle Tony Stark). D'ou `Hero` et non `"You"`, qui
#    donnerait le bonus a une face civile qui n'a pas de DEF (piege an002).
#  - « **any amount** of damage » : toute instance, pas seulement une attaque.
#    Un degat de traitrise, un degat indirect, un degat que le heros
#    s'inflige : tous ouvrent la fenetre.
#  - « remove 1 reactor counter from him **->** » : la fleche en fait un COUT.
#    Sans compteur, aucune prevention — d'ou le RETOUR de
#    `RetirerUnReacteur`, jamais une supposition.
#  - « prevent **up to** 2 » : 2 au plus. `PreventDamage(2, ...)` plafonne
#    deja, une instance de 1 degat ne gaspille pas le compteur au-dela.
#  - `Hero Interrupt` : rien en forme civile, alors meme que le compteur, lui,
#    se pose en forme civile par im006.
#
# ⚠ LE RETRAIT DU COMPTEUR EST DANS LE COUT, PAS DANS LE CORPS, ET C'EST UN
# CORRECTIF PAYE EN AUTOPLAY (03/09/2026). Ecrit `if RetirerUnReacteur(...):`
# dans le corps, la capacite RESOUT quand meme quand le reacteur est vide :
# elle ne fait rien, le moteur la repropose a l'identique, et la partie tourne
# en rond. Mesure : 1 partie bloquee sur 32, verdict « meme question posee a
# l'identique et le plateau n'a pas bouge ». Dans le COUT
# (`CoutDuReacteur`, helper du set), le False empeche le paiement et l'option
# n'est pas offerte. Meme defaut que le blocage Underling du 20/08.



def GetAbilities() -> Sequence['Ability']:

    def energy_shield(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        # Le compteur a deja ete retire par le COUT : ici, on previent.
        message.PreventDamage(2, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            Hero,
            defense=1,
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            energy_shield,
        ).SetCostFunc(CostFunc.Custom(None, CoutDuReacteur)),
    ]
