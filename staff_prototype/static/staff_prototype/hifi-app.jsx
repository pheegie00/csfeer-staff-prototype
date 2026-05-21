// CORE Hi-fi — Main App + Router + State store

const { useState: _useStateApp, useEffect: _useEffectApp, useCallback: _useCb, useMemo: _useMemoApp } = React;

// ============================================================
// ROUTER
// ============================================================

function parseHash() {
  const h = window.location.hash || '#/inbox';
  const parts = h.replace(/^#\/?/, '').split('/').filter(Boolean);
  return parts;
}

function useHashRoute() {
  const [parts, setParts] = _useStateApp(parseHash());
  _useEffectApp(() => {
    const handler = () => setParts(parseHash());
    window.addEventListener('hashchange', handler);
    return () => window.removeEventListener('hashchange', handler);
  }, []);
  return parts;
}

// ============================================================
// STATE STORE
// ============================================================

function useStoreState() {
  const [signedIn, setSignedIn] = _useStateApp(true); // start signed in for demo speed
  const [submissions, setSubmissions] = _useStateApp(window.INITIAL_SUBMISSIONS);
  const [dialogs, setDialogs] = _useStateApp({ rationale: null, determination: null });
  const [toast, setToast] = _useStateApp(null);

  const signIn = () => setSignedIn(true);
  const signOut = () => setSignedIn(false);

  const showToast = _useCb((message, variant = 'success') => setToast({ message, variant }), []);
  const closeToast = _useCb(() => setToast(null), []);

  const openRationale = _useCb((opts) => setDialogs(d => ({ ...d, rationale: opts })), []);
  const closeRationale = _useCb(() => setDialogs(d => ({ ...d, rationale: null })), []);
  const openDetermination = _useCb((opts) => setDialogs(d => ({ ...d, determination: opts })), []);
  const closeDetermination = _useCb(() => setDialogs(d => ({ ...d, determination: null })), []);

  const applyEdits = _useCb((subId, pending, rationale) => {
    setSubmissions(subs => subs.map(s => {
      if (s.id !== subId) return s;
      const fields = Object.entries(pending).map(([path, change]) => ({
        path,
        value: change.value,
        original: change.original,
      }));
      const editEntry = {
        when: nowStr(),
        who: 'Maya Rodriguez',
        whoRole: 'Federal Staff',
        rationale,
        fields,
      };
      // Apply edits to data
      let newData = s.data;
      fields.forEach(f => { newData = setByPath(newData, f.path, f.value); });
      // Build event log entries
      const newEvents = [
        {
          when: nowStr(),
          who: 'Maya Rodriguez',
          whoRole: 'Federal Staff',
          action: `Edited on behalf · ${fields.length} field${fields.length !== 1 ? 's' : ''}`,
          notes: `Rationale: ${rationale}`,
          kind: 'edit',
        },
        ...s.events,
      ];
      return {
        ...s,
        data: newData,
        edits: [...(s.edits || []), editEntry],
        pendingEdits: {},
        updated: todayStr(),
        status: s.status === 'Submitted' ? 'In Progress' : s.status,
        events: newEvents,
      };
    }));
  }, []);

  const returnSubmission = _useCb((subId, items, summary) => {
    setSubmissions(subs => subs.map(s => {
      if (s.id !== subId) return s;
      const returnItems = items.map((it, i) => ({
        id: 'r_' + Math.random().toString(36).slice(2, 8),
        section: it.section,
        field: it.field,
        sectionLabel: it.section,
        fieldLabel: it.field,
        text: it.text,
        ack: null,
      }));
      const updatedAO = s.data.ao ? { ...s.data.ao, signed: false, cleared: true, clearedAt: todayStr() } : s.data.ao;
      const newEvents = [
        {
          when: nowStr(),
          who: 'Maya Rodriguez',
          whoRole: 'Federal Staff',
          action: `Returned submission · ${items.length} item${items.length !== 1 ? 's' : ''}`,
          notes: `${s.data.ao ? 'AO signature cleared. ' : ''}Recipient notified.${summary ? ' Summary note: ' + summary : ''}`,
          kind: 'return',
        },
        ...s.events,
      ];
      return {
        ...s,
        status: 'Returned',
        returns: 1,
        returnItems,
        returnSummary: summary,
        returnedAt: todayStr(),
        data: { ...s.data, ao: updatedAO },
        updated: todayStr(),
        events: newEvents,
      };
    }));
  }, []);

  const recordDetermination = _useCb((subId, outcome, notes) => {
    setSubmissions(subs => subs.map(s => {
      if (s.id !== subId) return s;
      const status = outcome === 'Accepted' ? 'Accepted' : 'Closed';
      const determination = {
        outcome: status === 'Accepted' ? 'Accepted' : 'Closed without Acceptance',
        when: todayStr(),
        by: 'Maya Rodriguez',
        notes,
      };
      const newEvents = [
        {
          when: nowStr(),
          who: 'Maya Rodriguez',
          whoRole: 'Federal Staff',
          action: status === 'Accepted' ? 'Accepted submission · final determination' : 'Closed without acceptance · final determination',
          notes: notes || undefined,
          kind: status === 'Accepted' ? 'accept' : 'close',
        },
        ...s.events,
      ];
      return {
        ...s,
        status,
        determination,
        resolved: todayStr(),
        updated: todayStr(),
        events: newEvents,
      };
    }));
  }, []);

  return {
    user: window.MOCK_USER,
    signedIn,
    submissions,
    dialogs,
    toast,
    signIn, signOut,
    showToast, closeToast,
    openRationale, closeRationale,
    openDetermination, closeDetermination,
    applyEdits,
    returnSubmission,
    recordDetermination,
  };
}

function nowStr() {
  const d = new Date();
  return d.toISOString().slice(0, 16).replace('T', ' ');
}
function todayStr() {
  return new Date().toISOString().slice(0, 10);
}

// ============================================================
// MAIN APP
// ============================================================

function App() {
  const store = useStoreState();
  const route = useHashRoute();

  // Default landing
  _useEffectApp(() => {
    if (route.length === 0) {
      window.location.hash = store.signedIn ? '#/inbox' : '#/login';
    }
  }, [route.length, store.signedIn]);

  return (
    <StoreCtx.Provider value={store}>
      <Routes route={route} />
      <RationaleModal />
      <DeterminationModal />
      <Toast message={store.toast?.message} variant={store.toast?.variant} onClose={store.closeToast} />
    </StoreCtx.Provider>
  );
}

function Routes({ route }) {
  // route is an array of path parts: [] | ['login'] | ['inbox'] | ['sub', id] | ['sub', id, 'edit'] | ['sub', id, 'return']
  const top = route[0];

  if (top === 'login' || top === undefined) return <LoginShell />;

  return (
    <div className="app">
      <GovBanner />
      <AppHeader />
      <main className="app__body">
        {top === 'inbox' && <ScreenInbox />}
        {top === 'sub' && route[1] && route[2] === undefined && <ScreenSubmission id={route[1]} mode="review" />}
        {top === 'sub' && route[1] && route[2] === 'edit' && <ScreenSubmission id={route[1]} mode="edit" />}
        {top === 'sub' && route[1] && route[2] === 'return' && <ScreenReturnBuilder id={route[1]} />}
        {top === 'forms' && <Placeholder title="Form templates" hint="Out of scope for staff workflow MVP — managed by Focus engineering manually per REQ-001." />}
        {top === 'exports' && <Placeholder title="Exports" hint="CSV export per REQ-027 (resolved submissions only)." />}
        {top === 'help' && <Placeholder title="Help" hint="Documentation, contact info, and accessibility statements." />}
      </main>
    </div>
  );
}

function LoginShell() {
  return <ScreenLogin />;
}

// ============================================================
// PLACEHOLDER for unimplemented routes
// ============================================================

function Placeholder({ title, hint }) {
  return (
    <div className="placeholder">
      <PageHeader title={title} meta="Not in this prototype's scope" />
      <Card>
        <div className="placeholder__body">
          <div className="placeholder__icon">🏗</div>
          <p>{hint}</p>
          <a className="btn btn--outline" href="#/inbox">Back to submissions</a>
        </div>
      </Card>
    </div>
  );
}

// ============================================================
// MOUNT
// ============================================================

if (!window.CORE_SKIP_MOUNT) {
  const root = ReactDOM.createRoot(document.getElementById('root'));
  root.render(<App />);
}

// Expose for cross-file (print.jsx etc)
Object.assign(window, { useStoreState, App, Routes, nowStr, todayStr });
