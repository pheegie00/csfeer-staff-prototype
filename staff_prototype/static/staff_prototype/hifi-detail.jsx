// CORE Hi-fi — Submission detail (review + edit-on-behalf modes), form renderers, activity log

const { useState: _useStateD, useMemo: _useMemoD, useEffect: _useEffectD } = React;

// ============================================================
// SUBMISSION DETAIL SCREEN
// ============================================================

function ScreenSubmission({ id, mode = 'review' }) {
  const store = useStore();
  const sub = store.submissions.find(s => s.id === id);
  if (!sub) return <NotFound />;

  const fd = FORM_DEFS[sub.formType];
  const resolved = ['Accepted', 'Closed'].includes(sub.status);
  const returned = sub.status === 'Returned';
  const canEdit = !resolved && !returned;
  const canReturn = !resolved && sub.returns === 0 && (sub.status === 'Submitted');
  const canDetermine = !resolved && (sub.status === 'Submitted' || sub.status === 'In Progress');
  const finalReviewOnly = sub.returns === 1 && !resolved && !returned;

  // edit mode local state
  const [pendingEdits, setPendingEdits] = _useStateD(sub.pendingEdits || {});
  const [showLog, setShowLog] = _useStateD(false);

  _useEffectD(() => { setPendingEdits(sub.pendingEdits || {}); }, [sub.id]);

  const edits = mergeEdits(sub.edits, pendingEdits);
  const hasPending = Object.keys(pendingEdits).length > 0;

  const onFieldChange = (path, value) => {
    const orig = getByPath(sub.data, path);
    if (value === orig) {
      // revert
      const np = { ...pendingEdits };
      delete np[path];
      setPendingEdits(np);
    } else {
      setPendingEdits({ ...pendingEdits, [path]: { value, original: orig } });
    }
  };

  const onSaveWithRationale = () => {
    store.openRationale({ subId: sub.id, pending: pendingEdits, onConfirm: (rationale) => {
      store.applyEdits(sub.id, pendingEdits, rationale);
      setPendingEdits({});
      navTo(`#/sub/${sub.id}`);
    }});
  };

  const onDiscardEdits = () => {
    if (Object.keys(pendingEdits).length > 0 && !confirm('Discard all pending edits?')) return;
    setPendingEdits({});
    navTo(`#/sub/${sub.id}`);
  };

  return (
    <>
      <PageHeader
        breadcrumbs={[
          { label: 'Submissions', href: '#/inbox' },
          { label: sub.org.name },
          { label: mode === 'edit' ? 'Edit on behalf' : fd.short },
        ]}
        title={null}
      />

      {/* Edit-on-behalf banner */}
      {mode === 'edit' && (
        <Alert
          variant="warning"
          icon="✎"
          title={`You are editing on behalf of ${sub.org.name}`}
          actions={
            <>
              <Btn variant="ghost" size="sm" onClick={onDiscardEdits}>Discard</Btn>
              <Btn size="sm" disabled={!hasPending} onClick={onSaveWithRationale}>
                Save with rationale {hasPending && `(${Object.keys(pendingEdits).length})`}
              </Btn>
            </>
          }
        >
          Every change is logged. You'll be asked for a rationale before saving (REQ-043). <strong>Attestation</strong> and <strong>AO Signature</strong> are restricted to recipients — staff cannot edit those fields.
        </Alert>
      )}

      {finalReviewOnly && mode === 'review' && (
        <Alert variant="info" icon="ⓘ" title="Final review — one return already used">
          This submission has been returned once already (resubmitted {sub.submitted}). Per REQ-024, your only remaining actions are <strong>Accept</strong> or <strong>Close without acceptance</strong>. A second return is not available.
        </Alert>
      )}

      {resolved && (
        <Alert
          variant={sub.status === 'Accepted' ? 'success' : 'neutral'}
          icon={sub.status === 'Accepted' ? '✓' : '✕'}
          title={`${sub.status === 'Accepted' ? 'Accepted' : 'Closed without acceptance'} · ${sub.determination.when} by ${sub.determination.by}`}
          actions={
            <>
              <Btn variant="ghost" size="sm" onClick={() => setShowLog(true)}>Activity log</Btn>
              <Btn variant="outline" size="sm">Download CSV</Btn>
              <Btn variant="outline" size="sm">Download PDF</Btn>
            </>
          }
        >
          Locked from all edits (REQ-026). Record retained indefinitely (REQ-035).
          {sub.determination.notes && <div className="mt-1"><em>"{sub.determination.notes}"</em></div>}
        </Alert>
      )}

      {/* Sticky action bar */}
      <ActionBar
        sub={sub}
        mode={mode}
        hasPending={hasPending}
        showLog={() => setShowLog(true)}
        canEdit={canEdit}
        canReturn={canReturn}
        canDetermine={canDetermine}
      />

      <div className="layout layout--detail">
        <div className="layout__main">
          {sub.status === 'Returned' && <ReturnedStatePanel sub={sub} />}
          {sub.formType === 'tribal-plan'
            ? <TribalPlanForm sub={sub} edits={edits} pendingEdits={pendingEdits} editable={mode === 'edit'} onFieldChange={onFieldChange} />
            : <AnnualReportShortForm sub={sub} edits={edits} pendingEdits={pendingEdits} editable={mode === 'edit'} onFieldChange={onFieldChange} />
          }
        </div>
        <div className="layout__side">
          <SubmissionRail sub={sub} pendingCount={Object.keys(pendingEdits).length} editMode={mode === 'edit'} onShowLog={() => setShowLog(true)} />
          {sub.returnItems.length > 0 && <ReturnItemsRail sub={sub} />}
        </div>
      </div>

      <ActivityLogDrawer open={showLog} onClose={() => setShowLog(false)} sub={sub} />
    </>
  );
}

// ============================================================
// ACTION BAR
// ============================================================

function ActionBar({ sub, mode, hasPending, showLog, canEdit, canReturn, canDetermine }) {
  const store = useStore();
  const fd = FORM_DEFS[sub.formType];

  if (['Accepted', 'Closed'].includes(sub.status)) {
    return (
      <div className="actionbar actionbar--locked">
        <div className="actionbar__left">
          <StatusTag status={sub.status} />
          <div>
            <div className="actionbar__org">{sub.org.name}</div>
            <div className="actionbar__sub t-sm t-muted">
              {fd.short} · {sub.fy} · {sub.returns} return{sub.returns !== 1 ? 's' : ''} · {sub.daysIn}d cycle
            </div>
          </div>
        </div>
        <div className="actionbar__right">
          <span className="t-sm t-muted mr-2">🔒 All actions locked</span>
        </div>
      </div>
    );
  }

  if (sub.status === 'Returned') {
    return (
      <div className="actionbar">
        <div className="actionbar__left">
          <StatusTag status={sub.status} />
          <div>
            <div className="actionbar__org">{sub.org.name}</div>
            <div className="actionbar__sub t-sm t-muted">
              {fd.short} · {sub.fy} · Returned {sub.returnedAt} · {sub.returnItems.length} item{sub.returnItems.length !== 1 ? 's' : ''} · {sub.returnItems.filter(r => r.ack).length} of {sub.returnItems.length} acknowledged
            </div>
          </div>
        </div>
        <div className="actionbar__right">
          <Btn variant="ghost" size="sm" onClick={showLog}>Activity log</Btn>
          <Btn variant="ghost" size="sm">Email recipient</Btn>
          <Btn variant="outline" size="sm" disabled>Awaiting resubmit & resignature</Btn>
        </div>
      </div>
    );
  }

  if (mode === 'edit') {
    return (
      <div className="actionbar actionbar--edit">
        <div className="actionbar__left">
          <StatusTag status={sub.status} />
          <div>
            <div className="actionbar__org">{sub.org.name}</div>
            <div className="actionbar__sub t-sm t-muted">
              {hasPending ? `${Object.keys(sub.pendingEdits || {}).length} pending — but you have ${hasPending ? '✏ unsaved changes' : 'no changes yet'}` :
                'Make changes, then save with rationale. Lock expires 4:32 PM.'}
            </div>
          </div>
        </div>
        <div className="actionbar__right">
          <Btn variant="ghost" size="sm" onClick={showLog}>Activity log</Btn>
          <a className="btn btn--ghost btn--sm" href={`#/sub/${sub.id}`}>Exit edit mode</a>
        </div>
      </div>
    );
  }

  return (
    <div className="actionbar">
      <div className="actionbar__left">
        <StatusTag status={sub.status} />
        <div>
          <div className="actionbar__org">{sub.org.name}</div>
          <div className="actionbar__sub t-sm t-muted">
            {fd.short} · {sub.fy} · Submitted {sub.submitted} · Returns {sub.returns} / 1 · {sub.daysIn}d in queue
          </div>
        </div>
      </div>
      <div className="actionbar__right">
        <Btn variant="ghost" size="sm" onClick={showLog}>Activity log</Btn>
        <Btn variant="ghost" size="sm">View as recipient</Btn>
        <Btn variant="ghost" size="sm">Download PDF</Btn>
        {canEdit && <Btn variant="outline" onClick={() => navTo(`#/sub/${sub.id}/edit`)}>Edit on behalf</Btn>}
        {canReturn && <Btn variant="outline" onClick={() => navTo(`#/sub/${sub.id}/return`)}>Return for revision</Btn>}
        {canDetermine && <Btn onClick={() => store.openDetermination({ subId: sub.id })}>Make determination</Btn>}
      </div>
    </div>
  );
}

// ============================================================
// SUBMISSION RAIL (right side)
// ============================================================

function SubmissionRail({ sub, pendingCount, editMode, onShowLog }) {
  const fd = FORM_DEFS[sub.formType];
  return (
    <>
      {editMode && pendingCount > 0 && (
        <Rail title="This edit session">
          <RailItem label="Started">May 20 · 4:08 PM</RailItem>
          <RailItem label="Lock expires">4:32 PM</RailItem>
          <RailItem label="Pending changes">
            <strong>{pendingCount} field{pendingCount !== 1 ? 's' : ''}</strong>
            <div className="t-xs t-muted">Will be saved together with one rationale (REQ-043).</div>
          </RailItem>
        </Rail>
      )}

      <Rail title="Submission">
        <RailItem label="Organization">{sub.org.name}</RailItem>
        <RailItem label="UEI"><code>{sub.org.uei}</code></RailItem>
        <RailItem label="Region · State">{sub.org.region} · {sub.org.state}</RailItem>
        <RailItem label="Form">{fd.short}</RailItem>
        <RailItem label="Fiscal Year">{sub.fy}</RailItem>
        <RailItem label="Submitted">{sub.submitted}</RailItem>
        <RailItem label="Returns">{sub.returns} of 1 allowed</RailItem>
      </Rail>

      <Rail title="Recipient contacts">
        {sub.data.ao && (
          <RailItem label="Authorized Official">
            <div>{sub.data.ao.name}</div>
            <div className="t-xs t-muted">{sub.data.ao.title}</div>
            <div className="t-xs t-muted">{sub.data.ao.email}</div>
          </RailItem>
        )}
        {sub.data.contact && (
          <RailItem label="Primary contact">
            <div>{sub.data.contact.name}</div>
            <div className="t-xs t-muted">{sub.data.contact.title}</div>
            <div className="t-xs t-muted">{sub.data.contact.email}</div>
          </RailItem>
        )}
      </Rail>

      <button className="rail-link" onClick={onShowLog}>
        <span>View full activity log</span>
        <span>→</span>
      </button>
    </>
  );
}

function ReturnItemsRail({ sub }) {
  const ackCount = sub.returnItems.filter(r => r.ack).length;
  return (
    <Rail title={`Review items (${ackCount} of ${sub.returnItems.length} ack'd)`}>
      {sub.returnItems.map((ri, i) => (
        <div className="ri-mini" key={ri.id}>
          <div className="ri-mini__num">{i + 1}</div>
          <div>
            <div className="ri-mini__section">{ri.sectionLabel}</div>
            <div className={`ri-mini__status ${ri.ack ? 'is-ack' : ''}`}>
              {ri.ack ? `✓ Acknowledged ${ri.ack.when}` : 'Waiting for ack'}
            </div>
          </div>
        </div>
      ))}
    </Rail>
  );
}

// ============================================================
// TRIBAL PLAN FORM
// ============================================================

function TribalPlanForm({ sub, edits, pendingEdits, editable, onFieldChange }) {
  const d = sub.data;
  const F = editable ? InputFld : DisplayFld;

  const fieldProps = (path) => ({
    path,
    edits,
    pendingEdits,
    editable,
    onChange: (v) => onFieldChange(path, v),
    value: edits[path] !== undefined ? edits[path].value : getByPath(d, path),
    original: edits[path]?.original,
    edited: edits[path] !== undefined,
  });

  return (
    <>
      <Section num={1} title="Organization Information" meta="Auto-populated from UEI">
        <div className="grid-2">
          <Field label="Organization Legal Name" value={d.org.name} locked />
          <Field label="UEI" value={d.org.uei} locked />
          <Field label="State" value={d.org.state} locked />
          <Field label="Region" value={d.org.region} locked />
          <Field label="DUNS" value={d.org.duns || '—'} locked />
          <Field label="Fiscal Year" value={d.org.fy} locked />
        </div>
      </Section>

      <Section num={2} title="Primary Contact">
        <div className="grid-2">
          <F label="Name" {...fieldProps('contact.name')} />
          <F label="Title" {...fieldProps('contact.title')} />
          <F label="Email" {...fieldProps('contact.email')} />
          <F label="Phone" {...fieldProps('contact.phone')} />
        </div>
      </Section>

      <Section num={3} title="Programmatic Plan">
        <F label="Mission statement" {...fieldProps('plan.mission')} multiline full />
        <F label="Annual goals" {...fieldProps('plan.goals')} multiline full />
        <F label="Coordination with other programs" {...fieldProps('plan.coordination')} multiline full />
      </Section>

      <Section num={4} title="Service Areas">
        <F label="Service area description" {...fieldProps('services')} multiline full />
      </Section>

      <Section num={5} title="Proposed Budget" meta={`Total · ${fmtCurrency(Object.values(d.budget).reduce((a, b) => a + b, 0))}`}>
        <div className="grid-3">
          <F label="Employment Services" {...fieldProps('budget.employment')} currency />
          <F label="Education" {...fieldProps('budget.education')} currency />
          <F label="Emergency Assistance" {...fieldProps('budget.emergency')} currency />
          <F label="Housing" {...fieldProps('budget.housing')} currency />
          <F label="Nutrition" {...fieldProps('budget.nutrition')} currency />
          <F label="Administrative" {...fieldProps('budget.admin')} currency />
          <F label="Other" {...fieldProps('budget.other')} currency />
        </div>
      </Section>

      <Section num={6} title="Programmatic Narrative">
        <F label="Employment Services narrative" {...fieldProps('narrative.employment')} multiline full />
        <F label="Housing narrative" {...fieldProps('narrative.housing')} multiline full />
        <F label="Emergency Assistance narrative" {...fieldProps('narrative.emergency')} multiline full />
      </Section>

      <Section
        num={7}
        title="Attestation of Assurances"
        meta={<span className="tag tag--success tag--sm">Acknowledged</span>}
        locked
        lockedNote="Federal Staff cannot edit attestation content per REQ-043."
      >
        <p className="form-attest">
          The undersigned attests that the organization meets all CSBG eligibility, anti-discrimination, and reporting
          requirements under 42 U.S.C. §§ 9901–9926.
        </p>
        <Field label="Acknowledged by" value={`${d.attestation.ackBy} · ${d.attestation.ackAt}`} locked />
      </Section>

      <Section
        num={8}
        title="Authorized Official Signature"
        meta={d.ao.cleared ? <span className="tag tag--danger tag--sm">Cleared — requires resignature</span> : <span className="tag tag--primary tag--sm">Signed</span>}
        locked
        lockedNote="Federal Staff cannot sign or edit this section per REQ-043. Only the designated AO may complete it."
      >
        <div className="grid-2">
          <Field label="AO Name" value={d.ao.name} locked />
          <Field label="Title" value={d.ao.title} locked />
        </div>
        <div className="fld fld--full">
          <div className="fld__lbl">Typed signature</div>
          {d.ao.cleared ? (
            <div className="sig-box sig-box--cleared">
              <strong>Cleared on return</strong> · {d.ao.clearedAt} · The Authorized Official must re-sign before this submission can be re-submitted (REQ-042).
            </div>
          ) : (
            <div className="sig-box sig-box--signed">{d.ao.name}</div>
          )}
        </div>
        <Field label="Date signed" value={d.ao.signedAt || '—'} locked />
      </Section>
    </>
  );
}

// ============================================================
// ANNUAL REPORT SHORT FORM
// ============================================================

function AnnualReportShortForm({ sub, edits, pendingEdits, editable, onFieldChange }) {
  const d = sub.data;
  const F = editable ? InputFld : DisplayFld;

  const fieldProps = (path) => ({
    path,
    edits,
    pendingEdits,
    editable,
    onChange: (v) => onFieldChange(path, v),
    value: edits[path] !== undefined ? edits[path].value : getByPath(d, path),
    original: edits[path]?.original,
    edited: edits[path] !== undefined,
  });

  return (
    <>
      <Section num={1} title="Organization Information" meta="Auto-populated from UEI">
        <div className="grid-2">
          <Field label="Organization Legal Name" value={d.org.name} locked />
          <Field label="UEI" value={d.org.uei} locked />
          <Field label="State" value={d.org.state} locked />
          <Field label="Region" value={d.org.region} locked />
          <Field label="Fiscal Year" value={d.org.fy} locked />
        </div>
      </Section>

      <Section num={2} title="Primary Contact">
        <div className="grid-2">
          <F label="Name" {...fieldProps('contact.name')} />
          <F label="Title" {...fieldProps('contact.title')} />
          <F label="Email" {...fieldProps('contact.email')} />
          <F label="Phone" {...fieldProps('contact.phone')} />
        </div>
      </Section>

      <Section num={3} title="Reporting Period">
        <div className="grid-2">
          <F label="Period start" {...fieldProps('period.start')} />
          <F label="Period end" {...fieldProps('period.end')} />
        </div>
      </Section>

      <Section num={4} title="Outcomes & Counts" meta="Aggregate totals for the reporting period">
        <div className="grid-3">
          <F label="Individuals served" {...fieldProps('outcomes.individualsServed')} />
          <F label="Households served" {...fieldProps('outcomes.householdsServed')} />
          <F label="Employment outcomes" {...fieldProps('outcomes.employment')} />
          <F label="Education outcomes" {...fieldProps('outcomes.education')} />
          <F label="Housing stabilized" {...fieldProps('outcomes.housingStabilized')} />
          <F label="Food security" {...fieldProps('outcomes.foodSecurity')} />
        </div>
      </Section>

      <Section num={5} title="Services Provided">
        <F label="Services provided narrative" {...fieldProps('services')} multiline full />
      </Section>

      <Section
        num={6}
        title="Attestation"
        meta={<span className="tag tag--success tag--sm">Acknowledged</span>}
        locked
        lockedNote="Federal Staff cannot edit attestation content per REQ-043."
      >
        <p className="form-attest">The undersigned attests that all reported data is accurate to the best of their knowledge.</p>
        <Field label="Acknowledged by" value={`${d.attestation.ackBy} · ${d.attestation.ackAt}`} locked />
      </Section>
    </>
  );
}

// ============================================================
// Field wrappers — read vs edit
// ============================================================

function DisplayFld({ label, value, currency, full, locked }) {
  const display = currency ? fmtCurrency(value) : value;
  return <Field label={label} value={display} locked={locked} full={full} />;
}

function InputFld({ label, value, original, edited, onChange, currency, multiline, full, locked }) {
  if (locked) {
    const display = currency ? fmtCurrency(value) : value;
    return <Field label={label} value={display} locked full={full} />;
  }
  if (currency) {
    return (
      <div className={`fld ${edited ? 'is-edited' : ''} ${full ? 'fld--full' : ''}`}>
        <div className="fld__lbl">{label}</div>
        <div className="fld__currency-wrap">
          <span className="fld__currency-sym">$</span>
          <input
            type="text"
            value={value == null ? '' : String(value).replace(/[^0-9.]/g, '')}
            onChange={(e) => onChange(parseCurrency(e.target.value))}
            className="fld__input fld__input--currency"
          />
        </div>
        {edited && original !== undefined && (
          <div className="fld__edited-meta">Was: <span className="fld__strikethrough">{fmtCurrency(original)}</span></div>
        )}
      </div>
    );
  }
  return <InputField label={label} value={value} onChange={onChange} edited={edited} originalValue={original} multiline={multiline} full={full} />;
}

// ============================================================
// ACTIVITY LOG DRAWER
// ============================================================

function ActivityLogDrawer({ open, onClose, sub }) {
  const [filter, setFilter] = _useStateD('All');
  const events = filter === 'All' ? sub.events : sub.events.filter(e => filterMatch(e.kind, filter));
  return (
    <div className={`drawer ${open ? 'is-open' : ''}`} onClick={onClose}>
      <div className="drawer__panel" onClick={(e) => e.stopPropagation()}>
        <div className="drawer__head">
          <div>
            <h3>Activity log</h3>
            <div className="t-xs t-muted">Append-only · visible to all users · cannot be edited (REQ-028)</div>
          </div>
          <button className="drawer__close" onClick={onClose}>✕</button>
        </div>
        <div className="drawer__filters">
          {['All', 'Edits', 'Status', 'Comms'].map(f => (
            <button key={f} className={`chipbtn ${filter === f ? 'is-active' : ''}`} onClick={() => setFilter(f)}>{f}</button>
          ))}
        </div>
        <div className="drawer__body">
          {events.map((e, i) => (
            <div className={`log log--${e.kind || 'event'}`} key={i}>
              <div className="log__dot" />
              <div className="log__col">
                <div className="log__when">{e.when}</div>
                <div className="log__who">
                  <span className="log__name">{e.who}</span>
                  <span className="log__role">{e.whoRole}</span>
                </div>
                <div className="log__what">{e.action}</div>
                {e.notes && <div className="log__notes">{e.notes}</div>}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function filterMatch(kind, filter) {
  if (filter === 'Edits') return ['edit', 'create'].includes(kind);
  if (filter === 'Status') return ['submit', 'return', 'accept', 'close', 'sign'].includes(kind);
  if (filter === 'Comms') return ['return', 'ack', 'email'].includes(kind);
  return true;
}

// ============================================================
// NOT FOUND
// ============================================================

function NotFound() {
  return (
    <div className="empty empty--page">
      <div className="empty__icon">⌕</div>
      <h3>Submission not found</h3>
      <p>The submission you're looking for may have been archived.</p>
      <a className="btn btn--outline" href="#/inbox">Back to inbox</a>
    </div>
  );
}

// ============================================================
// HELPERS
// ============================================================

function getByPath(obj, path) {
  return path.split('.').reduce((acc, k) => acc?.[k], obj);
}

function setByPath(obj, path, value) {
  const out = { ...obj };
  const keys = path.split('.');
  let cur = out;
  for (let i = 0; i < keys.length - 1; i++) {
    cur[keys[i]] = { ...(cur[keys[i]] || {}) };
    cur = cur[keys[i]];
  }
  cur[keys[keys.length - 1]] = value;
  return out;
}

function mergeEdits(applied, pending) {
  const out = {};
  (applied || []).forEach(e => { e.fields.forEach(f => { out[f.path] = { value: f.value, original: f.original, applied: true, rationale: e.rationale, when: e.when, who: e.who }; }); });
  Object.entries(pending || {}).forEach(([k, v]) => { out[k] = { ...v, applied: false }; });
  return out;
}

Object.assign(window, { ScreenSubmission, getByPath, setByPath, mergeEdits });
