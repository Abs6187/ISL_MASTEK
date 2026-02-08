/**
 * Signify PWA Registration & Install Prompt
 *
 * This script is entirely optional. It registers the service worker
 * and handles the install prompt. If the browser doesn't support
 * service workers or PWA features, this script does nothing.
 *
 * Include via: <script src="pwa.js" defer></script>
 */
(function() {
  'use strict';

  // ── Feature detection ─────────────────────────────────────────
  if (!('serviceWorker' in navigator)) {
    console.log('[PWA] Service workers not supported');
    return;
  }

  // ── Service Worker Registration ───────────────────────────────
  window.addEventListener('load', function() {
    navigator.serviceWorker.register('/sw.js', { scope: '/' })
      .then(function(registration) {
        console.log('[PWA] Service worker registered, scope:', registration.scope);

        registration.addEventListener('updatefound', function() {
          var newWorker = registration.installing;
          if (newWorker) {
            newWorker.addEventListener('statechange', function() {
              if (newWorker.state === 'activated') {
                console.log('[PWA] New service worker activated');
              }
            });
          }
        });
      })
      .catch(function(err) {
        console.warn('[PWA] Service worker registration failed:', err);
      });
  });

  // ── Install Prompt Handling ───────────────────────────────────
  var deferredPrompt = null;
  var installBtn = null;

  window.addEventListener('beforeinstallprompt', function(e) {
    e.preventDefault();
    deferredPrompt = e;
    showInstallButton();
  });

  window.addEventListener('appinstalled', function() {
    console.log('[PWA] App installed successfully');
    deferredPrompt = null;
    hideInstallButton();
  });

  function showInstallButton() {
    if (installBtn) {
      installBtn.style.display = 'flex';
      return;
    }

    installBtn = document.createElement('button');
    installBtn.id = 'pwa-install-btn';
    installBtn.innerHTML = '📲';
    installBtn.title = 'Install Signify App';
    installBtn.setAttribute('aria-label', 'Install Signify App');

    var style = document.createElement('style');
    style.textContent = [
      '#pwa-install-btn {',
      '  position: fixed;',
      '  bottom: 24px;',
      '  left: 24px;',
      '  width: 52px;',
      '  height: 52px;',
      '  border-radius: 50%;',
      '  border: none;',
      '  background: linear-gradient(135deg, #6a11cb, #2575fc);',
      '  color: #fff;',
      '  font-size: 1.5rem;',
      '  display: flex;',
      '  align-items: center;',
      '  justify-content: center;',
      '  cursor: pointer;',
      '  z-index: 9998;',
      '  box-shadow: 0 4px 15px rgba(0,0,0,0.3);',
      '  transition: transform 0.3s, box-shadow 0.3s, opacity 0.3s;',
      '  animation: pwa-pulse 2s ease-in-out 3;',
      '}',
      '#pwa-install-btn:hover {',
      '  transform: scale(1.15);',
      '  box-shadow: 0 6px 20px rgba(106,17,203,0.5);',
      '}',
      '@keyframes pwa-pulse {',
      '  0%, 100% { box-shadow: 0 4px 15px rgba(0,0,0,0.3); }',
      '  50% { box-shadow: 0 4px 25px rgba(106,17,203,0.6); }',
      '}',
      '@media (max-width: 480px) {',
      '  #pwa-install-btn { bottom: 16px; left: 16px; width: 46px; height: 46px; font-size: 1.3rem; }',
      '}'
    ].join('\n');

    document.head.appendChild(style);
    document.body.appendChild(installBtn);

    installBtn.addEventListener('click', handleInstallClick);
  }

  function hideInstallButton() {
    if (installBtn) {
      installBtn.style.display = 'none';
    }
  }

  function handleInstallClick() {
    if (!deferredPrompt) {
      return;
    }
    deferredPrompt.prompt();
    deferredPrompt.userChoice.then(function(choiceResult) {
      if (choiceResult.outcome === 'accepted') {
        console.log('[PWA] User accepted install prompt');
      } else {
        console.log('[PWA] User dismissed install prompt');
      }
      deferredPrompt = null;
      hideInstallButton();
    });
  }

  // ── Online/Offline status indicator ───────────────────────────
  window.addEventListener('online', function() {
    console.log('[PWA] Back online');
  });

  window.addEventListener('offline', function() {
    console.log('[PWA] Gone offline');
  });

})();
