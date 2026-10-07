// Injecte en tete de CHAQUE page du jeu (voir construire.py). Les pages tournent dans un <iframe> de la
// coquille (navigateur.html) : c'est elle qui tient le moteur, et elle ne se recharge jamais.
// Ici, on redirige fetch, XMLHttpRequest et WebSocket du cadre vers ce moteur.
(() => {
  if (window === window.top) return;
  const M = window.top.__moteur;
  if (!M) return;
  const STATIQUE = /^\/(app|public|css|js|fonts|img|effects|stories|scan|assets|sounds|favicon\.ico|[A-Za-z0-9_.-]+\.html$)/;
  const natif = window.fetch.bind(window);
  const routeMoteur = (url) => url.origin === location.origin && !STATIQUE.test(url.pathname);

  // Version publique, SANS compte : ni signalement de bug, ni administration (ils passent par le serveur du site).
  const BUG = new Set(["/post_rapport_bug", "/get_rapport_actif", "/get_site_admin", "/get_messages_prives", "/post_messages_lus"]);
  window.fetch = async (input, init) => {
    const url = new URL(typeof input === "string" ? input : input.url, location.href);
    if (url.origin === location.origin && BUG.has(url.pathname)) {
      const corps = url.pathname === "/get_rapport_actif" ? '{"actif":false}' : url.pathname === "/get_messages_prives" ? "[]" : "";
      return new Response(corps, { status: url.pathname === "/post_rapport_bug" ? 403 : 200, headers: { "Content-Type": "application/json" } });
    }
    if (!routeMoteur(url)) return natif(input, init);
    const methode = ((init && init.method) || (typeof input !== "string" && input.method) || "GET").toUpperCase();
    const corps = init && typeof init.body === "string" ? init.body : "";
    const rep = await M.requete(methode, url.pathname, url.search.slice(1), corps);
    // Un fichier que le moteur n'a pas (image, son...) : on retente sur l'hebergeur statique.
    if (rep.status === 404 && methode === "GET") return natif(input, init);
    return rep;
  };

  // XMLHttpRequest (runtime historique) : emule par-dessus fetch, requetes asynchrones seulement.
  class FauxXHR {
    constructor() { this.readyState = 0; this.status = 0; this.responseText = ""; this.response = null; this.responseType = ""; this._h = {}; this._ev = {}; }
    open(m, u) { this._m = m; this._u = u; this.readyState = 1; this._maj(); }
    setRequestHeader() {}
    getResponseHeader(n) { return this._rh ? this._rh.get(n) : null; }
    getAllResponseHeaders() { return ""; }
    overrideMimeType() {}
    addEventListener(t, f) { (this._ev[t] = this._ev[t] || []).push(f); }
    removeEventListener(t, f) { this._ev[t] = (this._ev[t] || []).filter((x) => x !== f); }
    abort() { this._abort = true; }
    _maj() { this.onreadystatechange && this.onreadystatechange.call(this); (this._ev.readystatechange || []).forEach((f) => f.call(this)); }
    _fin(t) { const e = { target: this, type: t }; this["on" + t] && this["on" + t].call(this, e); (this._ev[t] || []).forEach((f) => f.call(this, e)); }
    send(corps) {
      window.fetch(new URL(this._u, location.href).href, { method: this._m, body: typeof corps === "string" ? corps : undefined })
        .then(async (r) => {
          if (this._abort) return;
          this._rh = r.headers; this.status = r.status; this.statusText = r.statusText;
          if (this.responseType === "arraybuffer") this.response = await r.arrayBuffer();
          else if (this.responseType === "blob") this.response = await r.blob();
          else { this.responseText = await r.text(); this.response = this.responseType === "json" ? JSON.parse(this.responseText || "null") : this.responseText; }
          this.readyState = 4; this._maj(); this._fin("load"); this._fin("loadend");
        })
        .catch(() => { this.readyState = 4; this.status = 0; this._maj(); this._fin("error"); this._fin("loadend"); });
    }
  }
  window.XMLHttpRequest = FauxXHR;

  // Retire du DOM les boutons de signalement de bug (l'ecran de preparation les construit sans demander au serveur)
  // et ajoute « Exporter / Importer mes parties » a la rangee des boutons d'en-tete.
  const MASQUES = /^(🐞\s*)?(Signaler un bug|Report a bug|Mes signalements|My reports|Bug)$/i;
  let ajoute = false;
  const parler = (msg) => { try { window.top.alert(msg); } catch (e) { /* */ } };
  function bouton(texte, titre, action) {
    const b = document.createElement("button");
    b.type = "button"; b.textContent = texte; b.title = titre; b.addEventListener("click", action); return b;
  }
  function ajouterSauvegardes(rangee) {
    if (ajoute || !rangee || !location.pathname.endsWith("/prepare.html")) return;
    ajoute = true;
    const champ = document.createElement("input");
    champ.type = "file"; champ.accept = ".json,application/json"; champ.style.display = "none";
    champ.addEventListener("change", async () => {
      const f = champ.files[0]; champ.value = ""; if (!f) return;
      try { parler((await M.importer(f)) + " fichier(s) importe(s). Ouvre « Reprendre » pour retrouver tes parties."); }
      catch (e) { parler("Import impossible : " + (e && e.message ? e.message : e)); }
    });
    rangee.append(
      bouton("💾 Exporter mes parties", "Telecharge un fichier avec toutes tes parties et reglages", () => M.exporter().catch((e) => parler("Export impossible : " + e.message))),
      bouton("📂 Importer", "Recharge un fichier d'export", () => champ.click()),
      champ);
  }
  function nettoyer() {
    document.querySelectorAll("button, a").forEach((b) => { if (MASQUES.test((b.textContent || "").trim())) b.remove(); });
    ajouterSauvegardes(document.querySelector(".reprise-boutons"));
  }
  new MutationObserver(nettoyer).observe(document.documentElement, { childList: true, subtree: true });
  document.addEventListener("DOMContentLoaded", nettoyer);

  class FauxWS {
    constructor(url) { this.url = url; this.readyState = 0; this._ev = {}; M.ouvrirWS(this); }
    send(t) { M.envoyerWS(String(t)); }
    close() { if (this.readyState === 3) return; this.readyState = 3; M.fermerWS(this); this._f("close", { code: 1000 }); }
    addEventListener(t, f) { (this._ev[t] = this._ev[t] || []).push(f); }
    removeEventListener(t, f) { this._ev[t] = (this._ev[t] || []).filter((x) => x !== f); }
    _f(t, e) { this["on" + t] && this["on" + t](e); (this._ev[t] || []).forEach((f) => f(e)); }
    _ouvert() { this.readyState = 1; this._f("open", {}); }
    _recevoir(json) { this._f("message", { data: json }); }
  }
  FauxWS.CONNECTING = 0; FauxWS.OPEN = 1; FauxWS.CLOSING = 2; FauxWS.CLOSED = 3;
  window.WebSocket = FauxWS;
})();
