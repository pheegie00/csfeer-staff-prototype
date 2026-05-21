// CORE Hi-fi — Workflow actions: Return builder, Rationale modal, Determination modal, Returned items panel, Login

const { useState: _useStateW, useEffect: _useEffectW } = React;

// ============================================================
// RETURN BUILDER SCREEN (route: #/sub/:id/return)
// ============================================================

function ScreenReturnBuilder({ id }) {
  const store = useStore();
  const sub = store.submissions.find(s => s.id === id);
  if (!sub) return <NotFound />;
  if (sub.status !== 'Submitted' || sub.returns >= 1) {
    return (
      <Alert variant="warning" title="Return not available">
        This submission cannot be returned: status is <strong>{sub.status}</strong> and {sub.returns} of 1 returns used.
        <a className="alert__link" href={`#/sub/${id}`}> Back to submission</a>
      </Alert>
    );
  }
  const fd = FORM_DEFS[sub.formType];

  const [items, setItems] = _useStateW([
    blankItem(1),
  ]);
  const [summary, setSummary] = _useStateW('');
  const [showPreview, setShowPreview] = _useStateW(false);

  function blankItem(n) {
    return { id: 'ri_' + Math.random().toString(36).slice(2, 8), section: '', field: '', text: '', n };
  }

  const updateItem = (id, patch) => setItems(items.map(it => it.id === id ? { ...it, ...patch } : it));
  const addItem = () => setItems([...items, blankItem(items.length + 1)]);
  const removeItem = (id) => {
    const next = items.filter(it => it.id !== id);
    setItems(next.map((it, i) => ({ ...it, n: i + 1 })));
  };

  const validItems = items.filter(it => it.text.trim().length > 0);
  const canSend = validItems.length >= 1;

  const onSend = () => {
    if (!canSend) return;
    store.returnSubmission(sub.id, validItems, summary);
    store.showToast(`Returned to ${sub.org.name} with ${validItems.length} item${validItems.length !== 1 ? 's' : ''}. AO signature cleared.`);
    navTo(`#/sub/${sub.id}`);
  };

  return (
    <>
      <PageHeader
        breadcrumbs={[
          { label: 'Submissions', href: '#/inbox' },
          { label: sub.org.name, href: `#/sub/${sub.id}` },
          { label: 'Return for revision' },
        ]}
        title="Return for revision"
        meta={`${sub.org.name} · ${fd.short} · ${sub.fy}`}
      />

      <Alert variant="danger" icon="⚠" title="One return only">
        CORE allows <strong>one return per submission</strong> (REQ-024). After {sub.org.name} resubmits, your only remaining
        actions will be <strong>Accept</strong> or <strong>Close without acceptance</strong>. Make sure every item the recipient needs to address is captured below.
      </Alert>

      <div className="layout layout--detail">
        <div className="layout__main">
          <Card className="card--builder">
            <div className="card__head card__head--builder">
              <div>
                <h3>Review items</h3>
                <div className="t-sm t-muted">
                  Minimum 1 item. Each becomes a discrete item the recipient must acknowledge before resubmit (REQ-023).
                  Functional parity with the current review memo (REQ-044).
                </div>
              </div>
              <span className="tag tag--primary">{validItems.length} valid item{validItems.length !== 1 ? 's' : ''}</span>
            </div>
            <div className="card__body">
              {items.map((it) => (
                <ReturnItemEditor
                  key={it.id}
                  item={it}
                  fd={fd}
                  onChange={(patch) => updateItem(it.id, patch)}
                  onRemove={items.length > 1 ? () => removeItem(it.id) : null}
                />
              ))}
              <button className="addbtn" onClick={addItem}>
                <span className="addbtn__icon">＋</span>
                <span>Add review item</span>
              </button>
            </div>
          </Card>

          <Card>
            <div className="card__head card__head--builder">
              <div>
                <h3>Summary note (optional)</h3>
                <div className="t-sm t-muted">A short overview message that opens the return email. Not a substitute for review items.</div>
              </div>
            </div>
            <div className="card__body">
              <textarea
                className="textarea textarea--summary"
                value={summary}
                onChange={(e) => setSummary(e.target.value)}
                placeholder="Optional — e.g., 'Overall in good shape, three items below to address. Reach out if any are unclear.'"
              />
            </div>
          </Card>

          <Alert variant="warning" title="What happens when you send this back">
            <ul className="alert__list">
              <li>Status flips to <strong>Returned</strong>. All Recipient users at {sub.org.name} receive an email (REQ-041).</li>
              <li>AO Signature is <strong>cleared</strong>. The AO must re-sign before the recipient can resubmit (REQ-042).</li>
              <li>Each item must be individually acknowledged by the recipient before they can submit again (REQ-023).</li>
              <li>The original submission record is preserved read-only in the audit trail (REQ-035).</li>
            </ul>
          </Alert>
        </div>

        <div className="layout__side">
          <Rail title="Submission">
            <RailItem label="Organization">{sub.org.name}</RailItem>
            <RailItem label="UEI"><code>{sub.org.uei}</code></RailItem>
            <RailItem label="Region · State">{sub.org.region} · {sub.org.state}</RailItem>
            <RailItem label="Form">{fd.short}</RailItem>
            <RailItem label="Submitted">{sub.submitted}</RailItem>
          </Rail>

          <Rail title="Will be notified">
            <RailItem label="Primary contact">
              <div>{sub.data.contact.name}</div>
              <div className="t-xs t-muted">{sub.data.contact.email}</div>
            </RailItem>
            {sub.data.ao && (
              <RailItem label="Authorized Official">
                <div>{sub.data.ao.name}</div>
                <div className="t-xs t-muted">{sub.data.ao.email}</div>
              </RailItem>
            )}
          </Rail>

          <div className="sticky-actions">
            <Btn variant="ghost" fullWidth onClick={() => navTo(`#/sub/${sub.id}`)}>Cancel</Btn>
            <Btn fullWidth onClick={() => setShowPreview(true)} disabled={!canSend}>
              Preview & send · {validItems.length} item{validItems.length !== 1 ? 's' : ''}
            </Btn>
          </div>
        </div>
      </div>

      <Modal
        open={showPreview}
        onClose={() => setShowPreview(false)}
        title="Preview return"
        subtitle={`This is how it will appear to ${sub.org.name}`}
        width="lg"
        footer={
          <>
            <Btn variant="ghost" onClick={() => setShowPreview(false)}>Back to edit</Btn>
            <Btn onClick={onSend}>Send back with {validItems.length} item{validItems.length !== 1 ? 's' : ''}</Btn>
          </>
        }
      >
        <ReturnPreview sub={sub} items={validItems} summary={summary} />
      </Modal>
    </>
  );
}

function ReturnItemEditor({ item, fd, onChange, onRemove }) {
  return (
    <div className="ri-edit">
      <div className="ri-edit__num">{item.n}</div>
      <div className="ri-edit__body">
        <div className="ri-edit__loc">
          <Select label="Section" value={item.section || ''} onChange={(v) => onChange({ section: v, field: '' })}
            options={['', ...fd.sections.filter(s => !s.staffLocked).map(s => `${s.num}. ${s.title}`)]} />
          {item.section && (
            <input
              type="text"
              className="ri-edit__field"
              placeholder="Optional: field name (e.g., 'Administrative budget')"
              value={item.field}
              onChange={(e) => onChange({ field: e.target.value })}
            />
          )}
        </div>
        <textarea
          className="textarea"
          placeholder="Describe what the recipient needs to address. Be specific — cite policy where applicable. Avoid yes/no questions."
          value={item.text}
          onChange={(e) => onChange({ text: e.target.value })}
        />
        <div className="ri-edit__foot">
          <span className="t-xs t-muted">{item.text.length} characters</span>
        </div>
      </div>
      {onRemove && (
        <button className="ri-edit__del" onClick={onRemove} aria-label="Remove item" title="Remove">✕</button>
      )}
    </div>
  );
}

function ReturnPreview({ sub, items, summary }) {
  return (
    <div className="preview">
      <div className="preview__email">
        <div className="preview__from">CORE &lt;noreply@core.acf.gov&gt; → {sub.data.contact.email}{sub.data.ao && `, ${sub.data.ao.email}`}</div>
        <div className="preview__subject">Action required: Your {FORM_DEFS[sub.formType].short} submission has been returned</div>
      </div>
      <div className="preview__body">
        <p>Hello {sub.data.contact.name},</p>
        <p>Your {FORM_DEFS[sub.formType].short} submission for {sub.fy} has been returned with {items.length} review item{items.length !== 1 ? 's' : ''} that need to be addressed before resubmitting.</p>
        {summary && (
          <blockquote className="preview__summary">
            {summary}
          </blockquote>
        )}
        <p><strong>Review items to address:</strong></p>
        <ol className="preview__items">
          {items.map(it => (
            <li key={it.id}>
              {it.section && <div className="preview__loc"><em>{it.section}{it.field && ` · ${it.field}`}</em></div>}
              <div>{it.text}</div>
            </li>
          ))}
        </ol>
        <p><strong>Next steps:</strong></p>
        <ol>
          <li>Acknowledge each item in the form (required before resubmission).</li>
          <li>Have your Authorized Official re-sign — the AO signature has been cleared.</li>
          <li>Resubmit the form when ready.</li>
        </ol>
        <p>— Maya Rodriguez<br/>Federal Staff · OCS Division of Community Assistance</p>
      </div>
    </div>
  );
}

// ============================================================
// RETURNED-STATE PANEL — shown above form when status === 'Returned'
// ============================================================

function ReturnedStatePanel({ sub }) {
  const ackCount = sub.returnItems.filter(r => r.ack).length;
  const allAcked = ackCount === sub.returnItems.length;
  const aoSigned = sub.data.ao ? sub.data.ao.signed : true;
  return (
    <Card className="card--returned">
      <div className="returned__hd">
        <div>
          <h3>Returned · awaiting resubmit</h3>
          <div className="t-sm t-muted">Returned {sub.returnedAt} · {sub.returnItems.length} items · {ackCount} of {sub.returnItems.length} acknowledged · AO {aoSigned ? '✓ re-signed' : '⚠ has not re-signed'}</div>
        </div>
        <ProgressMeter total={sub.returnItems.length} done={ackCount} />
      </div>

      {sub.returnSummary && (
        <div className="returned__summary">
          <div className="returned__summary-lbl">Summary note sent</div>
          <div className="returned__summary-txt">"{sub.returnSummary}"</div>
        </div>
      )}

      <div className="returned__items">
        {sub.returnItems.map((ri, i) => (
          <div className={`ack-row ${ri.ack ? 'is-ack' : ''}`} key={ri.id}>
            <div className="ack-row__indicator">
              <div className={`ack-dot ${ri.ack ? 'is-ack' : ''}`}>{ri.ack ? '✓' : i + 1}</div>
            </div>
            <div className="ack-row__body">
              <div className="ack-row__loc">{ri.sectionLabel}{ri.fieldLabel && ` · ${ri.fieldLabel}`}</div>
              <div className="ack-row__txt">{ri.text}</div>
              {ri.ack ? (
                <div className="ack-row__resp">
                  <div className="ack-row__resp-lbl">Recipient response · {ri.ack.when}</div>
                  <div>"{ri.ack.response}"</div>
                  <div className="t-xs t-muted">Acknowledged by {ri.ack.by}</div>
                </div>
              ) : (
                <div className="ack-row__wait">⏳ Waiting for acknowledgement · sent {sub.returnedAt}</div>
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="returned__foot">
        <div className="returned__status">
          {!allAcked && <span className="t-sm t-muted">Recipient must acknowledge all items before resubmit (REQ-023).</span>}
          {allAcked && !aoSigned && <span className="t-sm t-muted">All items acknowledged. Awaiting AO resignature (REQ-042).</span>}
          {allAcked && aoSigned && <span className="t-sm" style={{ color: 'var(--success)' }}>✓ Ready for recipient to resubmit.</span>}
        </div>
        <Btn variant="ghost" size="sm">Email reminder</Btn>
      </div>
    </Card>
  );
}

function ProgressMeter({ total, done }) {
  const pct = total === 0 ? 0 : Math.round((done / total) * 100);
  return (
    <div className="meter">
      <div className="meter__bar"><div className="meter__fill" style={{ width: pct + '%' }} /></div>
      <div className="meter__txt">{done}/{total}</div>
    </div>
  );
}

// ============================================================
// RATIONALE MODAL (triggered from edit mode save)
// ============================================================

function RationaleModal() {
  const store = useStore();
  const dialog = store.dialogs.rationale;
  const [rationale, setRationale] = _useStateW('');

  _useEffectW(() => { setRationale(''); }, [dialog]);

  if (!dialog) return null;
  const sub = store.submissions.find(s => s.id === dialog.subId);
  if (!sub) return null;
  const editsList = Object.entries(dialog.pending);

  const onConfirm = () => {
    if (rationale.trim().length === 0) return;
    dialog.onConfirm(rationale);
    store.closeRationale();
    store.showToast(`${editsList.length} edit${editsList.length !== 1 ? 's' : ''} saved with rationale. Logged.`);
  };

  return (
    <Modal
      open
      onClose={store.closeRationale}
      title="Add a rationale for these edits"
      subtitle={`Required before edits can be saved · Logged in audit trail (REQ-043) · Visible to ${sub.org.name} and FOIA reviewers`}
      width="lg"
      footer={
        <>
          <Btn variant="ghost" onClick={store.closeRationale}>Cancel</Btn>
          <Btn onClick={onConfirm} disabled={rationale.trim().length === 0}>
            Save {editsList.length} edit{editsList.length !== 1 ? 's' : ''} with rationale
          </Btn>
        </>
      }
    >
      <div className="rat__changes">
        <div className="rat__changes-hd">{editsList.length} field{editsList.length !== 1 ? 's' : ''} will be saved with this rationale:</div>
        <ul className="rat__changes-list">
          {editsList.map(([path, change]) => (
            <li key={path}>
              <div className="rat__path">{prettyPath(path)}</div>
              <div className="rat__diff">
                <span className="rat__from">{displayChange(change.original)}</span>
                <span className="rat__arrow">→</span>
                <span className="rat__to">{displayChange(change.value)}</span>
              </div>
            </li>
          ))}
        </ul>
      </div>

      <div className="fld fld--full">
        <div className="fld__lbl">Rationale <span className="req">*</span></div>
        <textarea
          className="textarea textarea--rationale"
          value={rationale}
          onChange={(e) => setRationale(e.target.value)}
          placeholder="Explain why these changes are needed. Include context (call notes, emails, etc.) where helpful. One rationale covers all edits in this session."
          autoFocus
        />
        <div className="fld__hint">Plain text only · Min 1 character · Cannot be edited after save</div>
      </div>

      <div className="rat__lock">
        <strong>Restricted fields not edited:</strong> AO Signature and Attestation of Assurances are off-limits to Federal Staff (REQ-043).
      </div>
    </Modal>
  );
}

function prettyPath(path) {
  const map = {
    'contact.name': 'Primary Contact · Name',
    'contact.title': 'Primary Contact · Title',
    'contact.email': 'Primary Contact · Email',
    'contact.phone': 'Primary Contact · Phone',
    'plan.mission': 'Programmatic Plan · Mission',
    'plan.goals': 'Programmatic Plan · Goals',
    'plan.coordination': 'Programmatic Plan · Coordination',
    'services': 'Service Areas',
    'budget.employment': 'Proposed Budget · Employment Services',
    'budget.education': 'Proposed Budget · Education',
    'budget.emergency': 'Proposed Budget · Emergency Assistance',
    'budget.housing': 'Proposed Budget · Housing',
    'budget.nutrition': 'Proposed Budget · Nutrition',
    'budget.admin': 'Proposed Budget · Administrative',
    'budget.other': 'Proposed Budget · Other',
    'narrative.employment': 'Narrative · Employment',
    'narrative.housing': 'Narrative · Housing',
    'narrative.emergency': 'Narrative · Emergency',
    'period.start': 'Reporting Period · Start',
    'period.end': 'Reporting Period · End',
    'outcomes.individualsServed': 'Outcomes · Individuals Served',
    'outcomes.householdsServed': 'Outcomes · Households Served',
    'outcomes.employment': 'Outcomes · Employment',
    'outcomes.education': 'Outcomes · Education',
    'outcomes.housingStabilized': 'Outcomes · Housing Stabilized',
    'outcomes.foodSecurity': 'Outcomes · Food Security',
  };
  return map[path] || path;
}

function displayChange(v) {
  if (v == null || v === '') return '—';
  if (typeof v === 'number') return fmtCurrency(v);
  return String(v).length > 60 ? String(v).slice(0, 60) + '…' : String(v);
}

// ============================================================
// DETERMINATION MODAL
// ============================================================

function DeterminationModal() {
  const store = useStore();
  const dialog = store.dialogs.determination;
  const [outcome, setOutcome] = _useStateW('Accepted');
  const [notes, setNotes] = _useStateW('');
  const [confirming, setConfirming] = _useStateW(false);

  _useEffectW(() => {
    if (dialog) { setOutcome('Accepted'); setNotes(''); setConfirming(false); }
  }, [dialog]);

  if (!dialog) return null;
  const sub = store.submissions.find(s => s.id === dialog.subId);
  if (!sub) return null;
  const fd = FORM_DEFS[sub.formType];

  const onConfirm = () => {
    store.recordDetermination(sub.id, outcome, notes);
    store.closeDetermination();
    store.showToast(`Submission ${outcome === 'Accepted' ? 'accepted' : 'closed without acceptance'} and locked.`);
  };

  return (
    <Modal
      open
      onClose={store.closeDetermination}
      title="Record final determination"
      subtitle={`${sub.org.name} · ${fd.short} · ${sub.fy} · Submitted ${sub.submitted} · Returns ${sub.returns} of 1`}
      width="lg"
      footer={
        confirming ? (
          <>
            <Btn variant="ghost" onClick={() => setConfirming(false)}>Back</Btn>
            <Btn variant={outcome === 'Accepted' ? 'primary' : 'danger'} onClick={onConfirm}>
              Yes — {outcome === 'Accepted' ? 'Accept and lock' : 'Close and lock'}
            </Btn>
          </>
        ) : (
          <>
            <Btn variant="ghost" onClick={store.closeDetermination}>Cancel</Btn>
            <Btn onClick={() => setConfirming(true)}>Continue →</Btn>
          </>
        )
      }
    >
      {!confirming ? (
        <>
          <div
            className={`radio-card ${outcome === 'Accepted' ? 'is-selected is-selected--success' : ''}`}
            onClick={() => setOutcome('Accepted')}
          >
            <div className="radio-card__dot" />
            <div>
              <h4>✓ Accept submission</h4>
              <p>Form data is finalized and locked from all further edits. Recipient is notified. Available for CSV export and downstream reporting (REQ-027).</p>
            </div>
          </div>
          <div
            className={`radio-card ${outcome === 'Closed' ? 'is-selected is-selected--danger' : ''}`}
            onClick={() => setOutcome('Closed')}
          >
            <div className="radio-card__dot" />
            <div>
              <h4>✕ Close without acceptance</h4>
              <p>Submission is closed; data preserved for the record but not counted as accepted for this fiscal year. Recipient is notified. Use for withdrawals, organizational changes, or persistent quality issues.</p>
            </div>
          </div>

          <div className="fld fld--full" style={{ marginTop: 16 }}>
            <div className="fld__lbl">Determination notes</div>
            <textarea
              className="textarea"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder={outcome === 'Accepted'
                ? "Optional — note anything worth carrying forward (e.g., 'All review items resolved on resubmit. AO re-signed 5/16.')"
                : "Required — explain the reason for closing without acceptance."
              }
            />
            <div className="fld__hint">Stored with the determination record. Visible to recipient and in the activity log.</div>
          </div>

          <Alert variant="warning" title="This action is final">
            Per REQ-026, the submission is locked from <strong>all further edits by every user</strong>.
            If anything needs correcting, use <em>Edit on behalf</em> before recording the determination.
          </Alert>
        </>
      ) : (
        <>
          <div className="confirm-block">
            <div className="confirm-block__head">
              {outcome === 'Accepted' ? '✓' : '✕'} {outcome === 'Accepted' ? 'Accept' : 'Close without acceptance'}
            </div>
            <div className="confirm-block__body">
              <div className="confirm-row"><span>Submission</span><strong>{sub.org.name} · {fd.short} · {sub.fy}</strong></div>
              <div className="confirm-row"><span>By</span><strong>Maya Rodriguez · Federal Staff</strong></div>
              <div className="confirm-row"><span>Notes</span><strong>{notes || '— (none)'}</strong></div>
            </div>
          </div>
          <Alert variant="danger" title="Confirm — this is irreversible">
            Once recorded, this submission becomes read-only for all users. The only way to "re-open" is for engineering to intervene at the database level. Are you sure?
          </Alert>
        </>
      )}
    </Modal>
  );
}

// ============================================================
// LOGIN SCREEN
// ============================================================

function ScreenLogin() {
  const store = useStore();
  return (
    <div className="login-page">
      <GovBanner />
      <div className="login-wrap">
        <div className="login-card">
          <div className="login-card__brand">
            <div className="login-card__logo">C</div>
            <div>
              <div className="login-card__title">CORE</div>
              <div className="login-card__sub">Community Outcomes Reporting Engine</div>
            </div>
          </div>

          <h1 className="login-card__heading">Sign in to CORE</h1>
          <p className="login-card__lead">Office of Community Services · ACF</p>

          <button className="login-btn" onClick={() => { store.signIn(); navTo('#/inbox'); }}>
            <span className="login-btn__icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg>
            </span>
            Sign in with Login.acf.gov
          </button>

          <div className="login-card__divider"><span>or</span></div>

          <button className="login-link" onClick={() => { store.signIn(); navTo('#/inbox'); }}>
            Sign in with Login.gov (recipient users)
          </button>

          <div className="login-card__help">
            <div><strong>Federal Staff:</strong> Use your ACF Okta credentials.</div>
            <div><strong>Tribal Recipients:</strong> Use your Login.gov account.</div>
            <a href="#" className="login-card__link">Trouble signing in?</a>
          </div>
        </div>

        <div className="login-compliance">
          <span className="login-compliance__chip">FedRAMP Authorized</span>
          <span className="login-compliance__chip">FISMA Moderate</span>
          <span className="login-compliance__chip">FIPS 140-2</span>
          <span className="login-compliance__chip">Section 508 / WCAG 2.0 AA</span>
        </div>
      </div>
    </div>
  );
}

Object.assign(window, {
  ScreenReturnBuilder,
  ReturnedStatePanel,
  RationaleModal,
  DeterminationModal,
  ScreenLogin,
});
