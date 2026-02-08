/**
 * Signify PWA Service Worker
 * 
 * Caching strategies:
 *   - App shell (HTML, CSS, JS, SVG): Cache-first, network fallback
 *   - API calls (/predict, /ask_ai): Network-only (real-time predictions)
 *   - External CDN resources: Stale-while-revalidate
 *   - Images: Cache-first with lazy caching on fetch
 *   - Offline fallback: /offline.html for navigation requests
 *
 * This service worker is entirely optional. If it fails to register
 * or encounters an error, the app continues to work normally.
 */

var CACHE_NAME = 'signify-v1';

var APP_SHELL = [
  '/',
  '/index.html',
  '/learn.html',
  '/single.html',
  '/quiz.html',
  '/mode.html',
  '/qm.html',
  '/about.html',
  '/contact.html',
  '/examples.html',
  '/faqs.html',
  '/offline.html',
  '/css/index.css',
  '/css/learn.css',
  '/css/single.css',
  '/css/quiz.css',
  '/css/mode.css',
  '/css/qm.css',
  '/css/styles.css',
  '/js/index.js',
  '/js/learn.js',
  '/js/single.js',
  '/js/quiz.js',
  '/js/mode.js',
  '/js/ai_helper.js',
  '/js/sound_manager.js',
  '/pwa.js',
  '/svg/hs1.svg',
  '/svg/hs2.svg',
  '/svg/hs3.svg',
  '/svg/hs4.svg',
  '/svg/learnbuttonSVG.svg',
  '/svg/playbuttonSVG.svg',
  '/images/ai_mascot.png',
  '/manifest.json',
  '/general.json',
  '/social.json',
  '/sports.json',
  '/tech.json',
  '/settings.json',
  '/js/math.json',
  '/qm.js'
];

var API_ROUTES = ['/predict', '/ask_ai', '/healthz'];

// Install: precache the app shell
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('[SW] Precaching app shell');
        return cache.addAll(APP_SHELL).catch(function(err) {
          console.warn('[SW] Some app shell resources failed to cache:', err);
          // Don't fail install if some resources are missing
          // Cache what we can individually
          return Promise.all(
            APP_SHELL.map(function(url) {
              return cache.add(url).catch(function() {
                console.warn('[SW] Failed to cache:', url);
              });
            })
          );
        });
      })
      .then(function() {
        return self.skipWaiting();
      })
  );
});

// Activate: clean up old caches
self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys()
      .then(function(cacheNames) {
        return Promise.all(
          cacheNames
            .filter(function(name) { return name !== CACHE_NAME; })
            .map(function(name) {
              console.log('[SW] Deleting old cache:', name);
              return caches.delete(name);
            })
        );
      })
      .then(function() {
        return self.clients.claim();
      })
  );
});

// Fetch: apply caching strategies based on request type
self.addEventListener('fetch', function(event) {
  var url = new URL(event.request.url);

  // Skip non-GET requests
  if (event.request.method !== 'GET') {
    return;
  }

  // API routes: network-only (predictions must be real-time)
  if (API_ROUTES.some(function(route) { return url.pathname.startsWith(route); })) {
    return;
  }

  // External CDN resources: stale-while-revalidate
  if (url.origin !== location.origin) {
    event.respondWith(staleWhileRevalidate(event.request));
    return;
  }

  // Navigation requests (HTML): network-first with offline fallback
  if (event.request.mode === 'navigate') {
    event.respondWith(networkFirstWithOfflineFallback(event.request));
    return;
  }

  // Static assets: cache-first
  event.respondWith(cacheFirst(event.request));
});

/**
 * Cache-first strategy: serve from cache, fall back to network.
 * Caches the network response for future use.
 */
function cacheFirst(request) {
  return caches.match(request)
    .then(function(cached) {
      if (cached) {
        return cached;
      }
      return fetch(request)
        .then(function(response) {
          if (response && response.status === 200 && response.type === 'basic') {
            var responseClone = response.clone();
            caches.open(CACHE_NAME).then(function(cache) {
              cache.put(request, responseClone);
            });
          }
          return response;
        });
    });
}

/**
 * Network-first strategy with offline fallback for navigation.
 * Tries network, falls back to cache, then to /offline.html.
 */
function networkFirstWithOfflineFallback(request) {
  return fetch(request)
    .then(function(response) {
      if (response && response.status === 200) {
        var responseClone = response.clone();
        caches.open(CACHE_NAME).then(function(cache) {
          cache.put(request, responseClone);
        });
      }
      return response;
    })
    .catch(function() {
      return caches.match(request)
        .then(function(cached) {
          return cached || caches.match('/offline.html');
        });
    });
}

/**
 * Stale-while-revalidate for CDN resources.
 * Serves cache immediately, updates cache in background.
 */
function staleWhileRevalidate(request) {
  return caches.open(CACHE_NAME)
    .then(function(cache) {
      return cache.match(request)
        .then(function(cached) {
          var fetchPromise = fetch(request)
            .then(function(response) {
              if (response && response.status === 200) {
                cache.put(request, response.clone());
              }
              return response;
            })
            .catch(function() {
              return cached;
            });
          return cached || fetchPromise;
        });
    });
}
