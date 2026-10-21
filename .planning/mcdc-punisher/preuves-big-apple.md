# Preuves PROCESSUS-CARTE : scénario 1 « The Big Apple » (environnements + 9 lieux), PU-5 fin / PU-7

Harnais : `tools/cas/big_apple.py`, préfixe `[big]`. Ville RÉELLE : `Puzzle.InstallerVille(grille, depart, en_jeu=True)` met les 9 lieux
en jeu, chacun dans la zone de SA rangée ; The City / Never Sleeps vont dans la zone commune (indice 1). Lancer :
`bash <script>` avec le filtre `[big]` (le filtre est une sous-chaîne, pas une regex ; une commande contenant le nom du harnais est refusée).
Méthode de substitution : copie du script, `sed` qui casse UNE chose (limite, condition de lieu, effet), relancer, constater rouge, restaurer.

⚠ Pièges trouvés en route (à reporter dans RECETTES-MOTEUR) :
- `Puzzle.CreateEncounterDeck(a, b, c)` : le DESSUS du deck est le DERNIER argument.
- `SetTarget(check_fn=...)` est IGNORÉ pour une cible `from_where=["YourHandCards"]` (jamais appelé) ; `traits=[...]` (OU) marche. Pour une cible `Identity`, `check_fn` est bien appelé.
- Un témoin « pas au lieu » placé dans une AUTRE rangée reste vert sans `Ville.AuLieu` (la zone suffit à bloquer) : le placer dans la MÊME rangée.
- Un ennemi hors de la zone du joueur n'est pas ciblable (R5) : monter un sbire AVANT `InstallerVille` pour qu'il suive le joueur.

### pu005 : The City
- [x] Étape 2 : mu004 (Action d'environnement, coût `Exhaust("YouControlUnit")`), pu121 (`Spend(Cost("1"))`), gmw/16073b (`SetTarget(lambda effect: ...)`).
- [x] Étape 5 : « or » du coût = DEUX Actions jumelles (une par coût) ; aucune limite par round ; les deux puces de règle sont portées par `Ville.Installer` / `Ville.AuLieu`.
- [x] Étape 7 : 3 cas `[big] pu005` (épuiser → Theater District, zone change ; 1 ressource → Lower East Side, même zone, perso pas épuisé ; deux déplacements dans le même round). Script retiré : 3 rouges. Restauré : 3 verts.
- [x] Limite imprimée : NON (témoin d'absence de limite = le 3e cas). Plateau : OUI (jeton de position : PU-8, interface).
Carte terminée : script OUI ; interface (jeton) à faire en PU-8.

### pu031 Theater District
- [x] Réf. mu004 + pu066. 3 cas : soin 4→2 ; témoin d'épuisement (2e Action avec un allié blessé : refusée) ; témoin pas-au-lieu (Hell's Kitchen, même rangée).
- [x] Substitution : sans limite → épuisement rouge ; sans AuLieu → témoin rouge ; soin à 0 → 2 rouges.
Carte terminée : OUI.

### pu036 Soho
- [x] Réf. ar010 (coût +1), 28020 (DrawUp/DiscardHandCards), pu031. 6 cas : Haymaker (2) refusé avec 2 icônes à Soho ; témoin Midtown ; témoin Financial District (même rangée) ; pioche 2/défausse 2 (main 3, deck 31→29) ; épuisement ; pas-au-lieu.
- [x] Substitution : coût +0, coût sans AuLieu, sans limite, Action sans AuLieu, sans pioche : chacune fait rougir au moins un cas.
Carte terminée : OUI.

### pu034 Midtown
- [x] Réf. 12024 (`PlayCardsLikeInTurn(..., update_resources_cost=-1)`), 28020 (« a player » = cible Identity), pu031. 5 cas : Black Widow (3) jouée avec 2 icônes ; témoin sans l'Action ; témoin de trait (Jessica Jones DEFENDER non éligible) ; épuisement (Hellcat reste en main) ; pas-au-lieu (West Village).
- [x] Substitution : sans réduction, sans limite, sans AuLieu, sans traits, sans script : tous rouges.
- ⚠ NON PROUVÉ : le filtre « joueur dans ce territoire » (`check_fn` sur Identity) à DEUX joueurs : le harnais ne sait pas donner une main au joueur 2. Appelé (vérifié par trace), non mesuré.
Carte terminée : OUI, sauf ce point (à vérifier en partie réelle à deux joueurs dans des rangées différentes).

### pu032 Upper East Side
- [x] Réf. jj008, 24030. `EncounterSideScheme` (pas la principale). 3 cas : annexe révélée après 1 traitrise défaussée ; épuisement (la 2e annexe reste dans le deck) ; pas-au-lieu.
- [x] Substitution : sans limite, sans AuLieu, sans reveal, type Minion : tous rouges.
Carte terminée : OUI.

### pu038 Chinatown
- [x] Réf. 53009 (`WhenPlayerWouldBeDealtEncounterCard` + `SetBeInstead`), 16057. « When YOU would be dealt » = le joueur au lieu. 3 cas : traitrise non distribuée, Shocker révélé (1 dégât) ; épuisement ; pas-au-lieu.
- [x] Substitution : sans limite, sans AuLieu, sans instead, sans reveal : tous rouges.
Carte terminée : OUI.
