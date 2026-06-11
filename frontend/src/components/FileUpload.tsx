import { useRef, useState } from "react"
import { useUpload } from "../api/useUpload"
import type { UploadResponse } from "../api/types"

interface Props {
  onUploaded: (data: UploadResponse) => void
}

export function FileUpload({ onUploaded }: Props) {
  const { upload, loading, error } = useUpload()
  const inputRef = useRef<HTMLInputElement>(null)
  const [dragging, setDragging] = useState(false)

  async function handleFile(file: File) {
    const data = await upload(file)
    if (data) onUploaded(data)
  }

  return (
    <div
      onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
      onDragLeave={() => setDragging(false)}
      onDrop={(e) => {
        e.preventDefault()
        setDragging(false)
        const file = e.dataTransfer.files[0]
        if (file) handleFile(file)
      }}
      onClick={() => inputRef.current?.click()}
      className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all
        ${dragging ? "border-axon-500 bg-axon-900/30" : "border-zinc-700 hover:border-axon-500"}`}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".csv,.tsv,.parquet"
        className="hidden"
        onChange={(e) => { const f = e.target.files?.[0]; if (f) handleFile(f) }}
      />
      <div className="text-4xl mb-3">⬆</div>
      {loading ? (
        <p className="text-axon-500 animate-pulse">Uploading...</p>
      ) : (
        <>
          <p className="text-zinc-300 font-medium">Drop your CSV here or click to browse</p>
          <p className="text-zinc-500 text-sm mt-1">CSV · TSV · Parquet</p>
        </>
      )}
      {error && <p className="text-red-400 text-sm mt-2">{error}</p>}
    </div>
  )
}
