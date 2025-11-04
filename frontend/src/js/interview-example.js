import React, { useState, useEffect, useMemo, useRef } from "react";
import { createRoot } from "react-dom/client";
import {
  GridContainer,
  Grid,
  Label,
  TextInput,
  ButtonGroup,
  Button,
  Card,
  CardBody,
  CardHeader,
  CardGroup,
  Alert,
  Textarea,
} from "@trussworks/react-uswds";
import { interviewState as useInterviewState } from "./state";
import Slide from "@mui/material/Slide";

const SectionContainer = (props) => {
  const {
    title,
    description,
    instructional_note: instructionalNote,
    help_text: helpText,
  } = props.section;
  const { direction, interviewStep, previousInterviewStep } = useInterviewState();
  const [displayQuestion, setDisplayQuestion] = useState(null);
  const [slideIn, setSlideIn] = useState(false);
  const [slideFrom, setSlideFrom] = useState("left");
  const cardRef = useRef(null);

  const {question: questionNumber} = interviewStep;

  const animationTime = 600;

  useEffect(() => {
    if (displayQuestion === null) {
      setDisplayQuestion(questionNumber);
      setSlideIn(true);
    }

    if (displayQuestion !== questionNumber) {
      setSlideFrom(direction === "forward" ? "right" : "left");
      setSlideIn(false);

      const timeout = setTimeout(() => {
        setSlideFrom(direction === "forward" ? "left" : "right");
        setDisplayQuestion(questionNumber);
        setSlideIn(true);
      }, animationTime + 10);
    }
  }, [questionNumber]);

  const currentField = useMemo(() => {
    if (!props.section.fields || props.section.fields.length === 0) {
      return null;
    }

    const fieldDef = props.section.fields[displayQuestion || 0];

    const FieldComponent = fieldDef.type === "textarea" ? Textarea : TextInput;

    return (
      <div className="margin-y-4">
        <Label htmlFor={fieldDef.name} hint={fieldDef.help_text}>
          <p>{fieldDef.label}</p>
        </Label>
        <FieldComponent
          id={fieldDef.name}
          name={fieldDef.name}
          type={fieldDef.type !== "textarea" ? fieldDef.type : undefined}
          defaultValue={fieldDef.default || ""}
          required={fieldDef.required}
        />
      </div>
    );
  }, [displayQuestion, props.section]);

  return (
    <CardGroup>
      <Card className="width-full">
        <div ref={cardRef} style={{ overflow: "hidden" }}>
          <CardHeader>
            <h2>{title}</h2>
            <h3>{description}</h3>
            <Alert type="info" headingLevel="h4" slim>
              {instructionalNote}
            </Alert>
            <p>{helpText}</p>
          </CardHeader>

          <Slide
            direction={slideFrom}
            in={slideIn}
            mountOnEnter
            unmountOnExit
            container={cardRef.current}
            timeout={animationTime}
          >
            <CardBody>{currentField}</CardBody>
          </Slide>
        </div>
      </Card>
    </CardGroup>
  );
};

const App = ({ data }) => {
  const { setSection, setDirection, setInterviewStep, interviewStep } =
    useInterviewState();

  const {section, question} = interviewStep;

  const handleNext = () => {
    const questionsInSection = data.sections[section].fields.length;

    setDirection("forward");

    // if it's the last question in the section
    if (question === questionsInSection - 1) {
      // Move to next section
      if (section < data.sections.length - 1) {
        setInterviewStep(section + 1, 0);
        // setSection(section + 1);
        // setQuestion(0);
      }
    } else {
      console.log("Moving to next question");
      // Move to next question
      setInterviewStep(section, question + 1);
    }
  };

  const handleBack = () => {
    setDirection("backward");
    if (question === 0) {
      // Move to previous section
      if (section > 0) {
        const prevSectionQuestions = data.sections[section - 1].fields.length;
        setInterviewStep(section - 1, prevSectionQuestions - 1);
        setSection(section - 1);
      }
    } else {
      // Move to previous question
      setInterviewStep(section, question - 1);
    }
  };

  const activeSection = useMemo(() => {
    return data.sections[section];
  }, [section, data]);

  return (
    <GridContainer className="usa-section">
      <Grid
        row
        className="minh-mobile-lg flex-column"
        style={{ "justify-content": "space-between" }}
      >
        <Grid row>
          <SectionContainer section={activeSection} />
        </Grid>
        <Grid row>
          <ButtonGroup type="default">
            <Button
              disabled={section === 0 && question === 0}
              onClick={handleBack}
            >
              Back
            </Button>
            <Button onClick={handleNext}>Next</Button>
          </ButtonGroup>
        </Grid>
      </Grid>
    </GridContainer>
  );
};

if (
  window.location.href.includes("interview") &&
  document.getElementById("form-schema")
) {
  const data = JSON.parse(document.getElementById("form-schema").textContent);
  const root = createRoot(document.getElementById("main-content"));
  root.render(<App data={data} />);
}
