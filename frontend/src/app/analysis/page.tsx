import Link from 'next/link'
import { Button } from '@/components/ui/button'

export default function AnalysisView() {
  return (
    <div className="flex flex-col h-screen overflow-hidden bg-background">
      <header className="flex-none h-16 border-b border-outline-variant bg-surface-container-low px-6 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link href="/">
            <span className="font-bold text-lg tracking-tight text-on-surface">FounderGate</span>
          </Link>
          <span className="text-outline-variant">/</span>
          <span className="text-on-surface-variant font-medium">B2B SaaS Security</span>
        </div>
        <div className="flex items-center gap-4">
          <div className="px-3 py-1 rounded-full bg-surface-container border border-outline-variant text-sm font-medium flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-primary" />
            <span className="text-on-surface">Human Gate Locked</span>
          </div>
          <Button size="sm">Pivot & Sign Off</Button>
        </div>
      </header>

      <main className="flex-1 flex overflow-hidden">
        {/* Left Pane: Evidence Source */}
        <div className="w-1/2 flex flex-col border-r border-outline-variant bg-surface">
          <div className="flex-none p-4 border-b border-outline-variant bg-surface-container-low flex justify-between items-center">
            <h2 className="font-semibold text-on-surface">Source Evidence</h2>
            <select className="bg-surface-container border border-outline-variant text-sm rounded px-2 py-1 text-on-surface">
              <option>Interview 1: CISO</option>
              <option>Interview 2: DevSecOps Lead</option>
            </select>
          </div>
          <div className="flex-1 overflow-y-auto p-6 font-mono text-sm space-y-4 text-on-surface-variant">
            <div className="flex gap-4">
              <span className="text-outline flex-none select-none">12</span>
              <p><span className="text-tertiary">Interviewer:</span> What is your biggest challenge with current security scanning?</p>
            </div>
            <div className="flex gap-4 bg-surface-container-low -mx-2 px-2 py-1 rounded">
              <span className="text-outline flex-none select-none">13</span>
              <p><span className="text-primary">CISO:</span> Honestly, it&apos;s the noise. We get thousands of alerts and my team spends 40% of their time just triaging false positives. We&apos;d absolutely pay for something that just tells us what to fix first.</p>
            </div>
            <div className="flex gap-4">
              <span className="text-outline flex-none select-none">14</span>
              <p><span className="text-tertiary">Interviewer:</span> That makes sense. Would you buy a tool that automatically prioritizes them based on runtime context?</p>
            </div>
            <div className="flex gap-4">
              <span className="text-outline flex-none select-none">15</span>
              <p><span className="text-primary">CISO:</span> That sounds amazing. Yes, if it works like that, it would be a game changer.</p>
            </div>
          </div>
        </div>

        {/* Right Pane: Extractor & Skeptic Review */}
        <div className="w-1/2 flex flex-col bg-surface-container-lowest">
          <div className="flex-none p-4 border-b border-outline-variant bg-surface-container-low">
            <h2 className="font-semibold text-on-surface">Claim Review</h2>
          </div>
          <div className="flex-1 overflow-y-auto p-6 space-y-6">

            {/* Claim Card 1 */}
            <div className="bg-surface-container-low border border-outline-variant rounded-lg overflow-hidden">
              <div className="p-4 border-b border-outline-variant">
                <div className="flex justify-between items-start mb-2">
                  <span className="text-xs font-bold uppercase tracking-wider text-primary">Extracted Claim</span>
                  <span className="text-xs text-on-surface-variant font-mono">Lines 13-15</span>
                </div>
                <p className="text-on-surface font-medium">Customer expresses strong willingness to pay for runtime-contextualized alert prioritization.</p>
              </div>

              <div className="p-4 bg-surface-container border-b border-outline-variant">
                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 rounded bg-error-container flex items-center justify-center flex-none">
                    <span className="text-error font-bold">!</span>
                  </div>
                  <div>
                    <span className="text-xs font-bold uppercase tracking-wider text-error">Skeptic Challenge: The Mom Test</span>
                    <p className="text-sm text-on-surface-variant mt-1">This is a hypothetical future promise. The interviewer asked a leading question (&quot;Would you buy...&quot;), and the customer gave a polite, hypothetical answer (&quot;That sounds amazing. Yes, if...&quot;). This does not validate actual willingness to pay.</p>
                  </div>
                </div>
              </div>

              <div className="p-4 flex gap-3">
                <Button variant="outline" className="flex-1 border-error text-error hover:bg-error-container">Discard Claim</Button>
                <Button variant="outline" className="flex-1">Log Assumption Debt</Button>
                <Button variant="outline" className="flex-1 border-primary text-primary">Accept Anyway</Button>
              </div>
            </div>

            {/* Claim Card 2 */}
            <div className="bg-surface-container-low border border-outline-variant rounded-lg overflow-hidden opacity-75">
              <div className="p-4 border-b border-outline-variant">
                <div className="flex justify-between items-start mb-2">
                  <span className="text-xs font-bold uppercase tracking-wider text-primary">Extracted Claim</span>
                  <span className="text-xs text-on-surface-variant font-mono">Line 13</span>
                </div>
                <p className="text-on-surface font-medium">Security teams spend 40% of their time triaging false positives.</p>
              </div>

              <div className="p-4 bg-surface-container border-b border-outline-variant">
                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 rounded bg-surface-container-highest flex items-center justify-center flex-none">
                    <span className="text-on-surface-variant font-bold">✓</span>
                  </div>
                  <div>
                    <span className="text-xs font-bold uppercase tracking-wider text-on-surface-variant">Skeptic Assessment</span>
                    <p className="text-sm text-on-surface-variant mt-1">Valid evidence of a specific, current problem and quantifiable pain point.</p>
                  </div>
                </div>
              </div>

              <div className="p-4 flex gap-3">
                <div className="w-full text-center py-2 bg-surface-container-highest text-on-surface-variant text-sm font-medium rounded">
                  Accepted
                </div>
              </div>
            </div>

          </div>
        </div>
      </main>
    </div>
  )
}
