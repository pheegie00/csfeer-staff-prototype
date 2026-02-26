/**
 * Form utility functions
 */

/**
 * Updates calculated fields based on their source fields.
 * This function is called when form inputs change and automatically
 * updates any fields with the "calculated-currency-field" or "calculated-field" classes.
 *
 * @param {Event} e - The change event from the form
 */
export function updateCalculatedFields(e) {
  const calculatedFields = e.currentTarget.querySelectorAll(".calculated-currency-field, .calculated-field");
  calculatedFields.forEach((field) => {
    let sourceFields = field.getAttribute("data-source-fields");
    sourceFields = sourceFields.split(',')
    const total = sourceFields.reduce((total, fieldName, index) => {
      const sourceField = e.currentTarget.querySelector(`[name=${fieldName}]`)
      if (sourceField === null) {
        return total;
      }
      let numericValue = parseFloat((sourceField.value || "0.0").replace(/,/g, ''));
      const newTotal = numericValue + total;
      return newTotal
    }, 0.0);
    const isCurrency = field.classList.contains("calculated-currency-field");
    const formatOptions = isCurrency
      ? { style: "decimal", minimumFractionDigits: 2 }
      : { style: "decimal", minimumFractionDigits: 0, maximumFractionDigits: 0 };
    field.value = Intl.NumberFormat("en-US", formatOptions).format(total);
  })
}
