/* ============================================
   MALL DIN Cash & Carry - Main JavaScript
   ============================================ */

document.addEventListener('DOMContentLoaded', function () {
    initMobileMenu();
    initStickyHeader();
    initCartFunctions();
    initSearch();
    initNewsletter();
    initAlertDismiss();
    initBackToTop();
    initQuantityButtons();
    initScrollReveal();
});

function initMobileMenu() {
    var hamburger = document.getElementById('hamburgerBtn');
    var nav = document.getElementById('headerNav');
    if (!hamburger || !nav) return;
    hamburger.addEventListener('click', function () {
        this.classList.toggle('active');
        nav.classList.toggle('nav-open');
        document.body.style.overflow = nav.classList.contains('nav-open') ? 'hidden' : '';
    });
}

function initStickyHeader() {
    var header = document.getElementById('siteHeader');
    if (!header) return;
    window.addEventListener('scroll', function () {
        if (window.scrollY > 50) header.classList.add('scrolled');
        else header.classList.remove('scrolled');
    });
}

function initCartFunctions() {
    document.querySelectorAll('.add-to-cart-btn, .product-card-add-btn').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            var form = this.closest('form');
            if (!form) return;
            e.preventDefault();
            var submitBtn = this;
            var originalText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adding...';
            fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(function (r) { return r.json(); })
            .then(function (data) {
                if (data.success) {
                    showToast(data.message || 'Added to Cart', 'success');
                    updateCartBadge(data.cart_count);
                    submitBtn.innerHTML = '<i class="fas fa-check"></i> Added';
                    setTimeout(function () {
                        submitBtn.disabled = false;
                        submitBtn.innerHTML = originalText;
                    }, 2000);
                } else {
                    showToast(data.message || 'Failed', 'error');
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }
            })
            .catch(function () { form.submit(); });
        });
    });
}

function updateCartBadge(count) {
    document.querySelectorAll('.cart-badge').forEach(function (badge) {
        badge.textContent = count;
        badge.style.display = count > 0 ? 'flex' : 'none';
    });
}

function showToast(message, type) {
    type = type || 'info';
    var container = document.getElementById('toastContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    var icons = { success: 'fa-check-circle', error: 'fa-times-circle', info: 'fa-info-circle', warning: 'fa-exclamation-triangle' };
    var toast = document.createElement('div');
    toast.className = 'toast toast-' + type;
    toast.innerHTML = '<span class="toast-icon"><i class="fas ' + (icons[type] || icons.info) + '"></i></span>' +
        '<span class="toast-message">' + message + '</span>' +
        '<button class="toast-close" onclick="this.parentElement.remove()">&times;</button>';
    container.appendChild(toast);
    setTimeout(function () {
        toast.classList.add('toast-hide');
        setTimeout(function () { if (toast.parentNode) toast.remove(); }, 300);
    }, 4000);
}

function initSearch() {
    document.querySelectorAll('.header-search form, .store-search').forEach(function (form) {
        form.addEventListener('submit', function (e) {
            var input = this.querySelector('input[name="q"]');
            if (input && !input.value.trim()) {
                e.preventDefault();
                showToast('Please enter a search term.', 'warning');
                input.focus();
            }
        });
    });
}

function initNewsletter() {
    document.querySelectorAll('.newsletter-form').forEach(function (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            var emailInput = this.querySelector('input[type="email"]');
            var submitBtn = this.querySelector('button');
            if (!emailInput || !emailInput.value.trim()) {
                showToast('Please enter your email address.', 'error');
                return;
            }
            submitBtn.disabled = true;
            fetch(form.action, { method: 'POST', body: new FormData(form) })
            .then(function () {
                showToast('Thank you for subscribing!', 'success');
                emailInput.value = '';
                submitBtn.disabled = false;
            })
            .catch(function () {
                showToast('An error occurred.', 'error');
                submitBtn.disabled = false;
            });
        });
    });
}

function initAlertDismiss() {
    document.querySelectorAll('.alert .alert-close').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var alertEl = this.closest('.alert');
            if (alertEl) alertEl.remove();
        });
    });
    setTimeout(function () {
        document.querySelectorAll('.alert').forEach(function (a) { a.remove(); });
    }, 6000);
}

function initBackToTop() {
    var btn = document.getElementById('backToTop');
    if (!btn) return;
    window.addEventListener('scroll', function () {
        if (window.scrollY > 400) btn.classList.add('visible');
        else btn.classList.remove('visible');
    });
    btn.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

function initQuantityButtons() {
    document.querySelectorAll('.quantity-control').forEach(function (selector) {
        var minusBtn = selector.querySelector('.qty-btn.minus, .quantity-btn:first-child');
        var plusBtn = selector.querySelector('.qty-btn.plus, .quantity-btn:last-child');
        var input = selector.querySelector('input');
        if (!minusBtn || !plusBtn || !input) return;
        minusBtn.addEventListener('click', function () {
            var val = parseInt(input.value) || 1;
            if (val > 1) { input.value = val - 1; input.dispatchEvent(new Event('change')); }
        });
        plusBtn.addEventListener('click', function () {
            var val = parseInt(input.value) || 1;
            var max = parseInt(input.getAttribute('max')) || 99;
            if (val < max) { input.value = val + 1; input.dispatchEvent(new Event('change')); }
        });
    });
}

function initScrollReveal() {
    var elements = document.querySelectorAll('.reveal');
    if (elements.length === 0) return;
    var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    elements.forEach(function (el) { observer.observe(el); });
}
