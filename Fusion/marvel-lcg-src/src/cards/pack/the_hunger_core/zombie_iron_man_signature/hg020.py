from . import *

# Patched Armor — ATTACHMENT (set signature Zombie Iron Man, carte 2/5). Traits TECH, UPGRADE.
# Attach to Zombie Iron Man.
# Zombie Iron Man gets +2* hit points.
# Hero Action: Spend 3 resources -> discard this card.
#
# Carte de reference :
#  - Structure IDENTIQUE a `01119` Solid-Sound Body (pack core, Klaw) : « Attach to <nom du vilain>. <vilain>
#    gagne/gets <bonus>. Hero Action: Spend N resources -> discard this card. » -> 3 memes fabriques :
#    `AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name="..."))`,
#    `AbilityFactory.GiveKeywordToAttached(CardFinder(name="..."), <bonus>=N)`,
#    `AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction).SetCost(Cost(...))`. Seul le bonus
#    change (retaliate 1 chez Klaw -> +2* PV ici) et le cout (`YBR`, trois icones distinctes, chez Klaw ->
#    montant generique ici, cf. mots-pieges).
#  - Bonus de PV « N* » (scalant avec le nombre de heros) : meme litteral que `21136a` Hela (`health="2*"`,
#    pack mts) et `21137a` (`health="3*"`). `GiveKeywordToAttached` -> `GiveKeywordToAttachWhenApplyThisInternal`
#    (asset.py:13 et asset_helper.py:28 declarent explicitement `Literal["2*","3*","6*"]`) -> `face.Gain`
#    (face_gain.py:160-162) qui route une chaine vers `Worlds.ConvertPerPlayerIconToInt`. C'est le MEME
#    mecanisme que celui qui rend l'etoile sur les PV IMPRIMES des Metazombies (`FormatPlayerNumValue`,
#    has_attribute.py:17-21) : cf. `hg008` Zombie Iron Man, PV imprimes « 11* » (commentaire « PV 11[per_hero] »
#    dans son propre script).
#
# ⚠ Mots-pieges :
#  - « Attach to Zombie Iron Man » : `CardFinder(name="Zombie Iron Man")` precis -- un seul personnage de ce
#    nom dans le pack (`hg008`, Villain, Horde deck (Metazombies)), aucune ambiguite avec le heros officiel
#    « Iron Man » (nom different, pas de collision de `CardFinder(name=...)`).
#  - « gets +2* hit points » : PAS « +2 hit points » fixe -- l'etoile scale le bonus avec le nombre de heros a
#    la table, exactement comme le total de PV DE BASE de Zombie Iron Man (`hg008`, « 11* ») est lui-meme
#    multiplie par le nombre de heros. Passer un `int` nu (`health=2`) aurait fige le bonus a 2 PV quelle que
#    soit la table, alors que le texte imprime porte la MEME etoile que le PV de base du personnage -- `health=
#    "2*"` (chaine, pas entier) est la seule valeur qui respecte le texte.
#  - « Spend 3 resources » SANS icone ni mention « of any type »/« of the same type » imprimee : contrairement
#    a `01119` (`Cost("YBR")`, trois icones DISTINCTES imprimees : energie + mental + physique), le cout ici
#    est un montant GENERIQUE -- `Cost("3")` (n'importe quelle combinaison de 3 ressources, sans restriction de
#    type), meme convention deja vue sur `hg018`/`hg019` dans ce meme set signature (« Spend 2 resources »,
#    texte egalement sans icone ni qualificatif).
#  - « Hero Action » : n'importe quel heros, a SON tour, pas seulement le controleur de Zombie Iron Man --
#    `AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction)` est generique (`WhenInYourPlayTurn`),
#    identique a `01119` : rien a restreindre au proprietaire du vilain.
#  - Traits imprimes « TECH », « UPGRADE » : traits DE SAVEUR (theme + type de carte Attachment), aucun mot-cle
#    moteur a coder -- absents de `docs/reference/mots-cles/` (meme statut deja arbitre sur `hg019`).
#  - Pas de limite imprimee, pas de condition « unless »/« otherwise »/« without », pas de choix de cible :
#    rien d'autre a coder.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(name="Zombie Iron Man")
        ),
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Zombie Iron Man"),
            health="2*",
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCost(Cost("3")),
    ]
