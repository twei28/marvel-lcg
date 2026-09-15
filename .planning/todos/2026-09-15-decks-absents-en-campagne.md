# « Je ne retrouve pas mes decks pour les campagnes »

**Question de l'utilisateur, 15/09/2026**, suivie de : « en fait je vois que mes
decks ne sont pas retenus, j'ai l'impression ».

⚠ **Mise de côté avant d'avoir la réponse à la seule question qui compte** : il
n'a pas dit s'il ne les VOIT PAS dans la liste, ou s'il les voit et que le choix
ne TIENT PAS. Les deux mènent à des causes très différentes. Ne rien creuser
avant.

## Ce qui est établi, et qu'il ne faut pas refaire

**Les decks sont bien retenus.** 88 fichiers dans `deck/custom/` sur le serveur,
88 aussi en local. Le serveur les expose : `GET /list_deck?` les rend tous.

**L'écran des campagnes utilise le MÊME sélecteur que les parties classiques.**
`prepare/app.js:59` le dit : « le mode Campagne a son propre écran, une seule
chose lui manque, choisir une équipe, et ce sélecteur-là vit ici. Plutôt que de
le dupliquer, l'écran des campagnes nous envoie sur `/prepare.html?campagne` ».
La liste vient donc de `catalog.decksForHero()` dans les deux cas : deck de
base, decks sauvegardés, paquets d'aspect.

**Un mécanisme suspect, à regarder en premier quand on rouvrira.**
`prepare/app.js:72`, registre `DECKS_CAMPAGNE` : « re-cliquer son propre héros
appelle `assignHero`, qui remet le deck de base. Sans ce registre, un clic de
curiosité ferait disparaître le deck de la campagne de la liste, et il n'y
aurait plus aucun moyen d'y revenir sans ressortir de l'écran. »

**L'appariement d'un deck sauvegardé à un héros** se fait sur
`d.hero[0].split(",")[0] === hero.heroCardId` (`catalog.js:432`). Une identité
alternative dont le `heroCardId` diffère ne verrait donc pas ses decks.

## ⚠ Un défaut trouvé au passage, indépendant de la question

`deploiement/deployer.ps1:95` exclut `--exclude=decks` de l'archive. **Le
dossier s'appelle `deck/`, au singulier.** L'exclusion ne s'applique donc à
rien : le `deck/` local part dans l'archive à chaque déploiement et s'extrait
par-dessus celui du serveur.

L'extraction n'efface rien, un deck construit sur le site survit donc. Mais un
deck local PORTANT LE MÊME NOM DE FICHIER écrase celui du serveur, sans bruit.
Même remarque à vérifier pour les autres exclusions de cette ligne
(`sauvegardes`, `saves`) si les dossiers réels portent un autre nom.

## Statut

**Mis de côté le 15/09/2026 à la demande de l'utilisateur.** Rien modifié.
