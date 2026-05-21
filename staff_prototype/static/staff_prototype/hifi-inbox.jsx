// CORE Hi-fi — Inbox with 3 switchable views (Table, Kanban, Card)

const { useState: _useState_inb, useMemo: _useMemo_inb } = React;

function ScreenInbox({ forceView }) {
  const store = useStore();
  const [view, setView] = _useState_inb(forceView || localStorage.getItem('core.inboxView') || 'table');
  const [filters, setFilters] = _useState_inb({ status: 'All', form: 'All', region: 'All', state: 'All', q: '' });
  const [sortKey, setSortKey] = _useState_inb('daysIn');
  const [sortDir, setSortDir] = _useState_inb('desc');

  const setViewPersist = (v) => {
    setView(v);
    localStorage.setItem('core.inboxView', v);
  };

  const filtered = _useMemo_inb(() => {
    const r = store.submissions.filter(s => {
      if (filters.status === 'My queue') return ['Submitted', 'In Progress', 'Returned'].includes(s.status);
      if (filters.status === 'Resolved') return ['Accepted', 'Closed'].includes(s.status);
      if (filters.status !== 'All' && s.status !== filters.status) return false;
      if (filters.form !== 'All') {
        const fName = FORM_DEFS[s.formType].short;
        if (filters.form !== fName) return false;
      }
      if (filters.region !== 'All' && s.org.region !== filters.region) return false;
      if (filters.state !== 'All' && s.org.state !== filters.state) return false;
      if (filters.q) {
        const q = filters.q.toLowerCase();
        if (!s.org.name.toLowerCase().includes(q) && !s.org.uei.toLowerCase().includes(q)) return false;
      }
      return true;
    });
    r.sort((a, b) => {
      let av = a[sortKey], bv = b[sortKey];
      if (sortKey === 'org') { av = a.org.name; bv = b.org.name; }
      if (sortKey === 'status') {
        const order = { 'Returned': 0, 'Submitted': 1, 'In Progress': 2, 'Accepted': 3, 'Closed': 4 };
        av = order[a.status]; bv = order[b.status];
      }
      if (av < bv) return sortDir === 'asc' ? -1 : 1;
      if (av > bv) return sortDir === 'asc' ? 1 : -1;
      return 0;
    });
    return r;
  }, [store.submissions, filters, sortKey, sortDir]);

  const counts = {
    all: store.submissions.length,
    myQueue: store.submissions.filter(s => ['Submitted', 'In Progress', 'Returned'].includes(s.status)).length,
    submitted: store.submissions.filter(s => s.status === 'Submitted').length,
    inProgress: store.submissions.filter(s => s.status === 'In Progress').length,
    returned: store.submissions.filter(s => s.status === 'Returned').length,
    resolved: store.submissions.filter(s => ['Accepted', 'Closed'].includes(s.status)).length,
  };

  const onSort = (k) => {
    if (sortKey === k) setSortDir(sortDir === 'asc' ? 'desc' : 'asc');
    else { setSortKey(k); setSortDir('desc'); }
  };

  return (
    <>
      <PageHeader
        title="Submissions"
        meta={`${filtered.length} of ${store.submissions.length} submissions · FY26 cycle open · across all regions`}
        actions={
          <>
            <Btn variant="ghost" icon="↓">Export CSV</Btn>
            <Btn variant="outline">Configure forms</Btn>
          </>
        }
      />

      <div className="toolbar">
        <div className="toolbar__row">
          <div className="tabs">
            {[
              { id: 'My queue', label: 'My queue', count: counts.myQueue, hint: 'open work' },
              { id: 'All', label: 'All', count: counts.all },
              { id: 'Submitted', label: 'Submitted', count: counts.submitted },
              { id: 'In Progress', label: 'In Progress', count: counts.inProgress },
              { id: 'Returned', label: 'Returned', count: counts.returned },
              { id: 'Resolved', label: 'Resolved', count: counts.resolved },
            ].map(t => (
              <button
                key={t.id}
                className={`tabs__tab ${filters.status === t.id ? 'is-active' : ''}`}
                onClick={() => setFilters({ ...filters, status: t.id })}
              >
                {t.label}
                <span className="tabs__count">{t.count}</span>
              </button>
            ))}
          </div>

          <div className="toolbar__viewswitch" role="group" aria-label="View">
            {[
              { id: 'table', label: 'Table', icon: TableIcon, hint: 'Dense triage' },
              { id: 'kanban', label: 'Kanban', icon: KanbanIcon, hint: 'By status' },
              { id: 'card', label: 'Cards', icon: CardIcon, hint: 'Roomy scan' },
            ].map(v => (
              <button
                key={v.id}
                className={`viewbtn ${view === v.id ? 'is-active' : ''}`}
                onClick={() => setViewPersist(v.id)}
                title={v.hint}
              >
                <v.icon />
                <span>{v.label}</span>
              </button>
            ))}
          </div>
        </div>

        <div className="toolbar__row toolbar__row--filters">
          <div className="searchwrap">
            <SearchIcon />
            <input
              type="text"
              placeholder="Search organization or UEI…"
              value={filters.q}
              onChange={(e) => setFilters({ ...filters, q: e.target.value })}
            />
            {filters.q && <button className="searchwrap__clear" onClick={() => setFilters({ ...filters, q: '' })}>✕</button>}
          </div>

          <Select label="Form" value={filters.form} onChange={(v) => setFilters({ ...filters, form: v })}
            options={['All', 'Tribal Plan', 'Annual Report (Short)']} />
          <Select label="Region" value={filters.region} onChange={(v) => setFilters({ ...filters, region: v })}
            options={['All', 'VI', 'VIII', 'IX', 'X']} />
          <Select label="State" value={filters.state} onChange={(v) => setFilters({ ...filters, state: v })}
            options={['All', 'AK', 'AZ', 'ND', 'OK']} />

          <div className="toolbar__spacer" />

          <button className="linkbtn" onClick={() => setFilters({ status: 'All', form: 'All', region: 'All', state: 'All', q: '' })}>
            Clear filters
          </button>
        </div>
      </div>

      {filtered.length === 0 ? (
        <EmptyState />
      ) : view === 'table' ? (
        <TableView rows={filtered} sortKey={sortKey} sortDir={sortDir} onSort={onSort} />
      ) : view === 'kanban' ? (
        <KanbanView rows={filtered} />
      ) : (
        <CardView rows={filtered} />
      )}
    </>
  );
}

// ============================================================
// TABLE VIEW
// ============================================================

function TableView({ rows, sortKey, sortDir, onSort }) {
  const Sort = ({ k }) => {
    if (sortKey !== k) return <span className="th__sort">⇅</span>;
    return <span className="th__sort th__sort--active">{sortDir === 'asc' ? '▲' : '▼'}</span>;
  };
  return (
    <div className="tbl-wrap">
      <table className="tbl tbl--hifi">
        <thead>
          <tr>
            <th onClick={() => onSort('status')}>Status <Sort k="status" /></th>
            <th onClick={() => onSort('org')}>Organization <Sort k="org" /></th>
            <th>Form · FY</th>
            <th>Region · State</th>
            <th onClick={() => onSort('submitted')}>Submitted <Sort k="submitted" /></th>
            <th onClick={() => onSort('updated')}>Last update <Sort k="updated" /></th>
            <th>Returns</th>
            <th onClick={() => onSort('daysIn')} className="text-right">Age <Sort k="daysIn" /></th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {rows.map(s => (
            <tr key={s.id} onClick={() => navTo(`#/sub/${s.id}`)} className="tbl__row--clickable">
              <td><StatusTag status={s.status} /></td>
              <td>
                <div className="tbl__org">{s.org.name}</div>
                <div className="tbl__uei">{s.org.uei}</div>
              </td>
              <td>
                <div>{FORM_DEFS[s.formType].short}</div>
                <div className="tbl__meta">{s.fy}</div>
              </td>
              <td>
                <span className="region-chip">{s.org.region}</span>
                <span className="tbl__state">{s.org.state}</span>
              </td>
              <td className="tbl__meta">{s.submitted}</td>
              <td className="tbl__meta">{s.updated}</td>
              <td><ReturnTag count={s.returns} /></td>
              <td className="text-right">
                <AgeBadge days={s.daysIn} status={s.status} />
              </td>
              <td className="text-right">
                <button className="tbl__open" onClick={(e) => { e.stopPropagation(); navTo(`#/sub/${s.id}`); }}>
                  Open →
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function AgeBadge({ days, status }) {
  const resolved = ['Accepted', 'Closed'].includes(status);
  let cls = 'age-badge';
  if (resolved) cls += ' age-badge--neutral';
  else if (days >= 20) cls += ' age-badge--hot';
  else if (days >= 10) cls += ' age-badge--warm';
  else cls += ' age-badge--cool';
  return <span className={cls}>{days}d</span>;
}

// ============================================================
// KANBAN VIEW
// ============================================================

function KanbanView({ rows }) {
  const cols = [
    { status: 'Submitted', label: 'Submitted', hint: 'New, awaiting review' },
    { status: 'In Progress', label: 'In Progress', hint: 'Recipient editing' },
    { status: 'Returned', label: 'Returned', hint: 'Awaiting resubmit' },
    { status: 'Accepted', label: 'Accepted', hint: 'Locked · resolved' },
    { status: 'Closed', label: 'Closed', hint: 'Closed without acceptance' },
  ];
  return (
    <div className="kanban kanban--hifi">
      {cols.map(c => {
        const items = rows.filter(s => s.status === c.status);
        return (
          <div className="kanban__col" key={c.status}>
            <div className="kanban__head">
              <div>
                <h4>{c.label}</h4>
                <div className="kanban__hint">{c.hint}</div>
              </div>
              <span className="kanban__count">{items.length}</span>
            </div>
            <div className="kanban__list">
              {items.length === 0 && <div className="kanban__empty">No submissions</div>}
              {items.map(s => (
                <div key={s.id} className="kcard kcard--hifi" onClick={() => navTo(`#/sub/${s.id}`)}>
                  <div className="kcard__top">
                    <div className="kcard__org">{s.org.name}</div>
                    <AgeBadge days={s.daysIn} status={s.status} />
                  </div>
                  <div className="kcard__form">{FORM_DEFS[s.formType].short} · {s.fy}</div>
                  <div className="kcard__bot">
                    <span className="region-chip region-chip--sm">{s.org.region}</span>
                    <span className="kcard__state">{s.org.state}</span>
                    <span className="kcard__sub">{s.submitted}</span>
                    {s.returns > 0 && <span className="kcard__r">R{s.returns}</span>}
                  </div>
                </div>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}

// ============================================================
// CARD VIEW
// ============================================================

function CardView({ rows }) {
  return (
    <div className="cardgrid">
      {rows.map(s => {
        const fd = FORM_DEFS[s.formType];
        const ackProgress = s.returnItems.length > 0
          ? `${s.returnItems.filter(r => r.ack).length} of ${s.returnItems.length} acknowledged`
          : null;
        return (
          <div key={s.id} className="cardgrid__card" onClick={() => navTo(`#/sub/${s.id}`)}>
            <div className="cgcard__hd">
              <StatusTag status={s.status} />
              <AgeBadge days={s.daysIn} status={s.status} />
            </div>
            <div className="cgcard__org">{s.org.name}</div>
            <div className="cgcard__form">{fd.short} · {s.fy}</div>

            <div className="cgcard__row">
              <div>
                <div className="cgcard__k">Region · State</div>
                <div className="cgcard__v">{s.org.region} · {s.org.state}</div>
              </div>
              <div>
                <div className="cgcard__k">Submitted</div>
                <div className="cgcard__v">{s.submitted}</div>
              </div>
              <div>
                <div className="cgcard__k">Returns</div>
                <div className="cgcard__v"><ReturnTag count={s.returns} /></div>
              </div>
            </div>

            {s.status === 'Returned' && ackProgress && (
              <div className="cgcard__progress">
                <ProgressBar
                  total={s.returnItems.length}
                  done={s.returnItems.filter(r => r.ack).length}
                />
                <div className="cgcard__progress-label">{ackProgress}</div>
              </div>
            )}

            {s.status === 'Accepted' && s.determination && (
              <div className="cgcard__resolved">✓ Accepted {s.determination.when} by {s.determination.by}</div>
            )}
            {s.status === 'Closed' && s.determination && (
              <div className="cgcard__resolved cgcard__resolved--closed">✕ Closed {s.determination.when}</div>
            )}

            <div className="cgcard__foot">
              <span className="cgcard__contact">
                <div className="avatar avatar--sm">{(s.data.contact?.name || 'X')[0]}</div>
                <div>
                  <div>{s.data.contact?.name}</div>
                  <div className="t-xs t-muted">{s.data.contact?.title}</div>
                </div>
              </span>
              <button className="cgcard__open">Open →</button>
            </div>
          </div>
        );
      })}
    </div>
  );
}

function ProgressBar({ total, done }) {
  const pct = total === 0 ? 0 : Math.round((done / total) * 100);
  return (
    <div className="progressbar">
      <div className="progressbar__fill" style={{ width: pct + '%' }} />
    </div>
  );
}

// ============================================================
// EMPTY STATE
// ============================================================

function EmptyState() {
  return (
    <div className="empty">
      <div className="empty__icon">⌕</div>
      <h3>No submissions match your filters</h3>
      <p>Try clearing filters or adjusting your search.</p>
    </div>
  );
}

// ============================================================
// FILTER SELECT
// ============================================================

function Select({ label, value, onChange, options }) {
  return (
    <label className="select">
      <span className="select__lbl">{label}</span>
      <select value={value} onChange={(e) => onChange(e.target.value)}>
        {options.map(o => <option key={o} value={o}>{o}</option>)}
      </select>
    </label>
  );
}

// ============================================================
// ICONS
// ============================================================

function TableIcon() {
  return <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18M9 4v16"/></svg>;
}
function KanbanIcon() {
  return <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="4" width="5" height="16" rx="1"/><rect x="10" y="4" width="5" height="10" rx="1"/><rect x="17" y="4" width="4" height="13" rx="1"/></svg>;
}
function CardIcon() {
  return <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="3" width="8" height="8" rx="1.5"/><rect x="13" y="3" width="8" height="8" rx="1.5"/><rect x="3" y="13" width="8" height="8" rx="1.5"/><rect x="13" y="13" width="8" height="8" rx="1.5"/></svg>;
}
function SearchIcon() {
  return <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>;
}

function navTo(hash) { window.location.hash = hash; }

Object.assign(window, { ScreenInbox });
