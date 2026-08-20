/**
 * SRM Valliammai Engineering College - CSE Department Portal
 * Service Worker for Native Web Push Notifications
 */

self.addEventListener('install', (event) => {
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(self.clients.claim());
});

self.addEventListener('push', (event) => {
    let data = {};
    if (event.data) {
        try {
            data = event.data.json();
        } catch (e) {
            data = { title: 'CSE Department Bulletin', body: event.data.text() };
        }
    }

    const title = data.title || '📢 CSE Department Bulletin';
    const targetUrl = (data.data && data.data.url) || data.url || '/news/';

    const options = {
        body: data.body || 'A new official department circular or news bulletin has been published.',
        icon: data.icon || '/static/images/brand-icon.png',
        badge: data.badge || '/static/images/badge-icon.png',
        vibrate: [200, 100, 200, 100, 200],
        tag: data.tag || 'cse-news-bulletin',
        renotify: true,
        requireInteraction: Boolean(data.requireInteraction),
        data: {
            url: targetUrl,
            timestamp: Date.now()
        },
        actions: [
            {
                action: 'view_bulletin',
                title: '📖 View Bulletin'
            },
            {
                action: 'dismiss',
                title: 'Dismiss'
            }
        ]
    };

    event.waitUntil(
        self.registration.showNotification(title, options)
    );
});

self.addEventListener('notificationclick', (event) => {
    event.notification.close();

    if (event.action === 'dismiss') {
        return;
    }

    const targetUrl = (event.notification.data && event.notification.data.url) || '/news/';

    event.waitUntil(
        clients.matchAll({ type: 'window', includeUncontrolled: true }).then((windowClients) => {
            // If tab is already open, focus it and navigate
            for (let i = 0; i < windowClients.length; i++) {
                const client = windowClients[i];
                if ('focus' in client) {
                    client.navigate(targetUrl);
                    return client.focus();
                }
            }
            // Otherwise open a new window
            if (clients.openWindow) {
                return clients.openWindow(targetUrl);
            }
        })
    );
});
