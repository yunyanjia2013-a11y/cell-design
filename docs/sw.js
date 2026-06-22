// Service Worker — 离线缓存 v4.0
const CACHE='celldesign-v4';
const URLS=['./','./index.html','./manifest.json','./icons/icon-192.png','./icons/icon-512.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(URLS)));self.skipWaiting()});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))));self.clients.claim()});
self.addEventListener('fetch',e=>{e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request).then(resp=>{if(resp&&resp.status===200){let rc=resp.clone();caches.open(CACHE).then(c=>c.put(e.request,rc))}return resp})))});
