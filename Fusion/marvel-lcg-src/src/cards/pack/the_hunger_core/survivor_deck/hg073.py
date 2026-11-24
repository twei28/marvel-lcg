from . import *

# DECISION (27/10/2026, passe de fusion hg028-hg076) sur le point « A CONFIRMER » ci-dessous : lecture STRICTE
# retenue, `card_type=Minion`. Le raisonnement de l'agent reposait sur une premisse fausse : « la lecture stricte
# viderait de son sens la moitie du nom imprime (... OR Metazombie) ». Or les 13 Fallen Heroes (hg059-hg071,
# set modulaire) sont des MINIONS portant le trait METAZOMBIE (`data/cards_custom.json`) : « a Zombie or
# Metazombie minion » designe donc exactement hg056/hg057 (trait ZOMBIE) + hg059-hg071 (trait METAZOMBIE),
# et la clause « or Metazombie » garde un effet reel. La lecture large (`Enemy`) laissait au contraire Chewie,
# allie a 0 cout, defausser GRATUITEMENT un Metazombie VILAIN (hg007-hg015, 9 a 15 PV par joueur), ce que le
# mot imprime « minion » exclut. Prouve par trois cas `[hg] hg073` : sbire ZOMBIE (hg056) defausse, sbire
# METAZOMBIE (hg059) defausse, vilain Metazombie (hg013) NON ciblable.
#
# * Chewie — ALLIE (Survivor deck, carte 2/5). Cout 0. THW 0. ATK 1[star]. PV 2. RES wild.
#   SURVIVOR. FLERKEN.
# Action: Exhaust Chewie -> discard a Zombie or Metazombie minion. Chewie takes 1 damage.
#
# ---------------------------------------------------------------------------
# ETAPE 2 : CARTES DE REFERENCE
#
# - Charpente « Action: Exhaust <nom> -> <effet>. <nom> takes 1 damage. » : le cout est SEUL « Exhaust
#   Chewie » (pas de degat DANS le cout, a la difference de `19002` Mantis/`dt066` Misty Knight ou le degat
#   est imprime AVANT la fleche) -- ici « Chewie takes 1 damage » est ecrit APRES la fleche, donc dans
#   l'EFFET, pas le cout. Modele retenu pour « <sujet> deals damage to itself en consequence d'un effet » :
#   `lj024` Wet Slobbering Kiss (`this.DealDamage(effect.targets, 3, effect)`, methode `CardFace.DealDamage`
#   appelee sur SOI-MEME comme source) -- repris ici avec `[this]` comme cible au lieu de `effect.targets`
#   (Chewie se vise LUI-MEME, pas un ennemi choisi).
# - « discard A MINION » choisi par cible (cout d'action, pas un defausse-jusqu'a) : modele officiel `61009`
#   4K Digital Camcorder (pack `jj`), `SetTarget(CardFinder(card_type=Minion, non_trait="ELITE"), range=(1,
#   1))` puis `Faces.DiscardAll([target], effect)` dans le callback.
# - Filtrer par DEUX traits en OU (« Zombie OR Metazombie ») sur une cible : modele `CardFinder(traits=[...])`
#   deja documente comme parametre OR natif (`card_finder/finder.py:133`, commentaire `# OR`), deja employe
#   dans CE scenario par `hg001.py` (commentaire etape 2 : `CardFinder(traits=["METAZOMBIE"], ...)`).
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - « Action » : type de capacite, pas un mot-cle (meme note que `hg072`).
# - Aucun terme en gras hors « Action » : rien d'autre a ficher.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE (etape 5, mots-pieges) -- ⚠ POINT LAISSE EN SUSPENS, MARQUE « A CONFIRMER »
#
# - « a Zombie or Metazombie MINION » : le mot imprime est « minion », mais dans ce scenario les Metazombies
#   NOMMES (Zombie Captain America, etc.) sont codes comme des `Villain` (« a Metazombie is a villain for
#   ALL purposes », commentaire de `commun.py:72`), PAS des `Minion` au sens du moteur -- seuls les zombies
#   generiques (`hg056` Hungry Zombie Minion, `hg057` Bloated Zombie Minion) sont de VRAIS `Minion`. Une
#   lecture STRICTE du type moteur limiterait donc cette carte a hg056/hg057 (le Coeur et les 9 Metazombies
#   nommes seraient hors de portee), ce qui viderait de son sens la moitie du nom imprime (« ... OR
#   Metazombie »). J'ai retenu `CardFinder(card_type=Enemy, traits=["ZOMBIE", "METAZOMBIE"])` -- `Enemy` est
#   la classe ANCETRE commune a `Minion` ET `Villain` (`base/villain.py:11`, `card_type/minion.py:10`), donc
#   le filtre couvre a la fois les zombies generiques ET les Metazombies nommes, conforme a l'intention
#   thematique imprimee (« a Zombie or Metazombie [...] » devrait pouvoir viser n'importe quel ennemi du
#   deck de rencontre portant l'un des deux traits, pas seulement les non-nommes). **A CONFIRMER** : si la
#   lecture voulue est la restriction stricte « uniquement des vrais Minion », remplacer `card_type=Enemy`
#   par `card_type=Minion` ne change qu'UNE ligne (`cible = CardFinder(...)` ci-dessous).
# - « Chewie TAKES 1 damage » (pas « deal 1 damage to Chewie ») : meme sujet grammatical, meme effet --
#   `this.DealDamage([this], 1, effect)`, `this` a la fois source et cible (pas une attaque, pas de
#   consequence de defense : degat direct, comme `lj024`).
# - Pas de `unless`/`otherwise`/`instead`/limite imprimee : rien d'autre a coder.
#
# ---------------------------------------------------------------------------
# ETAPE 6 : BLOC NOMBRES, TEXTE <-> CODE
#
# - « Chewie takes 1 damage » -> `this.DealDamage([this], 1, effect)`, `1` explicite.
# - `desc.ATK = "1*"` : LU NATIVEMENT (etoile de degats consequents officielle sur un Allie, voir la note
#   generale posee dans `hg072.py` -- pas un symbole « par heros » ici). Aucun script requis.
#
# A CONFIRMER EN PARTIE REELLE : meme reserve que `hg072` -- ni `test_capacites.py` ni l'autoplay n'ont ete
# lances sur ce lot (consigne de la tache).


def GetAbilities() -> Sequence['Ability']:

    cible = CardFinder(card_type=Minion, traits=["ZOMBIE", "METAZOMBIE"])

    def chewie(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)

        for target in effect.targets:
            Faces.DiscardAll([target], effect)
        this.DealDamage([this], 1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            chewie,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(cible, range=(1, 1), canbe_discard=True),
    ]
