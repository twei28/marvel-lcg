// Relais : sert /app/* depuis un build local (DIST) et envoie tout le reste (websocket compris) au serveur de jeu.
// Usage : DIST=<build> PORT=2498 CIBLE=2497 node relais.mjs
import http from 'http'
import net from 'net'
import fs from 'fs'
import path from 'path'
const DIST = process.env.DIST, PORT = +process.env.PORT, CIBLE = +(process.env.CIBLE ?? 2497)
const TYPES = { '.js': 'text/javascript', '.css': 'text/css', '.html': 'text/html', '.png': 'image/png', '.webp': 'image/webp', '.ttf': 'font/ttf', '.woff2': 'font/woff2', '.json': 'application/json', '.svg': 'image/svg+xml' }
http.createServer((req, res) => {
  const u = new URL(req.url, 'http://x')
  if (u.pathname.startsWith('/app/')) {
    const f = path.join(DIST, decodeURIComponent(u.pathname.slice(5)))
    if (fs.existsSync(f) && fs.statSync(f).isFile()) { res.writeHead(200, { 'content-type': TYPES[path.extname(f)] ?? 'application/octet-stream', 'cache-control': 'no-store' }); return res.end(fs.readFileSync(f)) }
  }
  const p = http.request({ host: '127.0.0.1', port: CIBLE, path: req.url, method: req.method, headers: req.headers }, (r) => { res.writeHead(r.statusCode, r.headers); r.pipe(res) })
  p.on('error', () => res.end())
  req.pipe(p)
}).on('upgrade', (req, socket, head) => {
  const s = net.connect(CIBLE, '127.0.0.1', () => {
    s.write(`${req.method} ${req.url} HTTP/1.1\r\n` + Object.entries(req.headers).map(([k, v]) => `${k}: ${v}`).join('\r\n') + '\r\n\r\n')
    s.write(head); s.pipe(socket); socket.pipe(s)
  })
  s.on('error', () => socket.destroy()); socket.on('error', () => s.destroy())
}).listen(PORT, '127.0.0.1', () => console.log('relais', PORT, '->', CIBLE, DIST))
