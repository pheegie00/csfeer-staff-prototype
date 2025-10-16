{{- define "csfeer.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end }}

{{- define "csfeer.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{- define "csfeer.chart" -}}
{{- printf "%s-%s" .Chart.Name (.Chart.Version | replace "+" "-") | trunc 63 | trimSuffix "-" -}}
{{- end }}

{{- define "csfeer.labels" -}}
app.kubernetes.io/name: {{ include "csfeer.name" . }}
app.kubernetes.io/instance: {{ .Release.Name | quote }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service | quote }}
helm.sh/chart: {{ include "csfeer.chart" . }}
{{- end }}

{{- define "csfeer.selectorLabels" -}}
app.kubernetes.io/name: {{ include "csfeer.name" . }}
app.kubernetes.io/instance: {{ .Release.Name | quote }}
{{- end }}
