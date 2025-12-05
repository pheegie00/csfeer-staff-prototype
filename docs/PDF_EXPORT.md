# PDF Export Feature

## Overview
Form entries can now be downloaded as PDF documents from multiple locations in the application.

## System Requirements

### macOS
WeasyPrint requires system libraries to be installed:
```bash
brew install cairo pango gdk-pixbuf gobject-introspection
```

### Linux (Debian/Ubuntu)
```bash
sudo apt-get install python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
```

### Docker
System dependencies are typically pre-installed in Python Docker images. Add to Dockerfile if needed:
```dockerfile
RUN apt-get update && apt-get install -y \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0
```

## Usage

### 1. From Form Edit Page
- Navigate to `/forms/entry/{id}/edit/`
- Click "Download as PDF" in the Quick Actions sidebar

### 2. From Form Preview Page
- Navigate to `/forms/entry/{id}/preview/`
- Click "Download PDF" button in the navigation actions

### 3. From Django Admin
- Go to `/admin/form_manager/formentry/`
- Click "Download PDF" link in the rightmost column for any entry

## Technical Details

### URL Endpoint
- **URL**: `/forms/entry/<int:pk>/download/`
- **Name**: `form_download_pdf`
- **View**: `form_manager.views.FormDownloadPDFView` (class-based view)
- **Permission**: Requires `can_view()` access via `FormPermissionMixin`

### PDF Generation
- Uses WeasyPrint to convert HTML to PDF
- Template: `form_manager/templates/forms/form_pdf.html`
- Styling: Embedded CSS optimized for print with USWDS design tokens
- Filename format: `{form_name}_v{version}_{id}.pdf`

### PDF Features
- Professional layout with USWDS styling
- Organization and form metadata header
- Status badge (Draft/Submitted/Amended/Archived)
- All form fields with labels and help text
- Submission information (date, submitter, last updated)
- Page numbers and headers
- Proper page breaks to avoid splitting fields

## Troubleshooting

### Error: "cannot load library 'libgobject-2.0-0'"
Install gobject-introspection:
```bash
brew install gobject-introspection  # macOS
# or
sudo apt-get install libgirepository1.0-dev  # Linux
```

### PDF Generation is Slow
This is normal for WeasyPrint. For large forms:
- Consider caching generated PDFs
- Use background tasks (Celery) for PDF generation
- Implement a "generating PDF" loading indicator

### Fonts Not Rendering
Ensure system fonts are accessible. WeasyPrint uses Pango for font rendering.

## Future Enhancements

Potential improvements:
1. Cache generated PDFs to avoid regeneration
2. Add watermark for draft/amended forms
3. Include audit trail in PDF
4. Bulk export multiple forms as ZIP
5. Custom PDF templates per form type
6. Add organization logo/branding
