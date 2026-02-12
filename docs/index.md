# Form Engine Documentation

The `form_manager` app is a schema-driven form engine built on Django and Pydantic. It powers multi-step government forms (CSBG reports) with features like conditional field visibility, auto-calculated fields, currency formatting, audit trails, and PDF export.

Forms are defined entirely in Python as Pydantic schema classes that combine Django form fields with a declarative UI that also defines the interview-style form flow. The engine handles rendering, navigation, validation, data persistence and review workflows automatically.

## Table of Contents

- [Creating New Forms](./form_creation.md)
- [Available Form Fields](./form_fields.md)
- [UI Component Blocks](./form_ui.md)


### Data management

1. **Schema registration**: `python manage.py load_initial_forms` reads Python schema classes and creates `FormDefinition` records in the database.
2. **Form creation**: User starts a form, creating a `FormEntry` with an empty `data` JSON field.
3. **Editing**: Each page POST saves field values incrementally into `FormEntry.data`. Only submitted fields are updated; existing data is preserved.
4. **Review**: All data displayed for confirmation. Validation runs with `use_default_if_excluded=True` to apply defaults for excluded fields.
5. **Submission**: Status changes to "submitted", timestamp recorded, audit trail created.

### Key models

| Model | Purpose |
|---|---|
| `FormDefinition` | Template for a form type/version. Stores `schema_class` name for dynamic import. |
| `FormEntry` | A filled-out form instance. Stores data as JSON. Status: draft/submitted/amended/archived. |
| `FormAuditTrail` | High-level events (create, save, submit, lock, etc.) |
| `FormAuditDetail` | Field-level change tracking (old value, new value) |
| `OrganizationProfile` | Tribal org that owns form entries |
| `UserOrganizationMembership` | Links users to orgs with roles (admin/editor/viewer) |
