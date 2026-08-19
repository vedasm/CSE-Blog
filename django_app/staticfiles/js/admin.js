(function () {
    'use strict';

    function initSidebarToggle() {
        const sidebar = document.getElementById('adminSidebar');
        const overlay = document.getElementById('adminOverlay');
        const toggleBtn = document.getElementById('adminMenuToggle');

        if (!sidebar || !overlay || !toggleBtn) {
            return;
        }

        function closeSidebar() {
            sidebar.classList.remove('show');
            overlay.classList.remove('show');
            toggleBtn.setAttribute('aria-expanded', 'false');
            sidebar.setAttribute('aria-hidden', 'true');
            document.body.classList.remove('admin-lock-scroll');
        }

        function openSidebar() {
            sidebar.classList.add('show');
            overlay.classList.add('show');
            toggleBtn.setAttribute('aria-expanded', 'true');
            sidebar.setAttribute('aria-hidden', 'false');
            document.body.classList.add('admin-lock-scroll');
        }

        toggleBtn.addEventListener('click', function () {
            if (sidebar.classList.contains('show')) {
                closeSidebar();
            } else {
                openSidebar();
            }
        });

        overlay.addEventListener('click', closeSidebar);

        window.addEventListener('keydown', function (event) {
            if (event.key === 'Escape') {
                closeSidebar();
            }
        });

        sidebar.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                if (window.innerWidth <= 992) {
                    closeSidebar();
                }
            });
        });

        window.addEventListener('resize', function () {
            if (window.innerWidth > 992) {
                closeSidebar();
                sidebar.setAttribute('aria-hidden', 'false');
                document.body.classList.remove('admin-lock-scroll');
            }
        }, { passive: true });
    }

    function initConfirmDialogs() {
        document.addEventListener('submit', function (event) {
            const form = event.target;
            if (!(form instanceof HTMLFormElement)) {
                return;
            }

            const message = form.getAttribute('data-confirm');
            if (!message) {
                return;
            }

            if (!window.confirm(message)) {
                event.preventDefault();
            }
        });
    }

    function initBlogFormHelpers() {
        const title = document.getElementById('id_title');
        const slug = document.getElementById('id_slug');
        const image = document.getElementById('id_featured_image');
        const preview = document.getElementById('image-preview');

        if (title && slug) {
            title.addEventListener('input', function () {
                slug.value = title.value
                    .toLowerCase()
                    .trim()
                    .replace(/[^a-z0-9]+/g, '-')
                    .replace(/^-|-$/g, '');
            });
        }

        if (image && preview) {
            image.addEventListener('change', function () {
                const file = image.files && image.files[0];
                if (!file) {
                    return;
                }

                preview.src = URL.createObjectURL(file);
                preview.classList.remove('d-none');

                const currentImg = document.getElementById('current-image');
                if (currentImg) {
                    currentImg.classList.add('d-none');
                }
            });
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        initSidebarToggle();
        initConfirmDialogs();
        initBlogFormHelpers();
    });
})();
