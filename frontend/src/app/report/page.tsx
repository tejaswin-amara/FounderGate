import { Button } from '@/components/ui/button'

export default function ReportView() {
  return (
    <div className="flex flex-col min-h-screen bg-background text-on-background p-8">
      <div className="max-w-4xl mx-auto w-full space-y-12">
        <header className="flex justify-between items-end border-b border-outline-variant pb-6">
          <div>
            <h1 className="text-4xl font-bold tracking-tight mb-2">Strategic Decision Record</h1>
            <p className="text-on-surface-variant text-lg">B2B SaaS Security • Generated Nov 16, 2026</p>
          </div>
          <Button variant="outline">Export Bilingual PDF</Button>
        </header>

        <section className="space-y-6">
          <div className="bg-surface-container-low p-6 rounded-lg border border-outline-variant">
            <h2 className="text-sm font-bold uppercase tracking-wider text-primary mb-4">Pivot Hypothesis & Target Wedge</h2>
            <p className="text-lg leading-relaxed">
              We initially hypothesized that CISOs wanted a new scanning tool.
              Evidence proved this wrong; they have too many tools. The new target wedge is an integration layer that prioritizes existing scanner alerts based on runtime context.
            </p>
          </div>
        </section>

        <section className="space-y-6">
          <h2 className="text-2xl font-semibold">Validated Evidence</h2>
          <div className="grid gap-4">
            <div className="bg-surface-container border border-outline-variant p-5 rounded-lg flex gap-4">
              <div className="w-1 bg-primary rounded-full" />
              <div>
                <p className="font-medium mb-2">Security teams spend ~40% of their time triaging false positives.</p>
                <p className="text-sm text-on-surface-variant font-mono">Source: Interview 1 (CISO), Line 13</p>
              </div>
            </div>
            <div className="bg-surface-container border border-outline-variant p-5 rounded-lg flex gap-4">
              <div className="w-1 bg-primary rounded-full" />
              <div>
                <p className="font-medium mb-2">Current solutions lack runtime context, leading to over-prioritization of unreachable vulnerabilities.</p>
                <p className="text-sm text-on-surface-variant font-mono">Source: Interview 2 (DevSecOps), Line 45</p>
              </div>
            </div>
          </div>
        </section>

        <section className="space-y-6">
          <h2 className="text-2xl font-semibold text-error">Assumption Debt Ledger</h2>
          <p className="text-on-surface-variant">Claims that were logged for future validation, not accepted as current facts.</p>
          <div className="grid gap-4">
            <div className="bg-error-container/20 border border-error/30 p-5 rounded-lg">
              <p className="font-medium text-error mb-2">Willingness to pay for prioritization tool.</p>
              <p className="text-sm text-on-surface-variant mb-3">
                Skeptic note: Derived from a leading question (&quot;Would you buy...&quot;) and a hypothetical polite response.
              </p>
              <div className="text-sm bg-surface-container-low p-3 rounded border border-outline-variant inline-block">
                <span className="font-bold text-on-surface">Test needed:</span> Offer a paid pilot or letter of intent.
              </div>
            </div>
          </div>
        </section>

        <div className="pt-12 text-center text-sm text-on-surface-variant border-t border-outline-variant">
          <p>This report was generated after 100% of extracted claims were human-adjudicated.</p>
        </div>
      </div>
    </div>
  )
}
