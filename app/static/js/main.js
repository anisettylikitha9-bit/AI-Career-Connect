/**
 * AI Career Connect - Main JavaScript
 * Shared utilities loaded on every page.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Auto-dismiss flash alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach((alert) => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 5000);
    });
});
