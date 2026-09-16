# Créditer les auteurs des packs fan-made

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

### Les trous connus

- **Iron Patriot** : auteur INTROUVABLE. Le zip est là
  (`A créer/Iron Patriot-20260829T085900Z-1-001.zip`), aucune fiche ne le
  nomme, l'archive non plus.
- **Beast** : la fiche parle d'un « message Discord pour l'auteur du pack »
  sans le nommer à cet endroit. À retrouver.
- **Sentinel** : le nom T-Wrecks vient d'un MESSAGE DE COMMIT, pas d'une source
  du pack. Le plus faible des treize.

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
