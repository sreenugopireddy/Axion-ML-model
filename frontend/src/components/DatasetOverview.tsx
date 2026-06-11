import type { UploadResponse } from "../api/types"

interface Props {
  data: UploadResponse
  onClean: () => void
  cleaning: boolean
}

export function DatasetOverview({ data, onClean, cleaning }: Props) {
  const nullCols = Object.entries(data.null_counts).filter(([, v]) => v > 0)

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: "Rows", value: data.rows.toLocaleString() },
          { label: "Columns", value: data.cols },
          { label: "Numeric cols", value: data.numeric_cols.length },
          { label: "Memory", value: `${data.memory_mb} MB` },
        ].map((s) => (
          <div key={s.label} className="bg-zinc-900 rounded-lg p-4 border border-zinc-800">
            <p className="text-zinc-400 text-xs uppercase tracking-wider">{s.label}</p>
            <p className="text-2xl font-semibold text-white mt-1">{s.value}</p>
          </div>
        ))}
      </div>

      <div className="bg-zinc-900 rounded-lg p-4 border border-zinc-800">
        <p className="text-zinc-400 text-sm mb-2">
          File: <span className="text-white">{data.filename}</span>
          {nullCols.length === 0 && (
            <span className="ml-3 text-green-400 text-xs">✓ No null values</span>
          )}
        </p>
        <div className="flex flex-wrap gap-2 max-h-32 overflow-y-auto">
          {data.columns.slice(0, 40).map((col) => (
            <span key={col} className="bg-zinc-800 text-zinc-300 text-xs px-2 py-1 rounded">
              {col}
            </span>
          ))}
          {data.columns.length > 40 && (
            <span className="text-zinc-500 text-xs px-2 py-1">
              +{data.columns.length - 40} more
            </span>
          )}
        </div>
      </div>

      <button
        onClick={onClean}
        disabled={cleaning}
        className="w-full bg-axon-500 hover:bg-axon-600 disabled:opacity-50 text-white
          font-medium py-3 rounded-lg transition-colors"
      >
        {cleaning ? "Running clean job..." : "Run Clean Pipeline →"}
      </button>
    </div>
  )
}
