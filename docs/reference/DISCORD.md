# Jouer depuis Discord (activité de salon vocal)

Permet de lancer une partie NarwhalChampions directement dans un salon vocal
Discord, sans quitter l'application. Ajouté le 28/09/2026.

## Comment ça marche, en bref

- Premier clic sur le bouton d'activité dans un salon vocal : cette personne
  devient l'**hôte**. Elle doit avoir un compte NarwhalChampions existant (pas
  d'inscription depuis ce flux) : sa table à elle démarre.
- Les personnes suivantes du même salon sont des **participants**. Déjà
  connectées : assises directement sur leur siège. Sinon, elles choisissent
  « J'ai un compte » (connexion, puis assises) ou « Je suis invité »
  (assises sans compte). Un siège par personne (`siege_activite_discord`,
  tenu en mémoire par activité : le moteur ne sait pas qui tient un siège
  avant le début de la partie) ; qui revient retrouve le sien (pseudo, ou
  cookie `nc_discord_invite` pour un invité) ; au-delà de trois
  participants, « Table complète ».
- Un salon vocal = une table. Deux clics simultanés dans le même salon ne
  créent jamais deux tables (vérifié par `site/test_activite_discord.py`).
- Une fois assis à la table, tout continue exactement comme d'habitude
  (préparation, salon, plateau) : rien n'est différent depuis ce point.

## Ce qu'il faut créer côté Discord (à faire à la main, un compte Discord à
vous)

1. https://discord.com/developers/applications → **New Application**.
2. Onglet **Activities → URL Mappings** : **Root Mapping** →
   `discord.{DOMAINE}` (ex. `discord.narwhalchampions.com`). **Aucune autre
   entrée** : les anciens mappings `/p1` … `/p30` (28/09/2026) sont à
   supprimer, ils ne servent plus et pourraient intercepter des chemins.
3. Copier l'**Application ID** (identifiant public, pas un secret) dans la
   variable `DISCORD_CLIENT_ID` de l'orchestrateur (voir plus bas).
4. Activer **Activities** et installer l'application sur le serveur Discord
   voulu (lien d'installation du panneau développeur).

Aucun secret client (Client Secret) n'est utilisé : l'intégration se limite
à `DiscordSDK(...).ready()` côté navigateur, sans échange OAuth serveur.

## Comment le jeu tient dans le cadre Discord (29/09/2026)

Trois contraintes de Discord, découvertes en conditions réelles, et ce qui
y répond :

- **Une seule origine.** Discord ne charge que `<clientId>.discordsays.com`,
  qui relaie vers le Root Mapping. Le client du jeu utilise des chemins
  absolus (`/prepare.html`, `/ws`...) : impossible de le servir sous un
  préfixe `/p1`. → L'hôte `discord.{DOMAINE}` porte TOUTES les tables :
  Caddy aiguille chaque requête vers le port de la bonne table d'après le
  cookie `nc_table`, posé par l'orchestrateur quand il assoit quelqu'un. Sans
  ce cookie, et pour le parcours d'entrée (`?frame_id=`, `/connexion`,
  `/pret`, `/entrer`, `/activite_discord`, `/discord-relais.js`), tout va à
  l'orchestrateur. Le lancement (`?frame_id=`) efface `nc_table`.
- **Cookies en iframe tiers.** Un cookie `SameSite=Lax` n'est jamais envoyé
  dans ce cadre, et un `Domain=.{DOMAINE}` y est rejeté. Discord exige
  `SameSite=None; Partitioned`, sans domaine ([doc
  Networking](https://docs.discord.com/developers/activities/development-guides/networking)).
  → Sur l'hôte `discord.*` seulement, le site (`_attributs_cookie`) et le
  moteur (`PoserCookie`, écrit à la main : `http.cookies` de Python 3.10 ne
  connaît pas `Partitioned`) posent leurs cookies ainsi. Ailleurs, rien ne
  change.
- **Le proxy suit les redirections lui-même.** `<clientId>.discordsays.com`
  (un worker Cloudflare) suit tout 3xx côté serveur et rend la page finale
  en 200 : les `Set-Cookie` de la redirection sont perdus et l'adresse du
  cadre ne change pas (mesuré au `curl` à travers le proxy, 29/09/2026 ;
  symptôme : « Introuvable » juste après la connexion). → Sur l'hôte
  `discord.*`, aucune vraie redirection : le site (`_rediriger`) et le
  moteur (middleware `_relais_discord`) rendent une page 200 qui porte les
  cookies et enchaîne par `meta refresh`.
- **Une seule page, jamais rechargée.** Discord n'envoie `READY` qu'une fois
  par cadre : après un rechargement du document, `sdk.ready()` ne revient
  plus et Discord ferme l'activité quelques secondes plus tard ([issue #41
  du SDK](https://github.com/discord/embedded-app-sdk/issues/41) ; constaté
  en prod le 29/09/2026 à chaque étape, même avec un « relais » qui
  rejouait `ready()` sur chaque page, abandonné). → L'amorce (`/` avec
  `?frame_id=`) est une **coquille** qui garde le SDK vivant et affiche le
  jeu dans un `<iframe>` interne, même origine, mêmes cookies partitionnés.
  Tout le parcours (connexion, attente, préparation, plateau) se déroule
  dans ce cadre interne sans que Discord ne voie un seul rechargement.
- **CSP du proxy : `'self'` seulement.** Aucun script d'un CDN ne se charge
  dans le cadre (ni `esm.sh`, ni Google Fonts, qui échoue sans dommage).
  → Le SDK est une copie locale, `site/discord-sdk.mjs` (bundle esm.sh
  2.5.0, MIT), servie en `/discord-sdk.js?v=2.5.0` avec un cache long.
  Pour monter de version : retélécharger le bundle et changer `?v=`.

Vérifié le 29/09/2026 dans un Chrome sans tête, À TRAVERS le proxy Discord,
avec la coquille : cadre interne lancé à la main (Discord absent, `ready()`
ne revient pas), puis connexion, entrée, siège, préparation, plateau et
WebSocket ouvert depuis le plateau, la coquille gardant son adresse d'un bout
à l'autre. Vérifié aussi au `curl` À TRAVERS le proxy Discord
(`https://<clientId>.discordsays.com`, en-têtes de Chrome imités) :
lancement, connexion, attente, `claim_seat`, préparation, plateau et
WebSocket (101) passent, cookies compris. Ce passage par le proxy est le
seul test qui reproduit le vrai cadre : tester sur `discord.{DOMAINE}` en
direct ne voit ni le suivi des redirections ni la CSP du proxy. **Reste non vérifiable hors du vrai client Discord** :
que le relais suffise à garder l'activité ouverte d'une page à l'autre.

## Sur le serveur

- Variable d'environnement à ajouter : `DISCORD_CLIENT_ID` (voir
  `deploiement/narwhal.service`, déjà prêt côté dépôt avec le gabarit
  `@DISCORD_CLIENT_ID@`).
- ⚠ `narwhal.service` est un fichier **surveillé, jamais réécrit**
  automatiquement par `synchroniser-conf.sh` (un réglage posé à la main,
  comme `INSCRIPTION_LIBRE`, y survit sciemment). Sur le serveur déjà en
  service, ajouter la ligne à la main :
  ```
  sudo systemctl edit --full narwhal
  # ajouter : Environment=DISCORD_CLIENT_ID=<l'Application ID copié plus haut>
  sudo systemctl restart narwhal
  ```
- Le `Caddyfile` porte l'en-tête `frame-ancestors` (apex et tables) et le
  bloc `@discord` (dans le bloc joker `*.{DOMAINE}`). ⚠ Ce fichier est
  « surveillé, jamais réécrit » par le déploiement : sur le serveur, il se
  modifie à la main (sauvegarde, `caddy validate --envfile
  /etc/caddy/cloudflare.env`, puis `systemctl reload caddy`).

## Ce qui est testé, ce qui ne peut pas l'être

- Testé (`site/test_activite_discord.py`, 14 assertions, toutes vertes) :
  la logique hôte/participant/connexion requise, l'atomicité entre deux
  ouvertures simultanées du même salon, l'indépendance entre deux salons.
- **Pas automatiquement testable** : tout ce qui exige le vrai client
  Discord (le SDK, l'iframe `/.proxy/`, l'obtention réelle de
  `instance_id`). Aucun harnais ne simule ce cadre ; le premier essai réel,
  avec un compte Discord Developer, est la seule vérification possible.
