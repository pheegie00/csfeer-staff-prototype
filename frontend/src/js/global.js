import '@uswds/uswds';
import Alpine from 'alpinejs'
import mask from '@alpinejs/mask'

// Form utilities
import { updateCalculatedFields, initSideNavSaveOnNavigate } from './utils/forms';

// Expose form utilities globally for Alpine.js template access
window.updateCalculatedFields = updateCalculatedFields;

initSideNavSaveOnNavigate();

Alpine.plugin(mask)
Alpine.start()