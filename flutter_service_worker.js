'use strict';
const MANIFEST = 'flutter-app-manifest';
const TEMP = 'flutter-temp-cache';
const CACHE_NAME = 'flutter-app-cache';

const RESOURCES = {"version.json": "8d58cc797747786052ff65bca5618f88",
"index.html": "49def75c6444780d7c55bd0e2e746042",
"/": "49def75c6444780d7c55bd0e2e746042",
"main.dart.js": "4433ef76f1649d862a04688e54a0b5ee",
"flutter.js": "7d69e653079438abfbb24b82a655b0a4",
"favicon.png": "5dcef449791fa27946b3d35ad8803796",
"icons/Icon-192.png": "ac9a721a12bbc803b44f645561ecb1e1",
"icons/Icon-maskable-192.png": "c457ef57daa1d16f64b27b786ec2ea3c",
"icons/Icon-maskable-512.png": "301a7604d45b3e739efc881eb04896ea",
"icons/Icon-512.png": "96e752610906ba2a93c65f8abe1645f1",
"manifest.json": "3fc29f9294b755bca0378065b89e216e",
"assets/AssetManifest.json": "54adeb05c557d4199c324ce25fd9a2da",
"assets/NOTICES": "0a86b3d77e0083fcf551027aeaee0d2d",
"assets/FontManifest.json": "505e76a1e24a31ea1cd99134567d0733",
"assets/AssetManifest.bin.json": "108f9a6077a49310b92daefb60d857ea",
"assets/packages/font_awesome_flutter/lib/fonts/fa-solid-900.ttf": "d989a3dc694aab39b12ddea092809182",
"assets/packages/font_awesome_flutter/lib/fonts/fa-regular-400.ttf": "ea1e726a1e11e2d8f98283c2c8e6bbde",
"assets/packages/font_awesome_flutter/lib/fonts/fa-brands-400.ttf": "f25e8e701660fb45e2a81ff3f43c6d5c",
"assets/shaders/ink_sparkle.frag": "4096b5150bac93c41cbc9b45276bd90f",
"assets/AssetManifest.bin": "c5841bf938afde3a2f4d7301b0ed6b70",
"assets/fonts/MaterialIcons-Regular.otf": "a8dd7636e5960da44d96e3aaaeaef10d",
"assets/assets/images/tab_fav_inactive.png": "1afe7a0859568d0c5aa6c8ee7e08c514",
"assets/assets/images/rabbit.png": "f178ff019b2f84f83c8ae4115611c0a0",
"assets/assets/images/tab_more_active.png": "f087e093dfd559f616eee15826dbdbe9",
"assets/assets/images/name_logo_red.png": "5fb7b26c8c4fe2376ecee55d6896ac2e",
"assets/assets/images/tab_sell_inactive.png": "d36e982ee48b3aa64c965ea173e957a9",
"assets/assets/images/contact_detail.png": "ead83089ea34aec21b03cc15f11455dd",
"assets/assets/images/tab_search_active.png": "f5cf6b35d2b32fd93f5617b8962c5f8c",
"assets/assets/images/onboard_map.png": "d10360c8ff6e91310b37e7a137482536",
"assets/assets/images/tab_fav_active.png": "68e64380a7cecc870adb79dedde360ca",
"assets/assets/images/check_active.png": "8af8530dbb80610d0cf05c5ee30b8c1e",
"assets/assets/images/tab_search_inactive.png": "7b21ab6a76bf4675162e24b9b85bed8f",
"assets/assets/images/confirm_detail.png": "5ebbafca98aabfdd1bad5cacc26bcc5c",
"assets/assets/images/tab_more_inactive_old.png": "6747354cc4d6002c2e6df5e8fca22849",
"assets/assets/images/search.png": "8a4c0021d5f01f886ff308f0952f712d",
"assets/assets/images/onboard_black.png": "00f2ca53ffc7b48212717b1bb415313d",
"assets/assets/images/filter.png": "9bec565079b8cb97885788e29ccb9ae4",
"assets/assets/images/selling_detail.png": "13329eb303d28f8b13112b4a367b5a53",
"assets/assets/images/tab_sell_active.png": "be92808e50dc621165cff03f93b814cb",
"assets/assets/images/tab_more_active_old.png": "c6704bf61c593a132f1b39ef84ae6e20",
"assets/assets/images/onboard_red.png": "0b5349fe541c78dd558884ca83a7cf89",
"assets/assets/images/tab_more_inactive.png": "63a213a0c8c8b8c770d2cdb8c0774815",
"assets/assets/images/placeholder_logo.png": "eee7564901bcf9c5ad5edc904ecabab5",
"assets/assets/images/splash_logo.png": "2ee25dc8ff8eb6140b9ebea20dd75c77",
"assets/assets/images/car_detail.png": "e83e35c3e247645c9f6def413144e6a7",
"assets/assets/images/check_inactive.png": "d2c54edb125a6d294604894655a1ec68",
"assets/assets/images/photo_detail.png": "08fe64bdfac097ade2d3f7e5192a0c8f",
"assets/assets/images/onboard_blue.png": "e6bf379751100f9593e5192f8dc1c29b",
"assets/assets/fonts/Rubik-Light.ttf": "86699cab89559b6f5ffd4887cb5c7a7c",
"assets/assets/fonts/Rubik-Medium.ttf": "e785acbf5775e9bec2129f4967a75472",
"assets/assets/fonts/Rubik-Italic.ttf": "17538a8196fb1d1fab888c5941acf9ec",
"assets/assets/fonts/Rubik-LightItalic.ttf": "ac5353ac12658ccfd7eca99a25be7037",
"assets/assets/fonts/Rubik-Regular.ttf": "46df28800514364ef2766f74386b1bd3",
"canvaskit/skwasm.js": "87063acf45c5e1ab9565dcf06b0c18b8",
"canvaskit/skwasm.wasm": "4124c42a73efa7eb886d3400a1ed7a06",
"canvaskit/chromium/canvaskit.js": "0ae8bbcc58155679458a0f7a00f66873",
"canvaskit/chromium/canvaskit.wasm": "f87e541501c96012c252942b6b75d1ea",
"canvaskit/canvaskit.js": "eb8797020acdbdf96a12fb0405582c1b",
"canvaskit/canvaskit.wasm": "64edb91684bdb3b879812ba2e48dd487",
"canvaskit/skwasm.worker.js": "bfb704a6c714a75da9ef320991e88b03"};
// The application shell files that are downloaded before a service worker can
// start.
const CORE = ["main.dart.js",
"index.html",
"assets/AssetManifest.json",
"assets/FontManifest.json"];

// During install, the TEMP cache is populated with the application shell files.
self.addEventListener("install", (event) => {
  self.skipWaiting();
  return event.waitUntil(
    caches.open(TEMP).then((cache) => {
      return cache.addAll(
        CORE.map((value) => new Request(value, {'cache': 'reload'})));
    })
  );
});
// During activate, the cache is populated with the temp files downloaded in
// install. If this service worker is upgrading from one with a saved
// MANIFEST, then use this to retain unchanged resource files.
self.addEventListener("activate", function(event) {
  return event.waitUntil(async function() {
    try {
      var contentCache = await caches.open(CACHE_NAME);
      var tempCache = await caches.open(TEMP);
      var manifestCache = await caches.open(MANIFEST);
      var manifest = await manifestCache.match('manifest');
      // When there is no prior manifest, clear the entire cache.
      if (!manifest) {
        await caches.delete(CACHE_NAME);
        contentCache = await caches.open(CACHE_NAME);
        for (var request of await tempCache.keys()) {
          var response = await tempCache.match(request);
          await contentCache.put(request, response);
        }
        await caches.delete(TEMP);
        // Save the manifest to make future upgrades efficient.
        await manifestCache.put('manifest', new Response(JSON.stringify(RESOURCES)));
        // Claim client to enable caching on first launch
        self.clients.claim();
        return;
      }
      var oldManifest = await manifest.json();
      var origin = self.location.origin;
      for (var request of await contentCache.keys()) {
        var key = request.url.substring(origin.length + 1);
        if (key == "") {
          key = "/";
        }
        // If a resource from the old manifest is not in the new cache, or if
        // the MD5 sum has changed, delete it. Otherwise the resource is left
        // in the cache and can be reused by the new service worker.
        if (!RESOURCES[key] || RESOURCES[key] != oldManifest[key]) {
          await contentCache.delete(request);
        }
      }
      // Populate the cache with the app shell TEMP files, potentially overwriting
      // cache files preserved above.
      for (var request of await tempCache.keys()) {
        var response = await tempCache.match(request);
        await contentCache.put(request, response);
      }
      await caches.delete(TEMP);
      // Save the manifest to make future upgrades efficient.
      await manifestCache.put('manifest', new Response(JSON.stringify(RESOURCES)));
      // Claim client to enable caching on first launch
      self.clients.claim();
      return;
    } catch (err) {
      // On an unhandled exception the state of the cache cannot be guaranteed.
      console.error('Failed to upgrade service worker: ' + err);
      await caches.delete(CACHE_NAME);
      await caches.delete(TEMP);
      await caches.delete(MANIFEST);
    }
  }());
});
// The fetch handler redirects requests for RESOURCE files to the service
// worker cache.
self.addEventListener("fetch", (event) => {
  if (event.request.method !== 'GET') {
    return;
  }
  var origin = self.location.origin;
  var key = event.request.url.substring(origin.length + 1);
  // Redirect URLs to the index.html
  if (key.indexOf('?v=') != -1) {
    key = key.split('?v=')[0];
  }
  if (event.request.url == origin || event.request.url.startsWith(origin + '/#') || key == '') {
    key = '/';
  }
  // If the URL is not the RESOURCE list then return to signal that the
  // browser should take over.
  if (!RESOURCES[key]) {
    return;
  }
  // If the URL is the index.html, perform an online-first request.
  if (key == '/') {
    return onlineFirst(event);
  }
  event.respondWith(caches.open(CACHE_NAME)
    .then((cache) =>  {
      return cache.match(event.request).then((response) => {
        // Either respond with the cached resource, or perform a fetch and
        // lazily populate the cache only if the resource was successfully fetched.
        return response || fetch(event.request).then((response) => {
          if (response && Boolean(response.ok)) {
            cache.put(event.request, response.clone());
          }
          return response;
        });
      })
    })
  );
});
self.addEventListener('message', (event) => {
  // SkipWaiting can be used to immediately activate a waiting service worker.
  // This will also require a page refresh triggered by the main worker.
  if (event.data === 'skipWaiting') {
    self.skipWaiting();
    return;
  }
  if (event.data === 'downloadOffline') {
    downloadOffline();
    return;
  }
});
// Download offline will check the RESOURCES for all files not in the cache
// and populate them.
async function downloadOffline() {
  var resources = [];
  var contentCache = await caches.open(CACHE_NAME);
  var currentContent = {};
  for (var request of await contentCache.keys()) {
    var key = request.url.substring(origin.length + 1);
    if (key == "") {
      key = "/";
    }
    currentContent[key] = true;
  }
  for (var resourceKey of Object.keys(RESOURCES)) {
    if (!currentContent[resourceKey]) {
      resources.push(resourceKey);
    }
  }
  return contentCache.addAll(resources);
}
// Attempt to download the resource online before falling back to
// the offline cache.
function onlineFirst(event) {
  return event.respondWith(
    fetch(event.request).then((response) => {
      return caches.open(CACHE_NAME).then((cache) => {
        cache.put(event.request, response.clone());
        return response;
      });
    }).catch((error) => {
      return caches.open(CACHE_NAME).then((cache) => {
        return cache.match(event.request).then((response) => {
          if (response != null) {
            return response;
          }
          throw error;
        });
      });
    })
  );
}
