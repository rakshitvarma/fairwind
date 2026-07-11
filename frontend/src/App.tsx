import { useState } from "react";
import { RouteWiseLogo } from "./assets";
import { Playground, type HistoryEntry } from "./components/Playground";
import { ModelsGrid } from "./components/ModelsGrid";
import { History } from "./components/History";
import { Stats } from "./components/Stats";

const GITHUB_URL = "https://github.com/rakshitvarma/routewise";
const DOCKER_URL = "https://github.com/rakshitvarma/routewise/pkgs/container/routewise";

function App() {
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const totalTokens = history.reduce((sum, h) => sum + h.tokens, 0);

  return (
    <div className="min-h-screen bg-[radial-gradient(ellipse_80%_50%_at_50%_-20%,rgba(124,92,252,0.15),transparent)]">
      <nav className="sticky top-0 z-10 border-b border-neutral-900/80 bg-black/70 backdrop-blur-xl">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-3.5">
          <div className="flex items-center gap-2.5">
            <RouteWiseLogo size={28} />
            <span className="text-lg font-bold tracking-tight text-white">RouteWise</span>
          </div>
          <div className="flex items-center gap-5 text-sm text-neutral-400">
            <a href={GITHUB_URL} target="_blank" rel="noreferrer" className="transition hover:text-white">
              GitHub
            </a>
            <a href={DOCKER_URL} target="_blank" rel="noreferrer" className="transition hover:text-white">
              Docker image
            </a>
          </div>
        </div>
      </nav>

      <main className="mx-auto max-w-5xl px-6 pb-24 pt-14">
        <div className="mb-10 text-center">
          <h1 className="text-4xl font-bold tracking-tight text-white sm:text-5xl">
            Route every task to the{" "}
            <span className="bg-gradient-to-r from-violet-400 via-sky-300 to-cyan-300 bg-clip-text text-transparent">
              cheapest model
            </span>{" "}
            that can answer it
          </h1>
          <p className="mx-auto mt-4 max-w-2xl text-[15px] leading-relaxed text-neutral-400">
            A hybrid routing agent that classifies each task for free, answers it locally when a
            small bundled model can be trusted, and only spends Fireworks tokens on what genuinely
            needs it. Built for AMD Developer Hackathon Act II, Track 1.
          </p>
        </div>

        <div className="mb-8">
          <Stats tokens={totalTokens} queries={history.length} />
        </div>

        <Playground onResult={(e) => setHistory((h) => [e, ...h])} />

        <History entries={history} />

        <section className="mt-16">
          <h2 className="mb-1 text-xl font-bold text-white">Models in play</h2>
          <p className="mb-5 text-sm text-neutral-500">
            Local models answer for free when they can be trusted; everything else routes to the
            cheapest sufficient Fireworks model.
          </p>
          <ModelsGrid />
        </section>

        <section className="mt-16">
          <h2 className="mb-4 text-xl font-bold text-white">How it works</h2>
          <ol className="space-y-3 text-[15px] leading-relaxed text-neutral-400">
            <li>
              <span className="font-semibold text-neutral-200">Local classifier</span> (regex, 0
              tokens) routes the task into one of 8 categories.
            </li>
            <li>
              <span className="font-semibold text-neutral-200">Deterministic math solver</span>{" "}
              answers bare arithmetic instantly for free — word problems fall through to
              Fireworks.
            </li>
            <li>
              <span className="font-semibold text-neutral-200">Two bundled local models</span>{" "}
              answer factual/sentiment/NER/summarisation and code_debug/code_gen for free,
              sanity- and syntax-checked before being trusted.
            </li>
            <li>
              <span className="font-semibold text-neutral-200">Logic puzzles</span> get 3-call
              self-consistency (majority vote) — cheap insurance against a demonstrated
              flaky-reasoning failure mode.
            </li>
            <li>
              <span className="font-semibold text-neutral-200">Everything else</span> is merged by
              model into as few Fireworks calls as possible, not one call per category.
            </li>
          </ol>
        </section>
      </main>

      <footer className="border-t border-neutral-900 py-8 text-center text-sm text-neutral-600">
        Built for AMD Developer Hackathon Act II · Track 1
      </footer>
    </div>
  );
}

export default App;
