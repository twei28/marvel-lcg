# TODO / SPEC — Serveur permanent multijoueur

**Statut :** conçu, non planifié, non implémenté
**Date de conception :** 2026-07-28
**Origine :** scénario B de la discussion « jouer en ligne à plusieurs » (le scénario A, tunnel + mot de passe, est livré : `launcher-multi.sh`)
**Rapport à la roadmap :** hors des 7 phases de la refonte UI. Indépendant : ne touche pas aux écrans.

---

## 1. Ce qui est déjà livré (scénario A)

Une partie en ligne fonctionne aujourd'hui : `launcher-multi.sh` démarre le moteur avec `launch.online.json` (mot de passe actif) et un tunnel Cloudflare, puis affiche un lien `/rejoindre.html` et un mot de passe. Vérifié en partie réelle à 2 joueurs.

Ses limites, qui sont exactement l'objet de ce todo :

- l'URL change à chaque lancement,
- le PC de l'hôte doit rester allumé et le script tourner,
- un seul mot de passe pour tout le monde,
- rien n'empêche un joueur de prendre le siège d'un autre (`?p=2`) ni de tout voir (`?hot_seat`).

## 2. Les quatre chantiers

### 2.1 Orchestrateur de tables

**Le fait :** un process = une partie. `/new` appelle `self.game.NewGame(...)` sur l'instance unique, donc lancer une partie détruit celle en cours (c'est écrit noir sur blanc dans `ui-check/tests/lancement-partie.spec.ts`). `client_synced` est un tableau de 4, un jeu = 4 sièges maximum.

**Le travail :** un petit service qui démarre un process de jeu par table sur un port dédié, et un reverse proxy (Caddy ou nginx) qui route `/table/<id>/` vers le bon port. Arrêt automatique d'une table inactive depuis N heures.

**Ce qui aide :** `server_addresses` et `port` sont déjà des variables de configuration, et `launcher_fast.py --config` accepte déjà un fichier de configuration par partie. Un fichier de configuration généré par table suffit.

### 2.2 Identité par siège — le vrai sujet

**Le fait, vérifié dans le code :** `get_player_ids` (`server_base.py`) lit simplement `?p=` dans l'URL, et renvoie **tous** les sièges si `?hot_seat` est présent. Aucune preuve d'identité n'est demandée nulle part.

**Le fait plus gênant :** `handle_get_world` (`server_sync.py`) renvoie `controller.world.render.descriptor`, **le même pour tout le monde**. Chaque carte porte un champ `visible_for_players`, et c'est le **navigateur** qui décide de masquer (`public/js/marvel/descriptor.js`, méthode `isVisible()`). Autrement dit : **le secret des mains n'est pas appliqué côté serveur**. Un joueur curieux voit la main des autres en lisant la réponse réseau, sans même tricher dans l'interface.

**Conséquence :** un reverse proxy qui signerait les URL de siège ne suffit pas. Il empêcherait l'usurpation de siège, mais pas la lecture des mains adverses, puisque l'information part du serveur.

**Le travail, en deux niveaux :**

1. **Jetons de siège** (proxy ou moteur) : une URL de siège signée, non transférable, qui force `p` et interdit `hot_seat`, `debug`, `show`, `show_all_cards`. Corrige l'usurpation. Faisable sans toucher au moteur.
2. **Filtrage du descripteur côté serveur** : ne sérialiser pour un client que ce que `visible_for_players` l'autorise à voir. **Modification du moteur**, sur un chemin très chaud (`handle_get_world` et `WebSendRender`), avec un risque de désynchronisation si le filtrage retire des objets que le client attend.

Entre amis, le niveau 1 suffit largement. Pour un serveur ouvert, le niveau 2 est obligatoire.

### 2.3 Reconnexion et sauvegarde

**Le fait :** les briques existent (`/save_replay_data` produit la scène compressée, `/load_replay_data` la recharge, `session.LoadScene` gère l'étape). Ce qui manque est la boucle : sauvegarde périodique, restauration au redémarrage, et reprise propre d'un client qui revient.

Le suivi de synchronisation par `render_id` et `client_synced` est déjà en place et sert de base à la reprise.

### 2.4 Images

**Le fait :** 349 Mo d'images dans `assets/pics/`, servies par le serveur de jeu, avec repli sur `image_servers` (cerebro, marvelcdb) quand une image manque localement, et cache disque dans `assets/cache/`. Mesuré à travers le tunnel : ~25 ko et 150 à 200 ms par carte.

**Le travail :** sur un VPS, ne pas embarquer les 349 Mo mais s'appuyer sur `image_servers` et le cache disque, ou pointer les clients directement vers le CDN. `cache_max_age` est déjà relevé à 24 h dans `launch.online.json`.

## 3. Ordre recommandé

1. **2.2 niveau 1** (jetons de siège) — c'est le seul trou qui gêne dès aujourd'hui, même en tunnel entre amis, et il ne demande aucune modification du moteur.
2. **2.1** (orchestrateur) — sans lui, pas de serveur permanent.
3. **2.3** (reconnexion) — devient nécessaire dès qu'une partie dure plus qu'une soirée.
4. **2.4** (images) — au moment du déploiement réel.
5. **2.2 niveau 2** (filtrage serveur) — seulement si le serveur s'ouvre au-delà du cercle d'amis.

## 4. Ce qu'il faut décider avant de commencer

1. **Public visé.** Cercle d'amis (le niveau 1 suffit, hébergement chez toi possible) ou serveur ouvert (niveau 2 obligatoire, VPS, et exposition juridique réelle : héberger publiquement un Marvel Champions non officiel appelle un retrait pour propriété intellectuelle). Cette réponse commande tout le reste.
2. **Hébergement.** VPS loué, ou machine à la maison avec un nom de domaine et un tunnel permanent (Cloudflare Tunnel nommé, pas le tunnel jetable actuel).
3. **Comptes.** Un mot de passe par table, ou de vrais comptes joueurs. Un mot de passe par table couvre le cercle d'amis sans rien construire.

## 5. Hors périmètre

- Matchmaking, salons publics, classements.
- Choix du deck par chaque joueur depuis son siège : demande un salon d'attente partagé avant la partie, que le moteur n'a pas. À traiter ici si ce chantier démarre, en lien avec `2026-07-28-recherche-decks-marvelcdb.md`.
- Parties à plus de 4 joueurs : le moteur est bâti sur 4 sièges.
