const CACHE_NAME = 'zalihe-v110'; // Povećan broj verzije za prisilno osvežavanje!

const urlsToCache = [
  '/Household_supplies/',
  '/Household_supplies/index.html',
  '/Household_supplies/script1.js',
  '/Household_supplies/voiceCommands.js',
  '/Household_supplies/productParts.js',
  '/Household_supplies/manifest.json',
  '/Household_supplies/icons/logo.png'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('✅ Keširanje novih fajlova...');
                return cache.addAll(urlsToCache);
            })
            .then(() => {
                console.log('✅ Svi fajlovi uspesno keširani');
                return self.skipWaiting();
            })
            .catch(error => {
                console.error('❌ Greška pri keširanju:', error);
            })
    );
});

self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(keys => {
            return Promise.all(keys.map(key => {
                if (key !== CACHE_NAME) {
                    console.log('🗑️ Brisanje starog keša:', key);
                    return caches.delete(key);
                }
            }));
        }).then(() => {
            console.log('✅ Service Worker v110 aktiviran');
            return self.clients.claim();
        })
    );
});

self.addEventListener('fetch', event => {
    if (event.request.url.startsWith('chrome-extension')) {
        return;
    }
    
    // Za JavaScript fajlove uvek idi prvo na MREŽU da se ne zaglavi stari kod
    if (event.request.url.endsWith('.js')) {
        event.respondWith(
            fetch(event.request)
                .then(response => {
                    const responseToCache = response.clone();
                    caches.open(CACHE_NAME).then(cache => cache.put(event.request, responseToCache));
                    return response;
                })
                .catch(() => caches.match(event.request)) // Ako nema mreže, uzmi iz keša
        );
        return;
    }

    // Za ostale fajlove (slike, HTML) traži prvo keš
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                if (response) return response;
                
                return fetch(event.request).then(response => {
                    if (!response || response.status !== 200 || response.type !== 'basic') {
                        return response;
                    }
                    const responseToCache = response.clone();
                    caches.open(CACHE_NAME).then(cache => cache.put(event.request, responseToCache));
                    return response;
                });
            })
            .catch(() => caches.match('/Household_supplies/index.html'))
    );
});
