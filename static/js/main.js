/**
 * AI Sales Assistance Agent - Main JavaScript
 * Handles frontend interactions and AJAX calls
 */

// Wait for DOM to load
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize sidebar toggle
    initSidebarToggle();
    
    // Initialize theme toggle
    initThemeToggle();
    
    // Initialize tooltips
    initTooltips();
    
    // Initialize notifications
    initNotifications();
    
    // Initialize form validation
    initForms();
    
    // Initialize data tables
    initDataTables();
    
    // Start notification polling
    startNotificationPolling();
}

/**
 * Sidebar toggle functionality
 */
function initSidebarToggle() {
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const appContainer = document.querySelector('.app-container');
    
    if (sidebarToggle && appContainer) {
        // Load saved state from localStorage
        const sidebarHidden = localStorage.getItem('sidebarHidden') === 'true';
        if (sidebarHidden) {
            appContainer.classList.add('sidebar-hidden');
            sidebarToggle.innerHTML = '≡';
        } else {
            sidebarToggle.innerHTML = '☰';
        }
        
        // Toggle on click
        sidebarToggle.addEventListener('click', function() {
            appContainer.classList.toggle('sidebar-hidden');
            const isHidden = appContainer.classList.contains('sidebar-hidden');
            localStorage.setItem('sidebarHidden', isHidden);
            sidebarToggle.innerHTML = isHidden ? '≡' : '☰';
        });
    }
}

/**
 * Theme toggle functionality (Dark/Light mode)
 */
function initThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    const html = document.documentElement;
    
    if (themeToggle) {
        // Load saved theme from localStorage
        const savedTheme = localStorage.getItem('theme') || 'light';
        html.setAttribute('data-theme', savedTheme);
        updateThemeButtonIcon(savedTheme);
        
        // Toggle on click
        themeToggle.addEventListener('click', function() {
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeButtonIcon(newTheme);
        });
    }
}

/**
 * Update theme button icon
 */
function updateThemeButtonIcon(theme) {
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.innerHTML = theme === 'light' ? '🌙' : '☀️';
        themeToggle.title = theme === 'light' ? 'Switch to dark mode' : 'Switch to light mode';
    }
}


function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(el => {
        el.style.position = 'relative';
    });
}

/**
 * Notification system
 */
function initNotifications() {
    // Mark notifications as read on click
    document.querySelectorAll('.notification-item').forEach(item => {
        item.addEventListener('click', function() {
            const id = this.dataset.id;
            if (id && !this.classList.contains('read')) {
                markNotificationRead(id);
            }
        });
    });
    
    // Mark all as read button
    const markAllReadBtn = document.getElementById('mark-all-read');
    if (markAllReadBtn) {
        markAllReadBtn.addEventListener('click', function(e) {
            e.preventDefault();
            markAllNotificationsRead();
        });
    }
}

/**
 * Mark single notification as read
 */
function markNotificationRead(id) {
    fetch(`/notifications/mark-read/${id}`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        // Update UI
        const notificationItem = document.querySelector(`[data-id="${id}"]`);
        if (notificationItem) {
            notificationItem.classList.remove('unread');
            notificationItem.classList.add('read');
            updateNotificationCount();
        }
    })
    .catch(error => console.error('Error marking notification as read:', error));
}

/**
 * Mark all notifications as read
 */
function markAllNotificationsRead() {
    fetch('/notifications/mark-all-read', {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        // Update UI
        document.querySelectorAll('.notification-item.unread').forEach(item => {
            item.classList.remove('unread');
            item.classList.add('read');
        });
        updateNotificationCount();
        showAlert('All notifications marked as read', 'success');
    })
    .catch(error => console.error('Error marking all notifications as read:', error));
}

/**
 * Update notification count badge
 */
function updateNotificationCount() {
    const badge = document.getElementById('notification-count');
    if (badge) {
        const unreadCount = document.querySelectorAll('.notification-item.unread').length;
        badge.textContent = unreadCount;
        badge.style.display = unreadCount > 0 ? 'inline' : 'none';
    }
}

/**
 * Start polling for new notifications
 */
function startNotificationPolling() {
    // Check for new notifications every 30 seconds
    setInterval(() => {
        fetch('/notifications/api/count')
            .then(response => response.json())
            .then(data => {
                const badge = document.getElementById('notification-count');
                if (badge && data.count !== parseInt(badge.textContent)) {
                    badge.textContent = data.count;
                    badge.style.display = data.count > 0 ? 'inline' : 'none';
                }
            })
            .catch(error => console.error('Error polling notifications:', error));
    }, 30000);
}

/**
 * Form initialization
 */
function initForms() {
    // Add confirmation to delete actions
    document.querySelectorAll('.btn-delete').forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item?')) {
                e.preventDefault();
            }
        });
    });
    
    // Lead form validation
    const leadForm = document.getElementById('lead-form');
    if (leadForm) {
        leadForm.addEventListener('submit', function(e) {
            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim();
            
            if (!name || !email) {
                e.preventDefault();
                showAlert('Please fill in all required fields', 'error');
                return false;
            }
            
            // Basic email validation
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                e.preventDefault();
                showAlert('Please enter a valid email address', 'error');
                return false;
            }
        });
    }
    
    // Score re-calculation button
    const scoreBtn = document.getElementById('rescore-btn');
    if (scoreBtn) {
        scoreBtn.addEventListener('click', function() {
            const leadId = this.dataset.leadId;
            rescoreLead(leadId);
        });
    }
}

/**
 * Rescore a lead using AI
 */
function rescoreLead(leadId) {
    fetch(`/leads/api/score/${leadId}`)
        .then(response => response.json())
        .then(data => {
            // Update score display
            const scoreElement = document.getElementById(`score-${leadId}`);
            if (scoreElement) {
                scoreElement.textContent = data.ai_score;
                scoreElement.className = `score-badge score-${getScoreClass(data.ai_score)}`;
            }
            
            // Update recommendation
            const recElement = document.getElementById(`recommendation-${leadId}`);
            if (recElement && data.recommendation) {
                recElement.textContent = data.recommendation.action;
            }
            
            showAlert(`Lead re-scored! New score: ${data.ai_score}`, 'success');
        })
        .catch(error => {
            console.error('Error rescoring lead:', error);
            showAlert('Error rescoring lead', 'error');
        });
}

/**
 * Data tables functionality
 */
function initDataTables() {
    const tables = document.querySelectorAll('.data-table');
    tables.forEach(table => {
        // Add search functionality
        const searchInput = table.parentElement.querySelector('.table-search');
        if (searchInput) {
            searchInput.addEventListener('input', function() {
                const searchTerm = this.value.toLowerCase();
                const rows = table.querySelectorAll('tbody tr');
                
                rows.forEach(row => {
                    const text = row.textContent.toLowerCase();
                    row.style.display = text.includes(searchTerm) ? '' : 'none';
                });
            });
        }
        
        // Add sort functionality
        const headers = table.querySelectorAll('th[data-sort]');
        headers.forEach(header => {
            header.addEventListener('click', function() {
                const column = this.dataset.sort;
                sortTable(table, column, this);
            });
        });
    });
}

/**
 * Sort table by column
 */
function sortTable(table, column, header) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    // Determine sort direction
    const isAsc = header.classList.contains('sort-asc');
    const direction = isAsc ? 'desc' : 'asc';
    
    // Remove sort classes from all headers
    table.querySelectorAll('th[data-sort]').forEach(th => {
        th.classList.remove('sort-asc', 'sort-desc');
    });
    
    // Add sort class to current header
    header.classList.add(`sort-${direction}`);
    
    // Sort rows
    rows.sort((a, b) => {
        const aVal = a.querySelector(`td[data-column="${column}"]`)?.textContent || '';
        const bVal = b.querySelector(`td[data-column="${column}"]`)?.textContent || '';
        
        // Try numeric comparison
        const aNum = parseFloat(aVal);
        const bNum = parseFloat(bVal);
        
        if (!isNaN(aNum) && !isNaN(bNum)) {
            return direction === 'asc' ? aNum - bNum : bNum - aNum;
        }
        
        // String comparison
        return direction === 'asc' 
            ? aVal.localeCompare(bVal) 
            : bVal.localeCompare(aVal);
    });
    
    // Re-append sorted rows
    rows.forEach(row => tbody.appendChild(row));
}

/**
 * Get score class based on value
 */
function getScoreClass(score) {
    if (score >= 70) return 'high';
    if (score >= 40) return 'medium';
    return 'low';
}

/**
 * Show alert message
 */
function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alert-container');
    if (!alertContainer) return;
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.innerHTML = `
        <span class="alert-icon">${getAlertIcon(type)}</span>
        <span>${message}</span>
    `;
    
    alertContainer.appendChild(alert);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 300);
    }, 5000);
}

/**
 * Get alert icon based on type
 */
function getAlertIcon(type) {
    const icons = {
        success: '✓',
        error: '✕',
        warning: '⚠',
        info: 'ℹ'
    };
    return icons[type] || icons.info;
}

/**
 * Dashboard API calls
 */
function loadDashboardStats() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            // Update stat cards
            document.getElementById('total-leads').textContent = data.total_leads;
            document.getElementById('high-priority').textContent = data.priority_counts.high;
            document.getElementById('medium-priority').textContent = data.priority_counts.medium;
            document.getElementById('low-priority').textContent = data.priority_counts.low;
        })
        .catch(error => console.error('Error loading dashboard stats:', error));
}

/**
 * Filter leads by status
 */
function filterLeadsByStatus(status) {
    const rows = document.querySelectorAll('#leads-table tbody tr');
    rows.forEach(row => {
        const rowStatus = row.dataset.status;
        if (status === 'all' || rowStatus === status) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

/**
 * Filter leads by priority
 */
function filterLeadsByPriority(priority) {
    const rows = document.querySelectorAll('#leads-table tbody tr');
    rows.forEach(row => {
        const rowPriority = row.dataset.priority;
        if (priority === 'all' || rowPriority === priority) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

/**
 * Export leads to CSV
 */
function exportLeadsToCSV() {
    const leads = [];
    const rows = document.querySelectorAll('#leads-table tbody tr');

    rows.forEach(row => {
        const lead = {
            name: row.dataset.name,
            email: row.dataset.email,
            company: row.dataset.company,
            phone: row.dataset.phone,
            job_title: row.dataset.jobTitle,
            source: row.dataset.source,
            company_size: row.dataset.companySize,
            engagement_level: row.dataset.engagementLevel,
            budget_range: row.dataset.budgetRange,
            timeline: row.dataset.timeline,
            ai_score: row.dataset.score,
            status: row.dataset.status
        };
        leads.push(lead);
    });

    if (leads.length === 0) {
        showAlert('No leads to export', 'warning');
        return;
    }

    const headers = Object.keys(leads[0]);
    const csvContent = [
        headers.join(','),
        ...leads.map(lead => headers.map(h => `"${lead[h] || ''}"`).join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `leads_export_${new Date().toISOString().split('T')[0]}.csv`;
    link.click();

    showAlert('Leads exported successfully', 'success');
}

/**
 * Import leads from CSV
 */
function importLeadsFromCSV() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.csv';
    input.onchange = function(e) {
        const file = e.target.files[0];
        if (file) {
            const formData = new FormData();
            formData.append('file', file);

            showAlert('Importing leads...', 'info');

            fetch('/leads/import-csv', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlert(`Successfully imported ${data.imported_count} leads`, 'success');
                    location.reload();
                } else {
                    showAlert(data.message || 'Import failed', 'error');
                }
            })
            .catch(error => {
                console.error('Error importing CSV:', error);
                showAlert('Error importing CSV file', 'error');
            });
        }
    };
    input.click();
}

/**
 * AI Insights toggle
 */
function toggleAIInsights() {
    const insightsPanel = document.getElementById('ai-insights-panel');
    if (insightsPanel) {
        insightsPanel.classList.toggle('hidden');
    }
}

/**
 * Batch actions for leads
 */
function batchAction(action) {
    const selectedLeads = Array.from(document.querySelectorAll('.lead-checkbox:checked'))
        .map(checkbox => checkbox.value);
    
    if (selectedLeads.length === 0) {
        showAlert('Please select at least one lead', 'warning');
        return;
    }
    
    // Show confirmation for destructive actions
    if (action === 'delete') {
        if (!confirm(`Are you sure you want to delete ${selectedLeads.length} leads?`)) {
            return;
        }
    }
    
    // Send batch request
    fetch('/leads/batch-action', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({
            action: action,
            lead_ids: selectedLeads
        })
    })
    .then(response => response.json())
    .then(data => {
        showAlert(data.message, data.success ? 'success' : 'error');
        if (data.success) {
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error with batch action:', error);
        showAlert('Error performing batch action', 'error');
    });
}

// Make functions globally available
window.rescoreLead = rescoreLead;
window.filterLeadsByStatus = filterLeadsByStatus;
window.filterLeadsByPriority = filterLeadsByPriority;
window.exportLeadsToCSV = exportLeadsToCSV;
window.importLeadsFromCSV = importLeadsFromCSV;
window.batchAction = batchAction;
window.markNotificationRead = markNotificationRead;
window.markAllNotificationsRead = markAllNotificationsRead;
window.showAlert = showAlert;

