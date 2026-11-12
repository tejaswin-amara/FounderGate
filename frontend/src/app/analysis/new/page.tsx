import { Button } from '@/components/ui/button'

export default function NewAnalysis() {
  return (
    <div className="flex-1 max-w-7xl mx-auto p-6 lg:p-8 w-full">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-on-surface">New Analysis</h1>
        <p className="text-on-surface-variant mt-2">Set up your hypothesis and provide interview data.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="space-y-6">
          <div className="bg-surface-container-low p-6 rounded-lg border border-outline-variant">
            <h2 className="text-xl font-semibold mb-4 text-on-surface">Pivot Hypothesis</h2>
            <textarea
              className="w-full h-32 bg-surface-container border border-outline-variant rounded-md p-3 text-on-surface focus:outline-none focus:ring-1 focus:ring-primary"
              placeholder="Enter your initial hypothesis here..."
            />
          </div>

          <div className="bg-surface-container-low p-6 rounded-lg border border-outline-variant">
            <h2 className="text-xl font-semibold mb-4 text-on-surface">Competitor Context</h2>
            <textarea
              className="w-full h-24 bg-surface-container border border-outline-variant rounded-md p-3 text-on-surface focus:outline-none focus:ring-1 focus:ring-primary"
              placeholder="List main competitors and alternative solutions..."
            />
          </div>
        </div>

        <div className="space-y-6">
          <div className="bg-surface-container-low p-6 rounded-lg border border-outline-variant h-full flex flex-col">
            <h2 className="text-xl font-semibold mb-4 text-on-surface">Interview Transcripts</h2>
            <div className="flex-1 bg-surface-container border border-outline-variant border-dashed rounded-md flex flex-col items-center justify-center p-8 text-center min-h-[200px]">
              <p className="text-on-surface-variant mb-4">Upload transcript files or paste text</p>
              <Button variant="secondary">Select Files</Button>
            </div>

            <div className="mt-4 flex justify-between items-center">
              <span className="text-sm text-on-surface-variant">Alternatively, use synthetic data:</span>
              <Button variant="outline" size="sm">Load Synthetic Scenario</Button>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-8 flex justify-end">
        <Button size="lg" className="w-full sm:w-auto">Start Analysis</Button>
      </div>
    </div>
  )
}
