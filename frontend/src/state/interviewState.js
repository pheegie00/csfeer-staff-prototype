import create from 'zustand'
import { devtools, persist } from 'zustand/middleware'

/*
  Minimal skeleton zustand store.
  - put shared UI/app state & actions here
  - extend with async actions and selectors as needed
*/
const interviewState = create(
  devtools(
    persist(
      (set, get) => ({
        // state
        user: null,
        sidebarOpen: false,
        items: [],

        // actions
        setUser: (user) => set({ user }),
        toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
        setItems: (items) => set({ items }),
        addItem: (item) => set((s) => ({ items: [...s.items, item] })),
        reset: () =>
          set({
            user: null,
            sidebarOpen: false,
            items: [],
          }),

        // example async action
        fetchItems: async (opts = {}) => {
          try {
            const res = await fetch('/api/items', opts)
            if (!res.ok) throw new Error(`HTTP ${res.status}`)
            const data = await res.json()
            set({ items: data })
            return data
          } catch (err) {
            // handle/log as appropriate for your app
            console.error('fetchItems error', err)
            throw err
          }
        },
      }),
      {
        name: 'csfeer-storage', // key in storage
      }
    )
  )
)

export default interviewState