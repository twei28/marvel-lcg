# Créditer les auteurs des packs fan-made

**CLOS le 21/10/2026** (item 16 du backlog). Décisions de l'utilisateur : la
liste reconstituée ci-dessous est acceptée telle quelle, affichage dans la
modale du héros, formulation « Pack créé par X ». Implémenté : `bioDuHeros`
(`app.js`) lit le champ `custom` déjà posé carte par carte sur la plupart des
packs (relu par `catalog.js` pour les scénarios, donc déjà une source établie,
pas un nouveau mécanisme). Seuls Conan et Red Sonja (RyCoRan) en manquaient,
complétés sur leurs 42 cartes. Vérifié en vrai (Agatha Harkness → Ripper3,
Conan → RyCoRan, un héros officiel → rien affiché).

**Demande de l'utilisateur, 16/09/2026** : « confirmer chaque personnage
fan-made avec son auteur, et le créditer, par exemple quand on clique sur le
personnage ou un truc du style. Mais d'abord je dois confirmer que ta liste est
bonne. »

## ⚠ LA LISTE N'EST PAS VALIDÉE

Elle a été reconstituée le 16/09/2026 **à partir des fiches de portage de ce
dépôt**, pas des cartes ni des zips d'origine. Aucun auteur ne doit être
affiché dans le jeu avant que l'utilisateur ait confirmé, ligne par ligne.

| Auteur | Packs attribués | Confirmé |
|---|---|---|
| **Rainy** | Hulk, Viv Vision, Iron Man (Model 42), Lady Sif, Beta Ray Bill, Black Cat, Spider-Man Noir, Throg, Sunfire, Ares, Blade, Spider-Man 2099, Superior Spider-Man, Muse | ☐ |
| **Kajislav** | Armored Spider-Man, Blink, Doctor Druid, Texas Twister, Mockingbird, Spider-Woman | ☐ |
| **BLUEHG** | Gorr the God Butcher, ses deux sets modulaires, Yondu | ☐ |
| **DesignHacker** | Night Thrasher, aspect Determination, scénario The Spot | ☐ |
| **Ripper3** | Agatha Harkness, Alligator Loki, campagne Web of Deceit | ☐ |
| **Grawlix Ipsum** | Doctor Doom, et ses Alt Arts | ☐ |
| **jakxin** | Hellcat | ☐ |
| **CptScorp** | Venompool | ☐ |
| **Dipsome** | Harry Osborn (Green Goblin) | ☐ |
| **BlueRiver** | Cameo Compliment | ☐ |
| **Mozilla** | Zeus | ☐ |
| **ekAugust** | Venomized | ☐ |
| **T-Wrecks** | Sentinel | ☐ |
| **Juri Krasko** | Angela | ☐ |
| **Neptune** | Iron Patriot | ☐ |
| **RyCoRan** | Howard the Duck | ☐ |
| **Lord Havok** | Dazzler | ☐ |
| **Nugget** | Lockjaw | ☐ |

### ⚠ Relevé du 16/09/2026 sur `tools/prefixes_fanmade.json`

Ce fichier nomme les auteurs dans ses notes, pack par pack, et c'est une
source PRIMAIRE (écrite au portage) là où la liste ci-dessus était
reconstituée. Croisé avec `deck/starter/` pour ne compter que les personnages
JOUABLES :

- **62 personnages fan-made jouables** dans le jeu ;
- **27 ont un auteur attesté** dans ce fichier, répartis sur **11 auteurs** ;
- **35 n'en ont aucun** : ce sont les packs migrés en bloc le 12/08/2026, dont
  la note ne dit rien de leur origine.

Deux corrections apportées à la table ci-dessus :

- **Juri Krasko** (Angela) n'y figurait pas du tout ;
- **Iron Patriot a un auteur : Neptune**, contrairement à ce qui est écrit
  juste en dessous.

Les 35 personnages sans auteur sont le vrai travail restant, et il ne se fera
pas depuis ce dépôt : il faut remonter aux zips et aux fils Discord d'origine.

### Les trous connus

- ~~**Iron Patriot** : auteur INTROUVABLE.~~ **Trouvé le 16/09/2026** :
  `prefixes_fanmade.json` le donne à **Neptune**. Reste à confirmer.
- **Beast** : la fiche parle d'un « message Discord pour l'auteur du pack »
  sans le nommer à cet endroit. À retrouver.
- **Sentinel** : le nom T-Wrecks vient d'un MESSAGE DE COMMIT, pas d'une source
  du pack. Le plus faible des treize.

### Trois auteurs ajoutés le 18/09/2026

Trouvés en relisant les sources primaires, ils ne figuraient pas dans la table :

- **RyCoRan**, Howard the Duck. Source : la note de `tools/prefixes_fanmade.json`
  (« Pack fan-made RyCoRan, zip "Howard the Duck (05-23 Final)" »).
- **Lord Havok**, Dazzler. Même source (« Pack custom de Lord Havok »).
- **Nugget**, Lockjaw. Source : le commentaire en tête de
  `cards/pack/lockjaw/lockjaw/__init__.py`. La note de `prefixes_fanmade.json`
  est vide pour ce pack, c'est donc le code qui porte l'information.

Au passage, deux attributions déjà présentes se voient confirmées par une
seconde source : **Rainy** pour Blade, et **BlueHG** pour le re-skin
Wolverine X-23.

⚠ Ces trois-là restent à confirmer comme les autres. Ils sont mieux étayés que
Sentinel, qui ne tient que sur un message de commit.

## Ce qui reste à décider, une fois la liste confirmée

**Où le crédit s'affiche.** La piste de l'utilisateur est « quand on clique sur
le personnage ». Trois endroits possibles, à trancher avec lui :

1. la **modale du héros** dans l'assistant (elle existe déjà, montre la
   biographie et les versions) ;
2. l'**aperçu d'une carte** sur le plateau, sous le texte ;
3. une **page de crédits** à part, qui remercierait tout le monde d'un coup.

**Où vit la donnée.** Le pack est déjà identifié par son préfixe de deux
lettres et son numéro de set (`data/sets_info.json`). L'auteur y aurait sa
place, à côté du nom de l'extension : une seule source, lue par l'assistant
comme par le plateau. À confirmer au moment du cadrage.

**La formulation.** « Pack créé par X » ? « Cartes de X » ? Et faut-il un lien
vers son profil, s'il en a un ? Ce sont des gens qui ont travaillé des mois :
la façon de les nommer mérite d'être choisie, pas improvisée.

## Statut

**Notée le 16/09/2026, à confirmer d'abord.** Aucune ligne de code, et la
validation de la liste passe avant tout le reste.
