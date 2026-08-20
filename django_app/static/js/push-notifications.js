/**
 * SRM Valliammai Engineering College - CSE Department Portal
 * Student Web Push Notifications Client Controller
 */

(function () {
    'use strict';

    // Helper: Convert urlSafe base64 to Uint8Array for PushManager
    function urlBase64ToUint8Array(base64String) {
        const padding = '='.repeat((4 - (base64String.length % 4)) % 4);
        const base64 = (base64String + padding).replace(/\-/g, '+').replace(/_/g, '/');
        const rawData = window.atob(base64);
        const outputArray = new Uint8Array(rawData.length);
        for (let i = 0; i < rawData.length; ++i) {
            outputArray[i] = rawData.charCodeAt(i);
        }
        return outputArray;
    }

    // Helper: CSRF Cookie Reader
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    class PushNotificationManager {
        constructor() {
            this.isSupported = ('serviceWorker' in navigator) && ('PushManager' in window) && ('Notification' in window);
            this.swRegistration = null;
            this.isSubscribed = false;
            this.vapidPublicKey = null;
        }

        async init() {
            if (!this.isSupported) {
                console.log('[PushNotifications] Web Push is not supported in this browser.');
                return;
            }

            try {
                // Register service worker
                this.swRegistration = await navigator.serviceWorker.register('/sw.js', { scope: '/' });
                console.log('[PushNotifications] Service Worker registered with scope:', this.swRegistration.scope);

                // Check existing subscription
                const subscription = await this.swRegistration.pushManager.getSubscription();
                this.isSubscribed = !(subscription === null);

                // Initialize floating UI prompt
                this.initUI();
            } catch (err) {
                console.warn('[PushNotifications] Init error:', err);
            }
        }

        async getVapidPublicKey() {
            if (this.vapidPublicKey) return this.vapidPublicKey;
            try {
                const response = await fetch('/news/api/push/vapid-key/');
                const data = await response.json();
                this.vapidPublicKey = data.publicKey;
                return this.vapidPublicKey;
            } catch (err) {
                console.error('[PushNotifications] Failed to fetch VAPID key:', err);
                return null;
            }
        }

        async subscribe(categoryFilter = 'all') {
            try {
                const permission = await Notification.requestPermission();
                if (permission !== 'granted') {
                    this.showToast('Notification permission was not granted.', 'warning');
                    return false;
                }

                const publicKey = await this.getVapidPublicKey();
                if (!publicKey) {
                    this.showToast('Failed to retrieve notification security key.', 'danger');
                    return false;
                }

                const convertedKey = urlBase64ToUint8Array(publicKey);
                const subscription = await this.swRegistration.pushManager.subscribe({
                    userVisibleOnly: true,
                    applicationServerKey: convertedKey
                });

                const subJson = subscription.toJSON();
                const payload = {
                    endpoint: subJson.endpoint,
                    keys: {
                        p256dh: subJson.keys.p256dh,
                        auth: subJson.keys.auth
                    },
                    category_filter: categoryFilter
                };

                const res = await fetch('/news/api/push/subscribe/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken') || ''
                    },
                    body: JSON.stringify(payload)
                });

                if (res.ok) {
                    this.isSubscribed = true;
                    this.updateUI();
                    this.showToast('🎉 Phone notifications active! You\'ll receive instant alerts for circulars & news.', 'success');
                    return true;
                } else {
                    throw new Error('Server subscription failed');
                }
            } catch (err) {
                console.error('[PushNotifications] Subscribe failed:', err);
                this.showToast('Could not enable notifications. Please check browser settings.', 'danger');
                return false;
            }
        }

        async unsubscribe() {
            try {
                const subscription = await this.swRegistration.pushManager.getSubscription();
                if (subscription) {
                    const endpoint = subscription.endpoint;
                    await subscription.unsubscribe();
                    await fetch('/news/api/push/unsubscribe/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCookie('csrftoken') || ''
                        },
                        body: JSON.stringify({ endpoint })
                    });
                }
                this.isSubscribed = false;
                this.updateUI();
                this.showToast('Push notifications turned off.', 'info');
            } catch (err) {
                console.error('[PushNotifications] Unsubscribe error:', err);
            }
        }

        initUI() {
            // Check if user has already dismissed prompt in this session
            const isDismissed = sessionStorage.getItem('push_prompt_dismissed') === 'true';

            // Create Floating Bell Widget
            const widgetHtml = `
                <div id="pushNotificationWidget" class="push-notification-widget">
                    <!-- Interactive Notification Banner (Floats above the bell button) -->
                    <div id="pushPromptCard" class="push-prompt-card ${(!this.isSubscribed && !isDismissed && Notification.permission !== 'denied') ? '' : 'd-none'}">
                        <div class="d-flex align-items-center justify-content-between mb-1">
                            <div class="d-flex align-items-center gap-2">
                                <div class="push-icon-badge">
                                    <i class="fa-solid fa-bell fa-sm"></i>
                                </div>
                                <div>
                                    <h6 class="fw-bold mb-0 text-dark" style="font-size: 0.95rem;">Instant Phone Alerts</h6>
                                    <span class="text-muted" style="font-size: 0.72rem;">SRM Valliammai CSE</span>
                                </div>
                            </div>
                            <button id="closePushPrompt" type="button" class="btn-close" style="font-size: 0.72rem;" aria-label="Close"></button>
                        </div>
                        
                        <p class="push-prompt-body">
                            Get instant notifications on your phone for urgent circulars, exam dates, and placement announcements.
                        </p>

                        <div class="d-flex align-items-center gap-2">
                            <button id="enablePushBtn" class="btn push-action-btn-primary rounded-pill flex-grow-1 fw-semibold d-flex align-items-center justify-content-center gap-1.5">
                                <i class="fa-solid fa-bell"></i> Enable Alerts
                            </button>
                            <button id="dismissPushBtn" class="btn push-action-btn-secondary rounded-pill px-3 fw-medium">
                                Later
                            </button>
                        </div>
                    </div>

                    <!-- Floating Bell Button -->
                    <button id="pushBellBtn" class="btn btn-primary push-bell-btn position-relative" title="Department Phone Notifications">
                        <i class="fa-solid fa-bell fa-lg"></i>
                        <span id="pushActiveBadge" class="position-absolute top-0 start-100 translate-middle p-1.5 bg-success border border-2 border-white rounded-circle ${this.isSubscribed ? '' : 'd-none'}">
                            <span class="visually-hidden">Active</span>
                        </span>
                    </button>
                </div>
            `;

            document.body.insertAdjacentHTML('beforeend', widgetHtml);

            // Bind UI Events
            const bellBtn = document.getElementById('pushBellBtn');
            const promptCard = document.getElementById('pushPromptCard');
            const enableBtn = document.getElementById('enablePushBtn');
            const dismissBtn = document.getElementById('dismissPushBtn');
            const closeBtn = document.getElementById('closePushPrompt');

            if (bellBtn) {
                bellBtn.addEventListener('click', () => {
                    if (this.isSubscribed) {
                        if (confirm('You are currently receiving push notifications for department bulletins. Would you like to unsubscribe?')) {
                            this.unsubscribe();
                        }
                    } else {
                        if (promptCard.classList.contains('d-none')) {
                            promptCard.classList.remove('d-none');
                        } else {
                            promptCard.classList.add('d-none');
                        }
                    }
                });
            }

            if (enableBtn) {
                enableBtn.addEventListener('click', async () => {
                    enableBtn.disabled = true;
                    enableBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span> Enabling...';
                    const success = await this.subscribe('all');
                    enableBtn.disabled = false;
                    enableBtn.innerHTML = '<i class="fa-solid fa-bell me-1"></i> Enable Alerts';
                    if (success && promptCard) {
                        promptCard.classList.add('d-none');
                    }
                });
            }

            const hidePrompt = () => {
                if (promptCard) promptCard.classList.add('d-none');
                sessionStorage.setItem('push_prompt_dismissed', 'true');
            };

            if (dismissBtn) dismissBtn.addEventListener('click', hidePrompt);
            if (closeBtn) closeBtn.addEventListener('click', hidePrompt);

            this.updateUI();
        }

        updateUI() {
            const bellBtn = document.getElementById('pushBellBtn');
            const activeBadge = document.getElementById('pushActiveBadge');
            const promptCard = document.getElementById('pushPromptCard');

            if (activeBadge) {
                if (this.isSubscribed) {
                    activeBadge.classList.remove('d-none');
                } else {
                    activeBadge.classList.add('d-none');
                }
            }

            if (bellBtn) {
                if (this.isSubscribed) {
                    bellBtn.classList.remove('btn-primary');
                    bellBtn.classList.add('btn-success');
                    bellBtn.setAttribute('title', '🔔 Push Notifications Active (Click to Manage)');
                } else {
                    bellBtn.classList.remove('btn-success');
                    bellBtn.classList.add('btn-primary');
                    bellBtn.setAttribute('title', '🔔 Enable Department Phone Notifications');
                }
            }

            if (this.isSubscribed && promptCard) {
                promptCard.classList.add('d-none');
            }
        }

        showToast(message, type = 'info') {
            const toastContainer = document.querySelector('.toast-container') || (() => {
                const c = document.createElement('div');
                c.className = 'toast-container position-fixed bottom-0 start-50 translate-middle-x p-3';
                c.style.zIndex = '1090';
                document.body.appendChild(c);
                return c;
            })();

            const toastId = 'toast_' + Date.now();
            const toastHtml = `
                <div id="${toastId}" class="toast align-items-center text-bg-${type} border-0 shadow-lg show" role="alert" aria-live="assertive" aria-atomic="true">
                    <div class="d-flex">
                        <div class="toast-body small fw-medium">
                            ${message}
                        </div>
                        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                    </div>
                </div>
            `;

            toastContainer.insertAdjacentHTML('beforeend', toastHtml);
            const el = document.getElementById(toastId);
            setTimeout(() => {
                if (el && el.parentNode) el.parentNode.removeChild(el);
            }, 5000);
        }
    }

    // Auto-initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            window.csePushManager = new PushNotificationManager();
            window.csePushManager.init();
        });
    } else {
        window.csePushManager = new PushNotificationManager();
        window.csePushManager.init();
    }
})();
