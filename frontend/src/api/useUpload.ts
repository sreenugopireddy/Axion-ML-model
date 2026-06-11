import { useState } from "react"
import { api } from "./client"
import type { UploadResponse } from "./types"

export function useUpload() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function upload(file: File): Promise<UploadResponse | null> {
    setLoading(true)
    setError(null)
    try {
      const form = new FormData()
      form.append("file", file)
      const res = await api.post<UploadResponse>("/upload", form, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      return res.data
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "Upload failed"
      setError(msg)
      return null
    } finally {
      setLoading(false)
    }
  }

  return { upload, loading, error }
}
