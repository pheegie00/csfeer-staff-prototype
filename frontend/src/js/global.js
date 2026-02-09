import '@uswds/uswds';
import Alpine from 'alpinejs'
import mask from '@alpinejs/mask'

// Form utilities
import { updateCalculatedFields } from './utils/forms';

// Expose form utilities globally for Alpine.js template access
window.updateCalculatedFields = updateCalculatedFields;

Alpine.plugin(mask)
Alpine.start()