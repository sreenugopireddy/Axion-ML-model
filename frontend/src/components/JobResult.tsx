import { useJob } from "../api/useJob"

interface Props {
  jobId: string
  onDone?: (result: Record<string, unknown>) => void
}

export function JobResult({ jobId, onDone }: Props) {
  const job = useJob(jobId)

  if (!job) return (
    <div className="text-zinc-400 animate-pulse">Waiting for job...</div>
  )

  if (job.status === "pending" || job.status === "running") return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-lg p-6">
      <div className="flex items-center gap-3">
        <div className="w-3 h-3 rounded-full bg-axon-500 animate-ping" />
        <p className="text-zinc-300">Job running... <span className="text-zinc-500 text-sm">{jobId}</span></p>
      </div>
    </div>
  )

  if (job.status === "failed") return (
    <div className="bg-red-950 border border-red-800 rounded-lg p-6">
      <p className="text-red-400 font-medium">Job failed</p>
      <p className="text-red-300 text-sm mt-1">{job.error}</p>
    </div>
  )

  if (job.status === "done" && job.result) {
    onDone?.(job.result)
    const r = job.result as Record<string, unknown>
    return (
      <div className="bg-zinc-900 border border-zinc-800 rounded-lg p-6 space-y-4">
        <p className="text-green-400 font-medium">✓ Job complete</p>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          {Object.entries(r)
            .filter(([, v]) => typeof v === "number")
            .map(([k, v]) => (
              <div key={k} className="bg-zinc-800 rounded p-3">
                <p className="text-zinc-400 text-xs">{k.replace(/_/g, " ")}</p>
                <p className="text-white font-semibold">{String(v)}</p>
              </div>
            ))}
        </div>
        <details className="text-sm">
          <summary className="text-zinc-400 cursor-pointer hover:text-zinc-200">
            Full result JSON
          </summary>
          <pre className="mt-2 text-zinc-300 bg-zinc-950 p-3 rounded text-xs overflow-auto max-h-48">
            {JSON.stringify(r, null, 2)}
          </pre>
        </details>
      </div>
    )
  }

  return null
}
