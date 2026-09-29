# Batterie « Marvelous » : Stan Lee joue chaque carte signature

Prouve que toute carte signature empruntable (classe « Hero », tous les héros
officiels et fan-made, sauf sets masqués) fonctionne quand Stan Lee la joue.
Chaque carte donne DEUX cas du harnais `tools/test_capacites.py` : un TÉMOIN
(la carte jouée par son vrai héros) et la MESURE (la même carte jouée par
Stan Lee, avec le deck signature entier de ce héros dans son `hero_deck`).

| Fichier | Rôle |
|---|---|
| `generer_cas.py` | engendre les cas (pur, déterministe) ; `python3 generer_cas.py` donne les comptes, `python3 generer_cas.py iron_man` imprime les cas d'un deck |
| `batterie_test_capacites.py` | lance `test_capacites.py` avec ces cas (rien n'est modifié dans le harnais) |
| `analyser.py` | apparie témoin/Stan Lee, classe VERT / ÉCART / NON CONCLUANT, regroupe les écarts par famille |

## Lancer

```bash
cd Fusion/marvel-lcg-src
cp -a .game-src .game-src-marvelous          # une fois ; JAMAIS .game
# pilote, 3 héros :
MARVELOUS_DECKS="spider_man,iron_man,spider_man_2099" PARALLELES=4 \
  python3.10 tools/generateurs-marvelous/batterie_test_capacites.py .game-src-marvelous 30000 /tmp/marvelous-pilote.json
# batterie complète (des heures) :
PARALLELES=4 nohup python3.10 tools/generateurs-marvelous/batterie_test_capacites.py .game-src-marvelous 30000 /tmp/marvelous.json > /tmp/marvelous.log 2>&1 &
python3 tools/generateurs-marvelous/analyser.py /tmp/marvelous.json
```

Rejouer un cas seul : `CAS_INDEX=<n> python3.10 tools/generateurs-marvelous/batterie_test_capacites.py .game-src-marvelous 30000`
(l'index est celui du rapport ; le journal du fils est `/tmp/capacites_<CAS_PREFIX><n>.log`).

Règles du harnais qui s'appliquent telles quelles : un dossier de jeu dédié,
jamais deux harnais sur le même dossier, ports sous 49152, une passe
parallèle se compare cas par cas à une passe séquentielle avant de conclure,
et des rouges en masse sont d'abord un artefact à rejouer seul.

## Ce que mesure un cas, et ce qu'il ne voit pas

Mesuré : la carte est en main et **jouable** (`Puzzle.AssertJouable`, lit
`CardFace.CanPlayBy`) ; elle se joue par le vrai chemin, en payant, sans
traceback ; après coup un allié / amélioration / soutien / manigance de joueur
est **en jeu**, un événement a **quitté la main et le deck**. Une empreinte
(cartes du joueur en jeu, main, défausse, PV) est écrite dans le message et
comparée témoin/Stan Lee par `analyser.py`, à titre indicatif.

Non mesuré : que l'**effet** de la carte soit le bon (un événement résolu à
vide est vert), les capacités déclenchées plus tard (Response, Interrupt), et
les cartes dont la mise en place exige une cible absente : elles rougissent
pour le témoin aussi et sont classées NON CONCLUANT, pas ÉCART. Ce sont les
cas à écrire à la main, un par un, quand la batterie générique est verte.
