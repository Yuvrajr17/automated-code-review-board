
const agents = [
  {
    name: "Diff Agent",
    description: "Identifies modified files and summarizes code changes.",
    role: "CHANGE ANALYSIS",
  },
  {
    name: "Style Agent",
    description: "Checks readability, formatting and coding standards.",
    role: "CODE QUALITY",
  },
  {
    name: "Security Agent",
    description: "Detects potentially unsafe patterns and vulnerabilities.",
    role: "SECURITY ANALYSIS",
  },
  {
    name: "Test Coverage Agent",
    description: "Examines test files and evaluates test-related changes.",
    role: "TEST ANALYSIS",
  },
  {
    name: "Reviewer Manager",
    description: "Consolidates findings and generates the final recommendation.",
    role: "FINAL REVIEW",
  },
];

function AgentPipeline() {
  return (
    <section className="rounded-lg border border-slate-200 bg-white shadow-sm">
      <div className="border-b border-slate-100 px-5 py-4">
        <h2 className="text-base font-semibold text-slate-900">
          Review Pipeline
        </h2>
        <p className="mt-1 text-sm text-slate-500">
          Five specialized agents working together
        </p>
      </div>

      <div className="divide-y divide-slate-100 px-5">
        {agents.map((agent, index) => (
          <div key={agent.name} className="flex gap-3 py-4">
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-md border border-slate-200 bg-slate-50 text-xs font-semibold text-slate-600">
              0{index + 1}
            </div>

            <div className="min-w-0 flex-1">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <h3 className="text-sm font-semibold text-slate-800">
                  {agent.name}
                </h3>

                <span className="rounded border border-slate-200 bg-slate-50 px-2 py-1 text-[10px] font-medium uppercase tracking-wide text-slate-500">
                  {agent.role}
                </span>
              </div>

              <p className="mt-1 text-xs leading-5 text-slate-500">
                {agent.description}
              </p>
            </div>
          </div>
        ))}
      </div>

      <div className="border-t border-slate-100 bg-slate-50 px-5 py-3">
        <p className="text-xs text-slate-500">
          Agents will execute automatically when a review is submitted.
        </p>
      </div>
    </section>
  );
}

export default AgentPipeline;
