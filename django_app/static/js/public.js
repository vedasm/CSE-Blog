(function () {
    'use strict';

    // -------------------------------------------------------------
    // 1. Contact Form Validation
    // -------------------------------------------------------------
    function initContactFormValidation() {
        const form = document.querySelector('form[data-contact-form]');
        if (!form) return;

        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                form.classList.add('was-validated');
            }
        });
    }

    // -------------------------------------------------------------
    // 2. News Board Live Filter & Quick Search
    // -------------------------------------------------------------
    function initNewsBoardFilter() {
        const filterBar = document.getElementById('newsFilterBar');
        const searchInput = document.getElementById('newsWidgetSearch');
        const feedList = document.getElementById('newsFeedList');
        const emptyMsg = document.getElementById('newsFilterEmptyMsg');

        if (!feedList) return;

        const items = feedList.querySelectorAll('.news-feed-item');
        let currentCategory = 'all';
        let currentSearch = '';

        function applyFilter() {
            let visibleCount = 0;
            const searchLower = currentSearch.toLowerCase().trim();

            items.forEach(function (item) {
                const itemCategory = item.getAttribute('data-category') || '';
                const isPinned = item.getAttribute('data-pinned') === 'true';
                const title = (item.getAttribute('data-title') || '').toLowerCase();
                const summary = (item.getAttribute('data-summary') || '').toLowerCase();

                let categoryMatch = false;
                if (currentCategory === 'all') {
                    categoryMatch = true;
                } else if (currentCategory === 'urgent') {
                    categoryMatch = isPinned;
                } else {
                    categoryMatch = (itemCategory === currentCategory);
                }

                let searchMatch = true;
                if (searchLower) {
                    searchMatch = title.includes(searchLower) || summary.includes(searchLower);
                }

                if (categoryMatch && searchMatch) {
                    item.style.display = 'block';
                    visibleCount++;
                } else {
                    item.style.display = 'none';
                }
            });

            if (emptyMsg) {
                if (visibleCount === 0 && items.length > 0) {
                    emptyMsg.classList.remove('d-none');
                } else {
                    emptyMsg.classList.add('d-none');
                }
            }
        }

        if (filterBar) {
            const tabs = filterBar.querySelectorAll('.news-tab-pill');
            tabs.forEach(function (tab) {
                tab.addEventListener('click', function () {
                    tabs.forEach(t => t.classList.remove('active'));
                    tab.classList.add('active');
                    currentCategory = tab.getAttribute('data-category') || 'all';
                    applyFilter();
                });
            });
        }

        if (searchInput) {
            searchInput.addEventListener('input', function () {
                currentSearch = searchInput.value;
                applyFilter();
            });
        }
    }

    // -------------------------------------------------------------
    // 3. News Quick-View Fluid Modal
    // -------------------------------------------------------------
    function initNewsQuickModal() {
        const modalEl = document.getElementById('newsQuickModal');
        if (!modalEl) return;

        const modal = new bootstrap.Modal(modalEl);
        const titleEl = document.getElementById('newsQuickModalLabel');
        const categoryEl = document.getElementById('modalCategory');
        const urgentBadge = document.getElementById('modalUrgentBadge');
        const dateEl = document.getElementById('modalDate');
        const summaryEl = document.getElementById('modalSummary');
        const contentEl = document.getElementById('modalContent');
        const attachmentBtn = document.getElementById('modalAttachmentBtn');
        const linkBtn = document.getElementById('modalLinkBtn');
        const detailBtn = document.getElementById('modalDetailBtn');

        document.addEventListener('click', function (e) {
            const trigger = e.target.closest('.news-modal-trigger, .news-feed-item');
            // If click was on a direct external link or PDF download, let default link action occur
            if (e.target.closest('a') && !e.target.closest('.news-modal-trigger')) {
                return;
            }
            if (!trigger) return;

            const item = trigger.closest('.news-feed-item');
            if (!item) return;

            const title = item.getAttribute('data-news-title') || '';
            const category = item.getAttribute('data-news-category') || 'Announcement';
            const content = item.getAttribute('data-news-content') || '';
            const summary = item.getAttribute('data-news-summary') || '';
            const date = item.getAttribute('data-news-date') || '';
            const isUrgent = item.getAttribute('data-news-urgent') === 'true';
            const attachment = item.getAttribute('data-news-attachment') || '';
            const link = item.getAttribute('data-news-link') || '';
            const url = item.getAttribute('data-news-url') || '#';

            if (titleEl) titleEl.textContent = title;
            if (categoryEl) categoryEl.textContent = category;
            if (dateEl) dateEl.textContent = date;
            if (contentEl) contentEl.textContent = content;

            if (urgentBadge) {
                if (isUrgent) urgentBadge.classList.remove('d-none');
                else urgentBadge.classList.add('d-none');
            }

            if (summaryEl) {
                if (summary && summary !== content.slice(0, 200)) {
                    summaryEl.textContent = summary;
                    summaryEl.classList.remove('d-none');
                } else {
                    summaryEl.classList.add('d-none');
                }
            }

            if (attachmentBtn) {
                if (attachment) {
                    attachmentBtn.href = attachment;
                    attachmentBtn.classList.remove('d-none');
                } else {
                    attachmentBtn.classList.add('d-none');
                }
            }

            if (linkBtn) {
                if (link) {
                    linkBtn.href = link;
                    linkBtn.classList.remove('d-none');
                } else {
                    linkBtn.classList.add('d-none');
                }
            }

            if (detailBtn) {
                detailBtn.href = url;
            }

            modal.show();
        });
    }

    // -------------------------------------------------------------
    // 4. Animated Achievements Number Counter (IntersectionObserver)
    // -------------------------------------------------------------
    function initAchievementCounters() {
        const counters = document.querySelectorAll('.counter-number');
        if (!counters.length) return;

        let hasAnimated = false;

        function animateCount(el) {
            const target = parseInt(el.getAttribute('data-target'), 10) || 0;
            const duration = 1800; // ms
            const frameDuration = 1000 / 60;
            const totalFrames = Math.round(duration / frameDuration);
            let frame = 0;

            const timer = setInterval(() => {
                frame++;
                // easeOutQuad
                const progress = frame / totalFrames;
                const easeProgress = 1 - (1 - progress) * (1 - progress);
                const current = Math.round(target * easeProgress);

                el.textContent = current;

                if (frame === totalFrames) {
                    clearInterval(timer);
                    el.textContent = target;
                }
            }, frameDuration);
        }

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !hasAnimated) {
                    hasAnimated = true;
                    counters.forEach(counter => animateCount(counter));
                }
            });
        }, { threshold: 0.25 });

        const section = document.querySelector('.achievements-section');
        if (section) {
            observer.observe(section);
        }
    }

    // -------------------------------------------------------------
    // 5. Share Button URL Copy
    // -------------------------------------------------------------
    function initShareButton() {
        const shareBtn = document.getElementById('copyShareBtn');
        if (!shareBtn) return;

        shareBtn.addEventListener('click', function () {
            const url = shareBtn.getAttribute('data-url') || window.location.href;
            if (navigator.clipboard && window.isSecureContext) {
                navigator.clipboard.writeText(url).then(() => {
                    const originalHtml = shareBtn.innerHTML;
                    shareBtn.innerHTML = '<i class="fa-solid fa-check me-2 text-success"></i> Link Copied!';
                    setTimeout(() => {
                        shareBtn.innerHTML = originalHtml;
                    }, 2500);
                });
            } else {
                prompt('Copy link to circular / article:', url);
            }
        });
    }

    // -------------------------------------------------------------
    // 6. Hero Canvas Particle & Code Animation
    // -------------------------------------------------------------
    function initHomeHeroEffects() {
        const heroBg = document.getElementById('heroBg');
        const canvas = document.getElementById('heroCanvas');

        if (!heroBg && !canvas) return;

        let scrollTicking = false;
        function applyParallax() {
            if (heroBg) {
                heroBg.style.transform = 'translateY(' + (window.pageYOffset * 0.25) + 'px)';
            }
            scrollTicking = false;
        }

        window.addEventListener('scroll', function () {
            if (!scrollTicking) {
                scrollTicking = true;
                requestAnimationFrame(applyParallax);
            }
        }, { passive: true });
        applyParallax();

        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        let width = 0;
        let height = 0;
        let frameCount = 0;
        const nodes = [];
        const codeElements = [];

        const config = {
            nodeCount: window.innerWidth < 768 ? 25 : 50,
            connectionDist: window.innerWidth < 768 ? 90 : 130,
            codeSnippets: ['</>', '{ }', '0101', 'async/await', 'fn()', 'AI::train()', 'O(log N)', 'SQL::SELECT', 'torch.cuda', 'git push'],
            colors: {
                node: 'rgba(96, 133, 247, 0.45)',
                line: 'rgba(96, 133, 247, ',
                binary: 'rgba(248, 250, 252, 0.08)'
            }
        };

        function resize() {
            width = canvas.width = canvas.offsetWidth;
            height = canvas.height = canvas.offsetHeight;
        }

        class Node {
            constructor() {
                this.x = Math.random() * width;
                this.y = Math.random() * height;
                this.vx = (Math.random() - 0.5) * 0.4;
                this.vy = (Math.random() - 0.5) * 0.4;
                this.radius = Math.random() * 2 + 1;
            }

            update() {
                this.x += this.vx;
                this.y += this.vy;
                if (this.x < 0) this.x = width;
                if (this.x > width) this.x = 0;
                if (this.y < 0) this.y = height;
                if (this.y > height) this.y = 0;
            }

            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                ctx.fillStyle = config.colors.node;
                ctx.fill();
            }
        }

        class CodeElement {
            constructor() {
                this.init();
            }

            init() {
                this.text = config.codeSnippets[Math.floor(Math.random() * config.codeSnippets.length)];
                this.x = Math.random() * width;
                this.y = Math.random() * height;
                this.z = Math.random() * 0.5 + 0.5;
                this.opacity = 0;
                this.fadeSpeed = Math.random() * 0.008 + 0.004;
                this.state = 'fade-in';
                this.vx = (Math.random() - 0.5) * 0.2 * this.z;
                this.vy = (Math.random() - 0.5) * 0.2 * this.z;
            }

            update() {
                this.x += this.vx;
                this.y += this.vy;

                if (this.state === 'fade-in') {
                    this.opacity += this.fadeSpeed;
                    if (this.opacity >= 0.35) this.state = 'float';
                } else if (this.state === 'fade-out') {
                    this.opacity -= this.fadeSpeed;
                    if (this.opacity <= 0) this.init();
                }

                if (Math.random() > 0.994) this.state = 'fade-out';
            }

            draw() {
                ctx.font = (11 * this.z) + 'px monospace';
                ctx.fillStyle = 'rgba(224, 231, 255, ' + this.opacity + ')';
                ctx.fillText(this.text, this.x, this.y);
            }
        }

        function drawNetwork() {
            for (let i = 0; i < nodes.length; i++) {
                for (let j = i + 1; j < nodes.length; j++) {
                    const dx = nodes[i].x - nodes[j].x;
                    const dy = nodes[i].y - nodes[j].y;
                    const dist = Math.sqrt((dx * dx) + (dy * dy));

                    if (dist < config.connectionDist) {
                        ctx.beginPath();
                        ctx.moveTo(nodes[i].x, nodes[i].y);
                        ctx.lineTo(nodes[j].x, nodes[j].y);
                        ctx.strokeStyle = config.colors.line + (0.35 * (1 - (dist / config.connectionDist))) + ')';
                        ctx.lineWidth = 0.6;
                        ctx.stroke();
                    }
                }
            }
        }

        function animate() {
            requestAnimationFrame(animate);

            if (document.hidden || reduceMotion) return;

            ctx.clearRect(0, 0, width, height);

            nodes.forEach(node => {
                node.update();
                node.draw();
            });

            drawNetwork();

            codeElements.forEach(code => {
                code.update();
                code.draw();
            });

            frameCount++;
        }

        window.addEventListener('resize', resize, { passive: true });
        resize();

        for (let i = 0; i < config.nodeCount; i++) {
            nodes.push(new Node());
        }
        for (let i = 0; i < 10; i++) {
            codeElements.push(new CodeElement());
        }
        animate();
    }

    // -------------------------------------------------------------
    // 7. Interactive Academic & Department Calendar System
    // -------------------------------------------------------------
    function setupCalendarInstance(config) {
        const monthYearEl = document.getElementById(config.monthYearId);
        const daysGridEl = document.getElementById(config.daysGridId);
        const prevBtn = document.getElementById(config.prevBtnId);
        const nextBtn = document.getElementById(config.nextBtnId);
        const todayBtn = document.getElementById(config.todayBtnId);
        const filterBar = document.getElementById(config.filterBarId);
        const scheduleListEl = document.getElementById(config.scheduleListId);
        const selectedDateTitle = document.getElementById(config.selectedDateTitleId);
        const selectedDateSubtitle = document.getElementById(config.selectedDateSubtitleId);
        const eventsCountEl = document.getElementById(config.eventsCountId);

        if (!daysGridEl || !monthYearEl) return;

        const monthNames = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ];

        const today = new Date();
        let viewDate = new Date();
        let selectedDateStr = formatDateStr(today.getFullYear(), today.getMonth() + 1, today.getDate());
        let currentCategory = 'all';
        let cachedSchedules = [];
        let isFetching = false;

        function padZero(n) {
            return n < 10 ? '0' + n : '' + n;
        }

        function formatDateStr(y, m, d) {
            return `${y}-${padZero(m)}-${padZero(d)}`;
        }

        function formatDisplayDate(dateStr) {
            const parts = dateStr.split('-');
            if (parts.length !== 3) return dateStr;
            const d = new Date(parseInt(parts[0]), parseInt(parts[1]) - 1, parseInt(parts[2]));
            return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
        }

        function fetchSchedulesAndRender() {
            if (isFetching) return;
            isFetching = true;

            const year = viewDate.getFullYear();
            const month = viewDate.getMonth() + 1;

            let url = `/events/api/calendar/?year=${year}&month=${month}`;
            if (currentCategory && currentCategory !== 'all') {
                url += `&category=${encodeURIComponent(currentCategory)}`;
            }

            fetch(url)
                .then(resp => resp.json())
                .then(data => {
                    isFetching = false;
                    if (data && data.status === 'success') {
                        cachedSchedules = data.schedules || [];
                    } else {
                        cachedSchedules = [];
                    }
                    renderCalendar();
                    renderDaySchedules(selectedDateStr);
                })
                .catch(err => {
                    isFetching = false;
                    console.error('Failed to load calendar events:', err);
                    renderCalendar();
                    renderDaySchedules(selectedDateStr);
                });
        }

        function isDateInRange(dateStr, startDateStr, endDateStr) {
            if (!endDateStr) {
                return dateStr === startDateStr;
            }
            return dateStr >= startDateStr && dateStr <= endDateStr;
        }

        function renderCalendar() {
            const year = viewDate.getFullYear();
            const month = viewDate.getMonth();

            monthYearEl.textContent = `${monthNames[month]} ${year}`;

            daysGridEl.innerHTML = '';

            const firstDayIndex = new Date(year, month, 1).getDay(); // 0 = Sun
            const daysInMonth = new Date(year, month + 1, 0).getDate();
            const daysInPrevMonth = new Date(year, month, 0).getDate();

            const todayStr = formatDateStr(today.getFullYear(), today.getMonth() + 1, today.getDate());

            // 1. Previous Month Overflow Days
            for (let i = firstDayIndex - 1; i >= 0; i--) {
                const prevDay = daysInPrevMonth - i;
                const prevDateStr = formatDateStr(month === 0 ? year - 1 : year, month === 0 ? 12 : month, prevDay);
                const cell = createDayCell(prevDay, prevDateStr, true);
                daysGridEl.appendChild(cell);
            }

            // 2. Current Month Days
            for (let day = 1; day <= daysInMonth; day++) {
                const dateStr = formatDateStr(year, month + 1, day);
                const cell = createDayCell(day, dateStr, false, dateStr === todayStr, dateStr === selectedDateStr);
                daysGridEl.appendChild(cell);
            }

            // 3. Next Month Overflow Days to complete 35 or 42 grid cells
            const totalCells = daysGridEl.children.length;
            const remainingCells = totalCells <= 35 ? (35 - totalCells) : (42 - totalCells);
            for (let nextDay = 1; nextDay <= remainingCells; nextDay++) {
                const nextDateStr = formatDateStr(month === 11 ? year + 1 : year, month === 11 ? 1 : month + 2, nextDay);
                const cell = createDayCell(nextDay, nextDateStr, true);
                daysGridEl.appendChild(cell);
            }
        }

        function createDayCell(dayNumber, dateStr, isOtherMonth, isToday = false, isSelected = false) {
            const cell = document.createElement('div');
            cell.className = 'calendar-day-cell';
            if (isOtherMonth) cell.classList.add('other-month');
            if (isToday) cell.classList.add('today');
            if (isSelected && !isOtherMonth) cell.classList.add('selected');

            const numSpan = document.createElement('span');
            numSpan.textContent = dayNumber;
            cell.appendChild(numSpan);

            // Find matching events on this date
            const dayEvents = cachedSchedules.filter(item => isDateInRange(dateStr, item.start_date, item.end_date));

            if (dayEvents.length > 0 && !isOtherMonth) {
                cell.classList.add('has-events');
                const dotsContainer = document.createElement('div');
                dotsContainer.className = 'cal-dots-container';

                // Collect up to 3 distinct category dots
                const seenColors = new Set();
                dayEvents.forEach(item => {
                    if (seenColors.size < 3 && !seenColors.has(item.category_color)) {
                        seenColors.add(item.category_color);
                        const dot = document.createElement('span');
                        dot.className = 'cal-event-dot';
                        dot.style.backgroundColor = item.category_color;
                        dotsContainer.appendChild(dot);
                    }
                });
                cell.appendChild(dotsContainer);
            }

            if (!isOtherMonth) {
                cell.addEventListener('click', function () {
                    const prevSelected = daysGridEl.querySelector('.calendar-day-cell.selected');
                    if (prevSelected) prevSelected.classList.remove('selected');
                    cell.classList.add('selected');
                    selectedDateStr = dateStr;
                    renderDaySchedules(dateStr);
                });
            }

            return cell;
        }

        function renderDaySchedules(dateStr) {
            if (!scheduleListEl) return;

            const dayEvents = cachedSchedules.filter(item => isDateInRange(dateStr, item.start_date, item.end_date));

            if (selectedDateTitle) {
                selectedDateTitle.textContent = `Schedule: ${formatDisplayDate(dateStr)}`;
            }
            if (selectedDateSubtitle) {
                selectedDateSubtitle.textContent = dateStr === formatDateStr(today.getFullYear(), today.getMonth() + 1, today.getDate())
                    ? "Today's department schedules"
                    : `${dayEvents.length} item(s) found`;
            }
            if (eventsCountEl) {
                eventsCountEl.textContent = `${dayEvents.length} scheduled`;
            }

            if (dayEvents.length === 0) {
                scheduleListEl.innerHTML = `
                    <div class="text-center py-4 text-muted bg-light rounded-4 p-3 my-2">
                        <i class="fa-regular fa-calendar-xmark fa-2x opacity-25 mb-2 d-block"></i>
                        <p class="small mb-1 fw-medium text-secondary">No schedules on this date.</p>
                        <p class="small text-muted mb-0" style="font-size: 0.76rem;">Click dates with colored dots to see scheduled assessments & events.</p>
                    </div>
                `;
                return;
            }

            let html = '';
            dayEvents.forEach(item => {
                const timeStr = item.start_time ? `<i class="fa-regular fa-clock text-primary me-1"></i> ${item.start_time}${item.end_time ? ' - ' + item.end_time : ''}` : '';
                const venueStr = item.venue ? `<i class="fa-solid fa-location-dot text-danger me-1 ms-2"></i> ${item.venue}` : '';
                const descStr = item.description ? `<p class="small text-secondary mb-2 mt-1 lh-sm">${item.description}</p>` : '';
                const linkBtn = item.registration_link ? `<a href="${item.registration_link}" target="_blank" class="btn btn-outline-primary btn-sm rounded-pill px-2.5 py-0.5" style="font-size: 0.72rem;">Register / Details <i class="fa-solid fa-arrow-up-right-from-square ms-1"></i></a>` : '';
                const attachBtn = item.attachment_url ? `<a href="${item.attachment_url}" target="_blank" class="btn btn-outline-danger btn-sm rounded-pill px-2.5 py-0.5" style="font-size: 0.72rem;"><i class="fa-solid fa-file-pdf me-1"></i> Circular PDF</a>` : '';

                html += `
                    <div class="day-schedule-card" style="border-left-color: ${item.category_color};">
                        <div class="d-flex align-items-center justify-content-between mb-1">
                            <span class="badge rounded-pill px-2 py-0.5" style="background-color: ${item.category_color}18; color: ${item.category_color}; font-size: 0.72rem;">
                                ${item.category_display}
                            </span>
                            ${item.is_academic_calendar ? '<span class="badge bg-warning-subtle text-warning border border-warning-subtle rounded-pill" style="font-size: 0.68rem;"><i class="fa-solid fa-file-lines me-1"></i>Academic</span>' : ''}
                        </div>
                        <h6 class="fw-bold text-dark mb-1 font-heading" style="font-size: 0.92rem;">${item.title}</h6>
                        <div class="small text-muted mb-1" style="font-size: 0.78rem;">
                            ${timeStr} ${venueStr}
                        </div>
                        ${descStr}
                        <div class="d-flex align-items-center gap-2 mt-2">
                            ${linkBtn}
                            ${attachBtn}
                        </div>
                    </div>
                `;
            });

            scheduleListEl.innerHTML = html;
        }

        // Event Listeners for Prev / Next / Today
        if (prevBtn) {
            prevBtn.addEventListener('click', function () {
                viewDate.setMonth(viewDate.getMonth() - 1);
                fetchSchedulesAndRender();
            });
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', function () {
                viewDate.setMonth(viewDate.getMonth() + 1);
                fetchSchedulesAndRender();
            });
        }

        if (todayBtn) {
            todayBtn.addEventListener('click', function () {
                viewDate = new Date();
                selectedDateStr = formatDateStr(today.getFullYear(), today.getMonth() + 1, today.getDate());
                fetchSchedulesAndRender();
            });
        }

        // Category Filter Tabs
        if (filterBar) {
            const tabs = filterBar.querySelectorAll('.news-tab-pill');
            tabs.forEach(tab => {
                tab.addEventListener('click', function () {
                    tabs.forEach(t => t.classList.remove('active'));
                    tab.classList.add('active');
                    currentCategory = tab.getAttribute('data-cal-category') || 'all';
                    fetchSchedulesAndRender();
                });
            });
        }

        // Initial Load
        fetchSchedulesAndRender();
    }

    function initInteractiveCalendars() {
        // 1. Homepage Embedded Calendar Widget
        if (document.getElementById('homeCalDaysGrid')) {
            setupCalendarInstance({
                monthYearId: 'homeCalMonthYear',
                daysGridId: 'homeCalDaysGrid',
                prevBtnId: 'homeCalPrevBtn',
                nextBtnId: 'homeCalNextBtn',
                todayBtnId: 'homeCalTodayBtn',
                filterBarId: 'homeCalFilterBar',
                scheduleListId: 'homeCalDayScheduleList',
                selectedDateTitleId: 'homeCalSelectedDateTitle',
                selectedDateSubtitleId: 'homeCalSelectedDateSubtitle',
                eventsCountId: 'homeCalEventsCount',
            });
        }

        // 2. Full Dedicated Calendar Page
        if (document.getElementById('fullCalDaysGrid')) {
            setupCalendarInstance({
                monthYearId: 'fullCalMonthYear',
                daysGridId: 'fullCalDaysGrid',
                prevBtnId: 'fullCalPrevBtn',
                nextBtnId: 'fullCalNextBtn',
                todayBtnId: 'fullCalTodayBtn',
                filterBarId: 'fullCalFilterBar',
                scheduleListId: 'fullCalDayScheduleList',
                selectedDateTitleId: 'fullCalSelectedDateTitle',
                selectedDateSubtitleId: 'fullCalSelectedDateSubtitle',
                eventsCountId: 'fullCalEventsCount',
            });
        }
    }

    // -------------------------------------------------------------
    // 8. Cyber IDE Tab Switcher in Hero
    // -------------------------------------------------------------
    function initCyberIdeTabs() {
        const tabsBar = document.getElementById('ideTabsBar');
        if (!tabsBar) return;

        const tabButtons = tabsBar.querySelectorAll('.ide-tab-btn');
        const codeView = document.getElementById('tabContentCode');
        const terminalView = document.getElementById('tabContentTerminal');
        const specsView = document.getElementById('tabContentSpecs');

        tabButtons.forEach(function (btn) {
            btn.addEventListener('click', function () {
                tabButtons.forEach(function (b) { b.classList.remove('active'); });
                btn.classList.add('active');

                const targetTab = btn.getAttribute('data-tab');
                if (codeView) codeView.classList.toggle('d-none', targetTab !== 'code');
                if (terminalView) terminalView.classList.toggle('d-none', targetTab !== 'terminal');
                if (specsView) specsView.classList.toggle('d-none', targetTab !== 'specs');
            });
        });
    }

    // -------------------------------------------------------------
    // Initialize Everything on DOMContentLoaded
    // -------------------------------------------------------------
    document.addEventListener('DOMContentLoaded', function () {
        initContactFormValidation();
        initNewsBoardFilter();
        initNewsQuickModal();
        initAchievementCounters();
        initShareButton();
        initHomeHeroEffects();
        initInteractiveCalendars();
        initCyberIdeTabs();
    });
})();
