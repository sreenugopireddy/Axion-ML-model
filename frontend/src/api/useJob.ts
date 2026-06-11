import { useState, useEffect, useRef } from "react"
import { api } from "./client"
import type { JobResponse } from "./types"

export function useJob(jobId: string | null) {
  const [job, setJob] = useState<JobResponse | null>(null)
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null)

  useEffect(() => {
    if (!jobId) return
    const poll = async () => {
      try {
        const res = await api.get<JobResponse>(`/jobs/${jobId}`)
        setJob(res.data)
        if (res.data.status === "done" || res.data.status === "failed") {
          if (intervalRef.current) clearInterval(intervalRef.current)
        }
      } catch {
        if (intervalRef.current) clearInterval(intervalRef.current)
      }
    }
    poll()
    intervalRef.current = setInterval(poll, 1500)
    return () => { if (intervalRef.current) clearInterval(intervalRef.current) }
  }, [jobId])

  return job
}
