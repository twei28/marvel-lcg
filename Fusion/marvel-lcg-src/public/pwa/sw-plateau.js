// Le service worker MINIMAL de l'application installee (zone 3 du telephone,
// 10/10/2026). Il ne garde RIEN en cache : pas de mode hors ligne, le jeu a
// besoin de son moteur. Il n'existe que parce que certains navigateurs
// exigent un service worker avec un gestionnaire `fetch` pour proposer
// l'installation. Servi a la racine (/sw-plateau.js, web_server.py).
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (evenement) => evenement.waitUntil(self.clients.claim()));
// Sans `respondWith` : chaque requete part au reseau, exactement comme sans lui.
self.addEventListener('fetch', () => {});
