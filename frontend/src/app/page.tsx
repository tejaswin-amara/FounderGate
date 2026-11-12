import Link from 'next/link'
import { Button } from '@/components/ui/button'

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-4 bg-background">
      <div className="max-w-3xl text-center space-y-8">
        <h1 className="text-5xl font-bold tracking-tight sm:text-6xl text-on-background">
          FounderGate
        </h1>
        <p className="text-xl text-on-surface-variant max-w-2xl mx-auto">
          Adversarial Customer Discovery and Go-To-Market discovery agent for early-stage founders.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center pt-8">
          <Link href="/analysis/new">
            <Button size="lg" className="w-full sm:w-auto">Start New Analysis</Button>
          </Link>
          <Link href="/report">
            <Button variant="outline" size="lg" className="w-full sm:w-auto">View Previous Reports</Button>
          </Link>
          <Link href="/analysis">
            <Button variant="ghost" size="lg" className="w-full sm:w-auto">View Active Analysis</Button>
          </Link>
        </div>
      </div>
    </div>
  )
}
