// CORE Hi-fi — shared UI atoms and chrome
// All components export to window for cross-file use.

const { useState, useEffect, useRef, useContext, createContext } = React;

// ============================================================
// STORE / CONTEXT
// ============================================================

const StoreCtx = createContext(null);
function useStore() { return useContext(StoreCtx); }

// ============================================================
// STATUS DEFINITIONS
// ============================================================

const STATUS_META = {
  'Submitted':       { cls: 'tag--info',    dot: true,  label: 'Submitted',     hint: 'Awaiting review' },
  'In Progress':     { cls: 'tag--warning', dot: true,  label: 'In Progress',   hint: 'Recipient editing' },
  'Returned':        { cls: 'tag--warning', dot: true,  label: 'Returned',      hint: 'Awaiting resubmit' },
  'Accepted':        { cls: 'tag--success', dot: true,  label: 'Accepted',      hint: 'Locked' },
  'Closed':          { cls: 'tag--neutral', dot: true,  label: 'Closed',        hint: 'Locked' },
};

function StatusTag({ status, size }) {
  const m = STATUS_META[status] || STATUS_META['Submitted'];
  return (
    <span className={`tag ${m.cls} ${m.dot ? 'tag--dot' : ''} ${size === 'sm' ? 'tag--sm' : ''}`}>
      {m.label}
    </span>
  );
}

function ReturnTag({ count, max = 1 }) {
  if (count === 0) {
    return <span className="tag tag--neutral tag--sm">0 / {max}</span>;
  }
  return <span className="tag tag--warning tag--sm">{count} / {max}</span>;
}

// ============================================================
// CHROME — gov banner + app header + nav
// ============================================================

function GovBanner() {
  const [open, setOpen] = useState(false);
  return (
    <div className="usgov-stripe">
      <div className="usgov-stripe__flag" aria-hidden="true">🇺🇸</div>
      <span>An official website of the United States government</span>
      <button className="usgov-stripe__btn" onClick={() => setOpen(!open)}>
        Here's how you know <span className="caret">{open ? '▴' : '▾'}</span>
      </button>
    </div>
  );
}

function AppHeader() {
  const { user } = useStore();
  return (
    <header className="app-header">
      <div className="app-header__brand" onClick={() => window.location.hash = '#/inbox'}>
        <div className="app-header__logo">C</div>
        <div>
          <div className="app-header__title">CORE</div>
          <div className="app-header__subtitle">Community Outcomes Reporting Engine · OCS</div>
        </div>
      </div>
      <nav className="app-header__nav">
        <a href="#/inbox" className="active">Submissions</a>
        <a href="#/forms">Form templates</a>
        <a href="#/exports">Exports</a>
        <a href="#/help">Help</a>
      </nav>
      <div className="app-header__user">
        <button className="iconbtn" title="Notifications">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
          <span className="iconbtn__dot" />
        </button>
        <div className="app-header__avatar">
          <div className="avatar">{user.initials}</div>
          <div className="app-header__meta">
            <div>{user.name}</div>
            <div className="t-muted t-xs">{user.role}</div>
          </div>
        </div>
      </div>
    </header>
  );
}

// ============================================================
// LAYOUT
// ============================================================

function PageHeader({ title, meta, actions, breadcrumbs }) {
  return (
    <div className="ph">
      {breadcrumbs && (
        <div className="ph__crumbs">
          {breadcrumbs.map((c, i) => (
            <React.Fragment key={i}>
              {i > 0 && <span className="ph__sep">›</span>}
              {c.href ? <a href={c.href}>{c.label}</a> : <span>{c.label}</span>}
            </React.Fragment>
          ))}
        </div>
      )}
      <div className="ph__row">
        <div>
          <h1 className="ph__title">{title}</h1>
          {meta && <div className="ph__meta">{meta}</div>}
        </div>
        {actions && <div className="ph__actions">{actions}</div>}
      </div>
    </div>
  );
}

// ============================================================
// BUTTONS
// ============================================================

function Btn({ variant = 'primary', size, icon, iconRight, disabled, onClick, children, type, fullWidth, ...rest }) {
  const cls = [
    'btn',
    `btn--${variant}`,
    size && `btn--${size}`,
    fullWidth && 'btn--full',
    disabled && 'is-disabled',
  ].filter(Boolean).join(' ');
  return (
    <button type={type || 'button'} className={cls} disabled={disabled} onClick={onClick} {...rest}>
      {icon && <span className="btn__icon">{icon}</span>}
      {children}
      {iconRight && <span className="btn__icon btn__icon--right">{iconRight}</span>}
    </button>
  );
}

// ============================================================
// CARD / SECTION
// ============================================================

function Card({ children, className = '', ...rest }) {
  return <div className={`card ${className}`} {...rest}>{children}</div>;
}

function Section({ num, title, meta, locked, lockedNote, children, defaultOpen = true }) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className={`section ${locked ? 'section--locked' : ''}`}>
      <div className="section__head" onClick={() => setOpen(!open)}>
        <div className="section__head-l">
          {num != null && <span className="section__num">{num}</span>}
          <h2>{title}</h2>
          {locked && (
            <span className="section__lockchip" title="Restricted from Federal Staff edits">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              Recipient-only
            </span>
          )}
        </div>
        <div className="section__head-r">
          {meta && <span className="t-sm t-muted">{meta}</span>}
          <span className="section__chev">{open ? '▾' : '▸'}</span>
        </div>
      </div>
      {open && <div className="section__body">{children}</div>}
      {open && lockedNote && <div className="section__lockednote">{lockedNote}</div>}
    </div>
  );
}

// ============================================================
// FORM FIELDS (display + edit)
// ============================================================

function Field({ label, value, locked, edited, originalValue, placeholder, full }) {
  return (
    <div className={`fld ${locked ? 'is-locked' : ''} ${edited ? 'is-edited' : ''} ${full ? 'fld--full' : ''}`}>
      <div className="fld__lbl">{label}</div>
      <div className={`fld__val ${!value ? 'fld__val--placeholder' : ''}`}>
        {value || placeholder || '—'}
      </div>
      {edited && originalValue !== undefined && (
        <div className="fld__edited-meta">
          <span className="fld__strikethrough">{originalValue}</span>
          <span> → changed by Federal Staff</span>
        </div>
      )}
    </div>
  );
}

function InputField({ label, value, onChange, locked, edited, originalValue, multiline, full, currency, placeholder }) {
  const cls = [`fld`, locked && 'is-locked', edited && 'is-edited', full && 'fld--full'].filter(Boolean).join(' ');
  return (
    <div className={cls}>
      <div className="fld__lbl">{label}</div>
      {currency && <span className="fld__currency">$</span>}
      {multiline ? (
        <textarea value={value || ''} onChange={(e) => onChange(e.target.value)} disabled={locked} placeholder={placeholder} />
      ) : (
        <input
          type="text"
          value={value == null ? '' : value}
          onChange={(e) => onChange(e.target.value)}
          disabled={locked}
          placeholder={placeholder}
          className={currency ? 'fld__input--currency' : ''}
        />
      )}
      {edited && originalValue !== undefined && (
        <div className="fld__edited-meta">
          Was: <span className="fld__strikethrough">{originalValue}</span>
        </div>
      )}
    </div>
  );
}

// ============================================================
// ALERTS
// ============================================================

function Alert({ variant = 'info', title, children, actions, icon }) {
  return (
    <div className={`alert alert--${variant}`}>
      <div className="alert__icon">{icon || getDefaultIcon(variant)}</div>
      <div className="alert__body">
        {title && <h4 className="alert__title">{title}</h4>}
        <div className="alert__text">{children}</div>
      </div>
      {actions && <div className="alert__actions">{actions}</div>}
    </div>
  );
}

function getDefaultIcon(v) {
  if (v === 'success') return '✓';
  if (v === 'warning') return '⚠';
  if (v === 'danger') return '⚠';
  return 'ℹ';
}

// ============================================================
// MODAL
// ============================================================

function Modal({ open, onClose, title, subtitle, children, footer, width = 'md', closeable = true }) {
  useEffect(() => {
    function onKey(e) {
      if (e.key === 'Escape' && open && closeable) onClose && onClose();
    }
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [open, onClose, closeable]);

  if (!open) return null;
  return (
    <div className="modal-scrim" onClick={closeable ? onClose : undefined}>
      <div
        className={`modal modal--${width}`}
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
      >
        <div className="modal__head">
          <div>
            <h2>{title}</h2>
            {subtitle && <p>{subtitle}</p>}
          </div>
          {closeable && (
            <button className="modal__close" onClick={onClose} aria-label="Close">✕</button>
          )}
        </div>
        <div className="modal__body">{children}</div>
        {footer && <div className="modal__foot">{footer}</div>}
      </div>
    </div>
  );
}

// ============================================================
// SIDE RAIL ITEMS
// ============================================================

function Rail({ title, children }) {
  return (
    <div className="rail">
      <div className="rail__head">{title}</div>
      <div className="rail__body">{children}</div>
    </div>
  );
}

function RailItem({ label, children }) {
  return (
    <div className="rail__item">
      <div className="rail__k">{label}</div>
      <div className="rail__v">{children}</div>
    </div>
  );
}

// ============================================================
// EMPTY STATE / SHIMMER
// ============================================================

function Toast({ message, onClose, variant = 'success' }) {
  useEffect(() => {
    if (!message) return;
    const t = setTimeout(() => onClose && onClose(), 3800);
    return () => clearTimeout(t);
  }, [message, onClose]);
  if (!message) return null;
  return (
    <div className={`toast toast--${variant}`}>
      <span className="toast__icon">{variant === 'success' ? '✓' : 'ℹ'}</span>
      <span>{message}</span>
      <button className="toast__close" onClick={onClose}>✕</button>
    </div>
  );
}

// ============================================================
// CURRENCY helper
// ============================================================

function fmtCurrency(n) {
  if (n == null || n === '') return '—';
  if (typeof n === 'string') {
    const parsed = parseFloat(n.toString().replace(/[$,]/g, ''));
    if (Number.isNaN(parsed)) return n;
    n = parsed;
  }
  return '$' + n.toLocaleString('en-US');
}

function parseCurrency(s) {
  if (typeof s === 'number') return s;
  if (!s) return 0;
  const v = parseFloat(s.toString().replace(/[$,\s]/g, ''));
  return Number.isNaN(v) ? 0 : v;
}

// ============================================================
// Export to window for cross-file
// ============================================================

Object.assign(window, {
  StoreCtx, useStore,
  StatusTag, ReturnTag,
  GovBanner, AppHeader,
  PageHeader,
  Btn,
  Card, Section,
  Field, InputField,
  Alert, Modal,
  Rail, RailItem,
  Toast,
  fmtCurrency, parseCurrency,
  STATUS_META,
});
