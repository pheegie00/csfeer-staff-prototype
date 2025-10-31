import React, { useState, useEffect } from "react";
import { createRoot } from 'react-dom/client';
import { GridContainer, Grid, Label, TextInput, ButtonGroup, Button } from "@trussworks/react-uswds";

const SCHEMA = [
  {
    id: 1,
    question: "How much did your orgnaization spend on employment?",
    dataType: Number,
  },
  {
    id: 2,
    question:
      "How much did your orgnaization spend on Childcare, Early Childhood, Youth Development, and Adult Education?",
    dataType: Number,
  },
  {
    id: 3,
    question: "How much did your orgnaization spend on Housing?",
    dataType: Number,
  },
  {
    id: 4,
    question: "How much did your orgnaization spend on Health and Nutrition?",
    dataType: Number,
  },
  {
    id: 5,
    question:
      "How much did your orgnaization spend on Civic Engagement and Community Involvement?",
    dataType: Number,
  },
  {
    id: 6,
    question: "How much did your orgnaization spend on Transportation?",
    dataType: Number,
  },
  {
    id: 6,
    question:
      "How much did your orgnaization spend on Partnerships, Linkages, and Coordination?",
    dataType: Number,
  },
  {
    id: 7,
    question: "Did your orgnaization have any other expenses to report?",
    dataType: Number,
  },
];

const QuestionContainer = (props) => {

  const {id, question, dataType} = props.stepConfig;

  return (
    <GridContainer>
      <Grid row gap={2}>
        <h2>{question}</h2>
        <TextInput />
      </Grid>
      <ButtonGroup type="default">
        <Button>Back</Button>
        <Button>Next</Button>

      </ButtonGroup>
      
    </GridContainer>
  );
};

const App = () => {
  const [currentStep, setCurrentStep] = useState(1);

  const currentQuestion = SCHEMA[currentStep];

  return <QuestionContainer stepConfig={currentQuestion} />;
};


const root = createRoot(document.getElementById('main-content'));
root.render(<App />);