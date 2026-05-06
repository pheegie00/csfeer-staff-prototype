import '@uswds/uswds';
import Alpine from 'alpinejs'
import mask from '@alpinejs/mask'

// Form utilities
import { updateCalculatedFields, initSideNavSaveOnNavigate } from './utils/forms';
import { initEditingLock } from './editing-lock';

// Expose form utilities globally for Alpine.js template access
window.updateCalculatedFields = updateCalculatedFields;

initSideNavSaveOnNavigate();
initEditingLock();

Alpine.plugin(mask)
Alpine.start()