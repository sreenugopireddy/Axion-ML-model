import { useState } from "react"
import { FileUpload } from "./components/FileUpload"
import { DatasetOverview } from "./components/DatasetOverview"
import { JobResult } from "./components/JobResult"
import { api } from "./api/client"
import type { UploadResponse } from "./api/types"

export default function App() {
  const [dataset, setDataset] = useState<UploadResponse | null>(null)
  const [cleanJobId, setCleanJobId] = useState<string | null>(null)
  const [cleaning, setCleaning] = useState(false)

  async function handleClean() {
    if (!dataset) return
    setCleaning(true)
    try {
      const res = await api.post("/clean", {
        file_id: dataset.file_id,
        impute_numeric: "median",
        impute_categorical: "mode",
        outlier_method: "none",
        outlier_threshold: 1.5,
        drop_duplicates: true,
      })
      setCleanJobId(res.data.job_id)
    } finally {
      setCleaning(false)
    }
  }

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100">
      <header className="border-b border-zinc-800 px-8 py-4 flex items-center gap-3">
        <div className="w-7 h-7 rounded-full bg-axon-500" />
        <span className="text-xl font-semibold tracking-tight">Axon</span>
        <span className="text-zinc-500 text-sm ml-2">ML Pipeline Studio</span>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-10 space-y-8">
        <div>
          <h1 className="text-3xl font-bold text-white">Upload a dataset</h1>
          <p className="text-zinc-400 mt-1">Clean, analyse, and train — all from your browser.</p>
        </div>

        {!dataset ? (
          <FileUpload onUploaded={setDataset} />
        ) : (
          <DatasetOverview
            data={dataset}
            onClean={handleClean}
            cleaning={cleaning}
          />
        )}

        {cleanJobId && (
          <div>
            <h2 className="text-lg font-semibold mb-3">Clean job</h2>
            <JobResult jobId={cleanJobId} />
          </div>
        )}

        {dataset && (
          <button
            onClick={() => { setDataset(null); setCleanJobId(null) }}
            className="text-zinc-500 text-sm hover:text-zinc-300 transition-colors"
          >
            ← Upload different file
          </button>
        )}
      </main>
    </div>
  )
}
