export interface UploadResponse {
  file_id: string
  filename: string
  rows: number
  cols: number
  columns: string[]
  numeric_cols: string[]
  categorical_cols: string[]
  null_counts: Record<string, number>
  memory_mb: number
}

export interface JobResponse {
  job_id: string
  status: "pending" | "running" | "done" | "failed"
  result: Record<string, unknown> | null
  error: string | null
}

export interface CleanRequest {
  file_id: string
  impute_numeric: string
  impute_categorical: string
  outlier_method: string
  outlier_threshold: number
  drop_duplicates: boolean
}
