import {create} from 'zustand'
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
        interviewStep: {
          section: 0,
          question: 0,
        },
        setInterviewStep: (section, question) => {
          set((state) => {
            return {
              previousInterviewStep: {
                section: state.interviewStep.section,
                question: state.interviewStep.question,
              }
            }
          });
          set({ interviewStep: {section, question }})
        },
        previousInterviewStep: {
          section: 0,
          question: 0,
        },
        direction: 'forward',
        setDirection: (direction) => set({ direction }),
      }),
      {
        name: 'csfeer-storage', // key in storage
      }
    )
  )
)

export default interviewState